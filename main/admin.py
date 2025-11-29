from django.contrib import admin
from django.utils.html import format_html
from .models import ContactSubmission, Project, ProjectGalleryImage

class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    fields = ['image', 'caption', 'order']
    ordering = ['order']

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'submitted_at']
    list_filter = ['subject', 'submitted_at']
    search_fields = ['name', 'email', 'company']
    readonly_fields = ['name', 'email', 'phone', 'company', 'subject', 'message', 'submitted_at']
    list_per_page = 20
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'client_name', 'category', 'year', 'is_featured', 'created_at']
    list_filter = ['category', 'is_featured', 'year', 'created_at']
    search_fields = ['title', 'client_name', 'industry']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectGalleryImageInline]
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'tagline', 
                'client_name', 'industry', 'category',
                'services', 'year', 'website_url'
            )
        }),
        ('Images', {
            'fields': ('featured_image',),
            'classes': ('collapse',)
        }),
        ('Project Details', {
            'fields': ('challenge', 'solution', 'results'),
            'classes': ('collapse',)
        }),
        ('Testimonial', {
            'fields': ('testimonial', 'testimonial_author', 'testimonial_position'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('is_featured',)
        })
    )

@admin.register(ProjectGalleryImage)
class ProjectGalleryImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order']
    list_filter = ['project']
    search_fields = ['project__title', 'caption']
    list_editable = ['order']