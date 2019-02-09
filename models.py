"""The models used in views.py for a django-paypal demonstration.
Written by John Gilbert (https://github.com/johngilbert2000)
Released to Public Domain. Use as you like."""

from django.db import models
from singleton import SingletonModel # included singleton.py from Senko Rasic in the project to use a singleton model (https://gist.github.com/senko/5028413)


# These item sizes / types are choice fields that can be added to your Model forms
ITEM_SIZES = (
    ('Any','Any'),
    ('Small','Small'),
    ('Medium','Medium'),
    ('Large', 'Large'),
)

ITEM_TYPES = (
    ('Any', 'Any'),
)


# Site Description
class SiteDescription(SingletonModel):
    who_we_are = models.TextField(verbose_name='Who We Are')
    what_we_do = models.TextField(verbose_name='What We Do')
    facebook = models.CharField(max_length=50, default='https://www.facebook.com/your-default-facebook-link/')
    twitter = models.CharField(max_length=50, default='https://twitter.com/your-default-twitter-link')
    instagram = models.CharField(max_length=50, default='https://www.instagram.com/your-default-instagram-link/')

    # Used for admin page
    description = models.TextField(default='Edit Description', editable=False)

    # Custom string name
    def __str__(self):
        return "Who We Are & What We Do"

    # Change the model display name for Django Admin
    class Meta:
        verbose_name_plural = 'Site Description'


# Artists
class Artist(models.Model):
    image = models.ImageField(upload_to='photo', verbose_name='Main Image')
    name = models.CharField(max_length=50)
    instagram = models.CharField(max_length=150, blank=True)
    twitter = models.CharField(max_length=150, blank=True)
    facebook = models.CharField(max_length=150, blank=True)
    about = models.TextField(max_length=500)
    art_style = models.TextField(max_length=500, verbose_name='Art Style')
    image1 = models.ImageField(upload_to='photo', blank=True, verbose_name='Additional Image 1')
    image2 = models.ImageField(upload_to='photo', blank=True, verbose_name='Additional Image 2')
    image3 = models.ImageField(upload_to='photo', blank=True, verbose_name='Additional Image 3')
    image4 = models.ImageField(upload_to='photo', blank=True, verbose_name='Additional Image 4')

    # Custom string name
    def __str__(self):
        return self.name




# Artist Choices for Gallery
ARTIST_CHOICES = [(x.name, x.name) for x in Artist.objects.all()]

# Gallery
class GalleryItem(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='photo')
    artist = models.CharField(max_length=20,choices=ARTIST_CHOICES, blank=True)

    updated = models.DateTimeField(auto_now=True, null=True)

    # Custom string name
    def __str__(self):
        return self.title

    # Change the model display name for Django Admin
    class Meta:
        verbose_name_plural = 'Gallery'


# Store
class StoreItem(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='photo')
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0.00)
    quantity = models.IntegerField(default=int(1))
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, blank=True, verbose_name='Item Type')
    size = models.CharField(max_length=20, choices=ITEM_SIZES, blank=True)
    about = models.TextField(max_length=200, blank=True, null=True)
    sold = models.BooleanField(default=False, verbose_name='Sold Out') # Sold Out
    show_in_gallery = models.BooleanField(default=False, verbose_name='Show In Gallery')
    buyer_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Recent Buyer Name')
    amount_paid = models.CharField(max_length=10,blank=True, null=True, verbose_name='Recent Amount Paid')
    buyer_currency = models.CharField(max_length=5,blank=True, null=True, verbose_name='Recent Buyer Currency')
    invoice = models.CharField(max_length=50, default='', blank=True, null=True, verbose_name='Invoice(s)')
    buyer_email = models.CharField(max_length=50, blank=True, null=True, verbose_name='Recent Buyer Email')

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # Custom string name for StoreItem
    def __str__(self):
        if self.price and (self.sold == True):
            return self.title + " - Price: $" + str(self.price) + " - Sold Out! "
        elif self.price:
            return self.title + " - Price: $" + str(self.price)
        else:
            return self.title

    # Makes StoreItem's sold field dependent on its quantity field
    def save(self,*args, **kwargs):
        if self.quantity == 0:
            self.sold = True
        elif self.quantity < 0:
            self.quantity = 0
            self.sold = True
        else:
            self.sold = False
        super(StoreItem, self).save(*args, **kwargs) # Calls the original save method

    # Change the model display name for Django Admin
    class Meta:
        verbose_name_plural = 'Store'


# Quote Requests
class QuoteRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(blank=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, verbose_name='Item Type')
    size = models.CharField(max_length=20, choices=ITEM_SIZES, blank=True)
    message = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    purchased = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    # Custom string name
    def __str__(self):
        return self.name

    # Change the model display name for Django Admin
    class Meta:
        verbose_name_plural = 'Quote Requests'

# Shipping Details and Purchased Item Information
class ShippingDetail(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(default='', verbose_name='Preferred Email')
    paypal_email = models.EmailField(default='', blank=True, verbose_name='Email Used At PayPal')
    phone = models.CharField(max_length=15, blank=True, null=True)
    desired_item = models.CharField(max_length=30, blank=True, null=True, verbose_name='Item')
    invoice = models.CharField(max_length=15,blank=True, null=True)
    paid = models.BooleanField(default=False)
    shipped = models.BooleanField(default=False)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zip = models.CharField(max_length=10)
    country = models.CharField(max_length=10, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='Transaction Time (GMT)')

    # Custom string name
    def __str__(self):
        return self.name

    # Change the model display name for Django Admin
    class Meta:
        verbose_name_plural = 'Shipping Details'

