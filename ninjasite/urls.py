from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from posts import views

from gallery.views import ImageView, ImageList, AlbumView, AlbumList, ImageCreate
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from posts.views import (
    index,
    search,
    post_list,
    post_detail,
    post_create,
    post_update,
    post_delete,
    IndexView,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    MapView,
    interactivemap,
    SocialmediaView,
    GalleryView,
    ContactView
)
from marketing.views import email_list_signup

app_name = 'gallery'
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index),
    path('', IndexView.as_view(), name='home'),
    # path('blog/', post_list, name='post-list'),
    path('blog/', PostListView.as_view(), name='post-list'),
    # path interactive map/
    path('interactivemap/', MapView.as_view(), name='interactive-map'),
    # Social Media
    path('socialmedia/', SocialmediaView.as_view(), name='social-media'),
    path('search/', search, name='search'),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    # path('create/', post_create, name='post-create'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    # path('post/<id>/', post_detail, name='post-detail'),
    path('post/<pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/<id>/update/', post_update, name='post-update'),
    path('post/<pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<id>/delete/', post_delete, name='post-delete'),
    path('post/<pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('tinymce/', include('tinymce.urls')),
    path('accounts/', include('allauth.urls')),
    # GalleryDisplay
    path('gallerydisplay/', GalleryView.as_view(), name='gallery-display'),
    # Contact Me
    path('contact/', ContactView.as_view(), name='contact-me'),
    # GalleryDisplay
    path('gallery/', include('gallery.urls')),
    path('', AlbumList.as_view(), name='album_list'),
    path('images/', ImageList.as_view(), name='image_list'),
    path('image/<int:pk>/<slug>', ImageView.as_view(), name='image_detail'),
    path('upload/', ImageCreate.as_view(), name='image_upload'),
    path('album/<int:pk>/<slug>/', AlbumView.as_view(), name='album_detail'),
    path('album/<int:apk>/<int:pk>/<slug>',
         ImageView.as_view(), name='album_image_detail')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
