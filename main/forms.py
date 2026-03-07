from django import forms
from .models import ContactSubmission, CollectiveApplication


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'company', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'your@email.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '+1 (234) 567-8900'
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Your Company (Optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control form-control-lg'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Tell us about your project...',
                'rows': 5
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['phone'].required = True
        self.fields['subject'].required = True
        self.fields['message'].required = True

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) < 10:
            raise forms.ValidationError("Please enter a valid phone number.")
        return phone


class CollectiveApplicationForm(forms.ModelForm):
    class Meta:
        model = CollectiveApplication
        fields = ['full_name', 'email', 'age', 'primary_skill', 'why_join', 'sample_work', 'portfolio_link']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'apply-input',
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'apply-input',
                'placeholder': 'you@email.com',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'apply-input',
                'placeholder': 'Your age',
                'min': 13,
                'max': 30,
            }),
            'primary_skill': forms.TextInput(attrs={
                'class': 'apply-input',
                'placeholder': 'e.g. Brand Design, Copywriting, Motion',
            }),
            'why_join': forms.Textarea(attrs={
                'class': 'apply-input apply-textarea',
                'placeholder': 'Tell us what drives you...',
            }),
            'sample_work': forms.ClearableFileInput(attrs={
                'id': 'portfolioFile',
                'accept': '.pdf,.jpg,.jpeg,.png',
                'style': 'display:none',
            }),
            'portfolio_link': forms.URLInput(attrs={
                'class': 'apply-input',
                'placeholder': 'https://yourportfolio.com',
            }),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 13 or age > 30:
            raise forms.ValidationError("Age must be between 13 and 30.")
        return age

    def clean(self):
        cleaned_data = super().clean()
        sample_work = cleaned_data.get('sample_work')
        portfolio_link = cleaned_data.get('portfolio_link')
        if not sample_work and not portfolio_link:
            raise forms.ValidationError("Please upload a sample work file OR provide a portfolio link.")
        return cleaned_data