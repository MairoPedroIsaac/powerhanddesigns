# main/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, ContactSubmission, CollectiveApplication
from .forms import ContactForm, CollectiveApplicationForm


def home_view(request):
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    return render(request, 'home.html', {'featured_projects': featured_projects})


def about(request):
    return render(request, 'about.html')


def solutions(request):
    return render(request, 'solutions.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            contact_submission = form.save()
            
            # Optional: Send email notification
            try:
                send_mail(
                    f'New Contact Form Submission: {contact_submission.get_subject_display()}',
                    f'''
                    Name: {contact_submission.name}
                    Email: {contact_submission.email}
                    Phone: {contact_submission.phone}
                    Company: {contact_submission.company}
                    Subject: {contact_submission.get_subject_display()}
                    Message: {contact_submission.message}
                    ''',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                # Log error but don't break the form submission
                print(f"Email sending failed: {e}")
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return render(request, 'contact.html', {'form': ContactForm()})
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {
        'form': form,
        'calendly_url': 'https://calendly.com/your-username'
    })


def portfolio_view(request):
    projects = Project.objects.all()
    featured_projects = Project.objects.filter(is_featured=True)
    
    # Get unique categories for filtering
    categories = Project.CATEGORY_CHOICES  
    
    context = {
        'projects': projects,
        'featured_projects': featured_projects,
        'categories': categories,
    }
    return render(request, 'portfolio.html', context)


def portfolio_detail_view(request, slug):
    project = get_object_or_404(Project, slug=slug)
    gallery_images = project.gallery_images.all()
    
    # Get related projects (same category)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'gallery_images': gallery_images,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio_detail.html', context)


def collective(request):
    if request.method == 'POST':
        form = CollectiveApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'collective.html', {'form': CollectiveApplicationForm(), 'submitted': True})
        else:
            return render(request, 'collective.html', {'form': form, 'submitted': False})
    else:
        form = CollectiveApplicationForm()

    return render(request, 'collective.html', {'form': form, 'submitted': False})