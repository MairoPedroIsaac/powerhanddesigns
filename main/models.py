from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator

class ContactSubmission(models.Model):
    SUBJECT_CHOICES = [
        ('', 'Select a service...'),
        ('brand_strategy', 'Brand Strategy'),
        ('identity_logo_design', 'Identity & Logo Design'),
        ('print_fabrication', 'Print & Fabrication'),
        ('eco_packaging', 'Eco Packaging Design'),
        ('environmental_design', 'Environmental Design'),
        ('workshops_consultations', 'Workshops & Consultations'),
        ('digital_marketing', 'Digital Marketing'),
        ('sustainable_website', 'Sustainable Website Development'),
        ('multiple_services', 'Multiple Services'),
        ('general_inquiry', 'General Inquiry'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    company = models.CharField(max_length=200, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='')
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'
    
    def __str__(self):
        return f"{self.name} - {self.get_subject_display()}"

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('branding', 'Branding'),
        ('packaging', 'Packaging'),
        ('print', 'Print Design'),
        ('environmental', 'Environmental Design'),
        ('identity', 'Identity & Logo'),
        ('strategy', 'Brand Strategy'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    tagline = models.CharField(max_length=300, help_text="Short catchy description")
    client_name = models.CharField(max_length=200)
    industry = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    services = models.TextField(help_text="Services provided (e.g., Branding, Logo Design)")
    year = models.IntegerField()
    website_url = models.URLField(blank=True, null=True)
    
    # Featured Image
    featured_image = models.ImageField(upload_to='portfolio/featured/')
    
    # Project Content
    challenge = models.TextField(help_text="Describe the challenge/problem")
    solution = models.TextField(help_text="Describe your solution")
    results = models.TextField(blank=True, help_text="Results achieved (optional)")
    
    # Testimonial (optional)
    testimonial = models.TextField(blank=True)
    testimonial_author = models.CharField(max_length=200, blank=True)
    testimonial_position = models.CharField(max_length=200, blank=True)
    
    # Meta
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

class ProjectGalleryImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.project.title} - Image {self.order}"