from django import forms


class GenerateKeyForm(forms.Form):
    validity_choices = [
        ('1', '1 day'),
        ('7', '7 days'),
        ('30', '1 month'),
        ('60', '2 months'),
        ('365', '1 year'),
        ('730', '2 years'),
        ('Unlimited', 'Unlimited')
    ]
    product = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none rounded-0'}))
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control shadow-none rounded-0'}))
    validity = forms.ChoiceField(
        choices=validity_choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control shadow-none rounded-0'}))
    watermark = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control shadow-none rounded-0'}))
