from django import forms
from video.models import Product, Video

validity_choices = [
    ('1', '1 day'),
    ('7', '7 days'),
    ('30', '1 month'),
    ('60', '2 months'),
    ('365', '1 year'),
    ('730', '2 years'),
    ('Unlimited', 'Unlimited')
]

STATUS_CHOICES = [
    ("DEACTIVATED", "DEACTIVATED"),
    ("REVOKED", "REVOKED")
]


class EditKeyForm(forms.Form):
    validity = forms.ChoiceField(
        choices=validity_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}))
    watermark = forms.ChoiceField(
        choices=[('Phone Number', 'Phone Number'), ('Serial Key', 'Serial Key'), ('Username', 'Username'),
                 ('Name', 'Name')], required=True,
        widget=forms.Select(attrs={'class': 'form-control watermark-select shadow-none rounded-0 mb-2'}))
    videos = forms.MultipleChoiceField(
        label='Access Status',
        required=False,
        choices=[('all', 'All Videos')],
        initial='all',
        widget=forms.SelectMultiple(attrs={'class': 'form-control shadow-none rounded-0 mb-2 videos-selector'}))
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}))
    second_screen = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0 mt-3 mb-2'}))


class GenerateKeyForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(), required=True,
        widget=forms.Select(attrs={'class': 'form-control products-select shadow-none rounded-0 mb-2'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        max_value=1000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}))
    validity = forms.ChoiceField(
        choices=validity_choices,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}))
    watermark = forms.ChoiceField(
       choices=[('Phone Number', 'Phone Number'), ('Serial Key', 'Serial Key'), ('Username', 'Username'),
                ('Name', 'Name')], required=True,
        widget=forms.Select(attrs={'class': 'form-control watermark-select shadow-none rounded-0 mb-2'}))
    videos = forms.MultipleChoiceField(
        label='Access Status',
        required=False,
        choices=[('all', 'All Videos')],
        initial='all',
        widget=forms.SelectMultiple(attrs={'class': 'form-control shadow-none rounded-0 mb-2 videos-selector'}))
    second_screen = forms.BooleanField(
        label='Allow Second Screen',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'shadow-none rounded-0 mt-3 mb-2',
                                          'checked': 'checked'}))


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'title', 'short_description', 'long_description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}),
            'title': forms.TextInput(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}),
            'long_description': forms.Textarea(attrs={'class': 'form-control shadow-none rounded-0 mb-2'}),
        }
