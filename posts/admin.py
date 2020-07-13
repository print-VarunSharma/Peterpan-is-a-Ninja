from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView

from gallery.models import Image, Album
from django.contrib import admin
from imagekit.admin import AdminThumbnail
import importlib
if importlib.util.find_spec('adminsortable2', 'admin'):
    from adminsortable2.admin import SortableAdminMixin
else:
    # Mock up class for mixin
    class SortableAdminMixin:
        mock = True


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)


class ImageAdmin(admin.ModelAdmin):
    admin_thumbnail = AdminThumbnail(
        image_field='data_thumbnail', template='gallery/admin/thumbnail.html')
    list_display = ('title', 'admin_thumbnail', 'date_taken', 'date_uploaded')
    list_filter = ('image_albums',)
    list_per_page = 25
    readonly_fields = ('admin_thumbnail',)


class AlbumAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('order', 'title')
    list_display_links = ('title',)
    if hasattr(SortableAdminMixin, 'mock'):
        list_editable = ('order',)
        list_display = ('title', 'order')
    filter_horizontal = ('images',)
    raw_id_fields = ('highlight',)


admin.site.unregister(Image)
admin.site.unregister(Album)
admin.site.register(Image, ImageAdmin)
admin.site.register(Album, AlbumAdmin)
