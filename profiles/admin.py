from django.contrib import admin
from .models import UserProfile, Project, SavedPDFDocument, CategoryFollow

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_email',)
    search_fields = ('user', 'bio', 'gravatar_email', 'twitter', 'stackoverflow', 'facebook', 'website', 'receive_email')


class SavedPDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'pdfdocument', 'saved_at')
    date_hierarchy = 'saved_at'

class CategoryFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'followed_at')
    date_hierarchy = 'followed_at'

class ProjectAdmin(admin.ModelAdmin):
    list_display=('title', 'user', )
    search_fields = ['title', 'description', 'url', 'source_url']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(SavedPDFDocument, SavedPDFDocumentAdmin)
admin.site.register(CategoryFollow, CategoryFollowAdmin)
