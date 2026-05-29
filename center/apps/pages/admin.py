from django.contrib import admin
from .models import StaticPage
from ckeditor_uploader.widgets import CKEditorUploadingWidget

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'is_active']
    list_filter = ['page_type', 'is_active']

