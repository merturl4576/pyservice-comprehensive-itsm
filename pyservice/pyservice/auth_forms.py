from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CompanyAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form that includes company_name.
    """
    company_name = forms.CharField(
        label="Company Name",
        max_length=200,
        required=False,  # Super admin might not need it
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Enter your company name'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        company_name = self.cleaned_data.get('company_name')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
                company_name=company_name
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
