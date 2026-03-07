from django.db import models
from django.utils.text import slugify
from django.core.validators import RegexValidator


class ContactSubmission(models.Model):
    SUBJECT_CHOICES = [
        ('', 'Select a service...'),
        ('impact_brand_system', 'Impact Brand System'),
        ('brandpaw_saas', 'BrandPaw™ SaaS'),
        ('environmental_branding', 'Environmental Branding'),
        ('marketing_collateral', 'Marketing Collateral Design'),
        ('sustainable_packaging', 'Sustainable Packaging Design'),
        ('print_fabrication', 'Print & Fabrication'),
        ('digital_marketing', 'Digital Marketing'),
        ('website_development', 'Website Development'),
        ('workshops_consultations', 'Workshops & Consultations'),
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


class CollectiveApplication(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    primary_skill = models.CharField(max_length=100)
    why_join = models.TextField()
    sample_work = models.FileField(upload_to='collective/portfolios/', blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Collective Application'
        verbose_name_plural = 'Collective Applications'

    def __str__(self):
        return f"{self.full_name} — {self.primary_skill} ({self.submitted_at.strftime('%d %b %Y')})"