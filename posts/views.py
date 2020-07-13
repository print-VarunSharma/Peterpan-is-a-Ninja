from django.db.models import Count, Q
from django.db import models

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.template import Context, loader, TemplateDoesNotExist
from django.http import Http404

from django.views.generic import TemplateView

from .forms import CommentForm, PostForm
from .models import Post, Author, PostView
from marketing.forms import EmailSignupForm
from marketing.models import Signup

from posts import views

# Gallery
from django.views.generic import DetailView, ListView, FormView
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from gallery.models import Image, Album
from gallery.forms import ImageCreateForm
from gallery import settings

form = EmailSignupForm()


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None


class SearchView(View):
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(overview__icontains=query)
            ).distinct()
        context = {
            'queryset': queryset
        }
        return render(request, 'search_results.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post \
        .objects \
        .values('categories__title') \
        .annotate(Count('categories__title'))
    return queryset


class IndexView(View):
    form = EmailSignupForm()

    def get(self, request, *args, **kwargs):
        featured = Post.objects.filter(featured=True)
        latest = Post.objects.order_by('-timestamp')[0:3]
        context = {
            'object_list': featured,
            'latest': latest,
            'form': self.form
        }
        return render(request, 'index.html', context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()
        messages.info(request, "Successfully subscribed")
        return redirect("home")


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,
        'latest': latest,
        'form': form
    }

    return render(request, 'index.html', context)


class PostListView(ListView):
    form = EmailSignupForm()
    model = Post
    template_name = 'blog.html'
    context_object_name = 'queryset'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context


def post_list(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_request_var': page_request_var,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'blog.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'pk': post.pk
            }))


def post_detail(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)


class PostCreateView(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        form.instance.author = get_author(self.request.user)
        form.save()
        return redirect(reverse("post-detail", kwargs={
            'pk': form.instance.pk
        }))


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'post_confirm_delete.html'


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))

# ---------------------------Interactive Map----------------------------------------


class MapView(TemplateView):
    template_name = 'interactivemap.html'


def interactivemap(request):
    return render(request, 'home.html', context)

# ------------------------- Social Media-----------------------------------------------


class SocialmediaView(TemplateView):
    template_name = 'socialmedia.html'

    def socialmedia(request):
        return render(request, 'socialmedia.html', context)

# ------------------------------Gallery Views--------------------------------------------


class GalleryView(TemplateView):
    template_name = 'gallerydisplay.html'

# -------------------Contact me ----------------------------


class ContactView(TemplateView):
    template_name = 'contact.html'
# ---------------------Star Cross Gallery----------------------------------


class GallerySettingsMixin(object):
    """ Apply Gallery's Settings to a view """

    def get_context_data(self, **kwargs):
        """ Make settings available to the template """
        context = super(GallerySettingsMixin, self).get_context_data(**kwargs)
        context['logo_path'] = settings.GALLERY_LOGO_PATH
        context['gallery_title'] = settings.GALLERY_TITLE
        context['hdpi_factor'] = settings.GALLERY_HDPI_FACTOR
        context['image_margin'] = settings.GALLERY_IMAGE_MARGIN
        context['footer_info'] = settings.GALLERY_FOOTER_INFO
        context['footer_email'] = settings.GALLERY_FOOTER_EMAIL
        context['theme_css_path'] = static(
            'gallery/css/themes/{}.css'.format(settings.GALLERY_THEME_COLOR))

        return context


class ImageView(GallerySettingsMixin, DetailView):
    model = Image

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data(**kwargs)
        context['album_images'] = []
        context['apk'] = self.kwargs.get('apk')

        context['next_image'] = None
        context['previous_image'] = None

        # If there is an album in the context, look up the images in it
        if context['apk']:
            context['album'] = Album.objects.get(pk=context['apk'])
            images = context['album'].images.all()
            album_images = sorted(images, key=lambda i: i.date_taken)
            context['album_images'] = album_images
            for i in range(len(album_images)):
                if self.object.pk == album_images[i].pk:
                    if i > 0:
                        context['previous_image'] = album_images[i - 1]
                    if i < len(album_images) - 1:
                        context['next_image'] = album_images[i + 1]
        else:
            # Look for albums this image appears in
            context['albums'] = self.object.image_albums.all()

        return context


class ImageList(GallerySettingsMixin, ListView):
    model = Image

    def get_queryset(self):
        # Order by newest first
        return super(ImageList, self).get_queryset().order_by('-pk')


class ImageCreate(GallerySettingsMixin, LoginRequiredMixin, FormView):
    """ Embedded drag and drop image upload"""
    login_url = '/admin/login/'
    form_class = ImageCreateForm
    template_name = 'gallery/image_upload.html'

    def form_valid(self, form):
        """ Bulk create images based on form data """
        image_data = form.files.getlist('data')
        for data in image_data:
            image = Image.objects.create(data=data)
            image.image_albums.add(form.data['apk'])
        messages.success(self.request, "Images added successfully")
        return super().form_valid(form)

    def get_success_url(self):
        next_url = self.request.POST.get('next')
        return_url = reverse('gallery:image_list')
        if next_url:
            return_url = next_url
        return return_url

    def form_invalid(self, form):
        response = super().form_invalid(form)
        next_url = self.request.POST.get('next')
        if next_url:
            # TODO: Preserve error message
            return redirect(next_url)
        else:
            return response


class AlbumView(GallerySettingsMixin, DetailView):
    model = Album

    def get_queryset(self):
        album = super(AlbumView, self).get_queryset()
        return album

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        images = context['album'].images.all()
        context['images'] = sorted(images, key=lambda i: i.date_taken)
        return context


class AlbumList(GallerySettingsMixin, ListView):
    model = Album
    template_name = 'gallery/album_list.html'
