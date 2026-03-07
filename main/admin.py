from django.contrib import admin
from django.utils.html import format_html
from .models import ContactSubmission, Project, ProjectGalleryImage, CollectiveApplication


class ProjectGalleryImageInline(admin.TabularInline):
    model = ProjectGalleryImage
    extra = 1
    fields = ['image', 'image_preview', 'caption', 'order']
    readonly_fields = ['image_preview']
    ordering = ['order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


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
    
    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.featured_image.url)
        return "-"
    image_preview.short_description = "Featured Image Preview"
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title', 'slug', 'tagline', 
                'client_name', 'industry', 'category',
                'services', 'year', 'website_url'
            )
        }),
        ('Featured Image', {
            'fields': ('featured_image', 'image_preview'),
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
    readonly_fields = ['image_preview']


@admin.register(ProjectGalleryImage)
class ProjectGalleryImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order', 'image_preview']
    list_filter = ['project']
    search_fields = ['project__title', 'caption']
    list_editable = ['order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(CollectiveApplication)
class CollectiveApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'age', 'primary_skill', 'has_file', 'has_link', 'submitted_at']
    list_filter = ['primary_skill', 'submitted_at']
    search_fields = ['full_name', 'email', 'primary_skill']
    readonly_fields = ['full_name', 'email', 'age', 'primary_skill', 'why_join', 'sample_work', 'portfolio_link', 'submitted_at']
    list_per_page = 20

    def has_file(self, obj):
        return bool(obj.sample_work)
    has_file.boolean = True
    has_file.short_description = 'File Uploaded'

    def has_link(self, obj):
        return bool(obj.portfolio_link)
    has_link.boolean = True
    has_link.short_description = 'Portfolio Link'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False