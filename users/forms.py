from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email Address",
                                widget=forms.EmailInput(attrs={"class": "form-control shadow-none rounded-4"}))
    password = forms.CharField(label="Password", max_length=100,
                               widget=forms.PasswordInput(attrs={"class": "form-control shadow-none rounded-4"}))
