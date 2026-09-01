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
    content_use_consent = forms.ChoiceField(
        choices=CollectiveApplication.CONSENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'consent-radio-input'}),
        required=True
    )

    class Meta:
        model = CollectiveApplication
        fields = [
            'full_name', 'email', 'age', 'primary_skill', 'primary_skill_other', 
            'why_join', 'portfolio_link', 
            'hunting_for', 'hunting_for_other', 'hope_to_build', 
            'challenge_writeup', 'content_use_consent'
        ]
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
            'primary_skill': forms.Select(attrs={
                'class': 'apply-input',
                'id': 'primarySkillSelect',
            }),
            'primary_skill_other': forms.TextInput(attrs={
                'class': 'apply-input',
                'placeholder': 'Please specify your skill...',
                'id': 'primarySkillOtherField',
            }),
            'why_join': forms.Textarea(attrs={
                'class': 'apply-input apply-textarea',
                'placeholder': 'Tell us what drives you...',
                'rows': 5,
            }),
            'portfolio_link': forms.TextInput(attrs={
                'class': 'apply-input',
                'placeholder': 'e.g. Behance link, Instagram handle @username, or website',
            }),
            'hunting_for': forms.Select(attrs={
                'class': 'apply-input',
                'id': 'huntingForSelect',
            }),
            'hunting_for_other': forms.TextInput(attrs={
                'class': 'apply-input',
                'placeholder': 'Please specify what you are hunting for...',
                'id': 'huntingForOtherField',
            }),
            'hope_to_build': forms.Textarea(attrs={
                'class': 'apply-input apply-textarea',
                'placeholder': 'I am hoping to build...',
                'rows': 3,
            }),
            'challenge_writeup': forms.Textarea(attrs={
                'class': 'apply-input apply-textarea',
                'placeholder': 'Write your answer here...',
                'rows': 5,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add empty labels / placeholders for select fields
        self.fields['primary_skill'].choices = [('', 'Select your primary skill...')] + list(CollectiveApplication.PRIMARY_SKILL_CHOICES)
        self.fields['hunting_for'].choices = [('', 'Select what you are hunting for...')] + list(CollectiveApplication.HUNTING_FOR_CHOICES)
        # primary_skill_other and hunting_for_other are dynamically shown, so they should not be strictly required by default in the Django field level (we validate in clean)
        self.fields['primary_skill_other'].required = False
        self.fields['hunting_for_other'].required = False
        self.fields['portfolio_link'].required = False

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 13 or age > 30:
            raise forms.ValidationError("Age must be between 13 and 30.")
        return age

    def clean(self):
        cleaned_data = super().clean()

        # Conditional other validations
        primary_skill = cleaned_data.get('primary_skill')
        primary_skill_other = cleaned_data.get('primary_skill_other')
        if primary_skill == 'Other' and not primary_skill_other:
            self.add_error('primary_skill_other', "Please specify your primary skill since you selected 'Other'.")

        hunting_for = cleaned_data.get('hunting_for')
        hunting_for_other = cleaned_data.get('hunting_for_other')
        if hunting_for == 'Other' and not hunting_for_other:
            self.add_error('hunting_for_other', "Please specify what you are hunting for since you selected 'Other'.")

        return cleaned_data