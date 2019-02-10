"""The forms used in views.py for a django-paypal demonstration.
Written by John Gilbert (https://github.com/johngilbert2000)
Released to Public Domain. Use as you like."""

from django import forms
from .models import QuoteRequest, ShippingDetail

# These item sizes / types are choice fields that can be added to your forms
ITEM_SIZES = (
    ('Any','Any'),
    ('Small','Small'),
    ('Medium','Medium'),
    ('Large', 'Large'),
)

ITEM_TYPES = (
    ('Any', 'Any'),
)

# The Contact Form (used in home_view in views.py)
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='')
    email = forms.EmailField(label='')
    phone = forms.CharField(max_length=15, label='', required=False)
    website = forms.CharField(label='', max_length=100, required=False)
    message = forms.CharField(widget=forms.Textarea, label='')

    name.widget.attrs.update({'placeholder': 'Your Name'})
    email.widget.attrs.update({'placeholder': 'Your Email Address'})
    phone.widget.attrs.update({'placeholder': 'Your Phone Number (optional)'})
    website.widget.attrs.update({'placeholder': 'Your Website (optional)'})
    message.widget.attrs.update({'placeholder': 'Type your message here...'})

# The Quote Request Form (used in home_view in views.py)
class GetQuoteForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='')
    email = forms.EmailField(label='')
    phone = forms.CharField(max_length=15, label='', required=False)
    image = forms.ImageField(required=False)
    item_type = forms.ChoiceField(choices=ITEM_TYPES)
    size = forms.ChoiceField(choices=ITEM_SIZES, required=False)
    message = forms.CharField(widget=forms.Textarea, label='')

    name.widget.attrs.update({'placeholder': 'Your Name'})
    email.widget.attrs.update({'placeholder': 'Your Email Address'})
    phone.widget.attrs.update({'placeholder': 'Your Phone Number (optional)'})
    message.widget.attrs.update({'placeholder': 'Type any notes here...'})

    image.label = "Upload Image:"
    item_type.label = "Select Item Type:"
    size.label = "Select Size:"

    class Meta:
        model = QuoteRequest
        fields = ('name', 'email', 'phone', 'image', 'item_type', 'size', 'message',)


# The Shipping Details form (used in shipping_view in forms.py)
class ShippingDetailsForm(forms.ModelForm):
    name = forms.CharField(max_length=20, label='')
    email = forms.EmailField(label='')
    phone = forms.CharField(max_length=15, label='', required=False)
    street = forms.CharField(max_length=100, label='')
    city = forms.CharField(max_length=30, label='')
    state = forms.CharField(max_length=20, label='')
    zip = forms.CharField(max_length=10, label='')
    country = forms.CharField(max_length=10, label='', required=False)

    name.widget.attrs.update({'placeholder': 'Your Name'})
    email.widget.attrs.update({'placeholder': 'Email'})
    phone.widget.attrs.update({'placeholder': 'Phone Number (Optional)'})
    street.widget.attrs.update({'placeholder': 'Street'})
    city.widget.attrs.update({'placeholder': 'City'})
    state.widget.attrs.update({'placeholder': 'State'})
    zip.widget.attrs.update({'placeholder': 'Zip'})
    country.widget.attrs.update({'placeholder': 'Country'})

    class Meta:
        model = ShippingDetail
        fields = ('name','email','phone','street','city','state','zip','country',)
