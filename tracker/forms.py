from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PushupEntry


class SignUpForm(UserCreationForm):
    """Form for user registration."""
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class PushupEntryForm(forms.ModelForm):
    """Form for adding/editing pushup entries."""
    
    class Meta:
        model = PushupEntry
        fields = ['date', 'count', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set default date to today
        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()

    def clean_date(self):
        """Validate that regular users can only enter today's date."""
        date = self.cleaned_data.get('date')
        today = timezone.now().date()
        
        # Allow admins and staff to enter any date
        if self.user and (self.user.is_staff or self.user.is_superuser):
            return date
        
        # Regular users can only enter today's date
        if date != today:
            raise forms.ValidationError(
                f"You can only log pushups for today's date ({today}). "
                "Please contact an admin if you need to add historical data."
            )
        
        return date

    def clean_count(self):
        """Validate that count is positive."""
        count = self.cleaned_data.get('count')
        if count and count < 1:
            raise forms.ValidationError("Count must be at least 1.")
        return count

