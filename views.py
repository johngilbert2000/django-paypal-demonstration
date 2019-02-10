"""A demonstration of using django-paypal in a django project.
Written by John Gilbert (https://github.com/johngilbert2000)
Released to Public Domain. Use as you like."""

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from decimal import Decimal
from django.contrib import messages

from .forms import ContactForm, GetQuoteForm, ShippingDetailsForm
from .models import SiteDescription, GalleryItem, StoreItem, Artist, ShippingDetail

from slugify import slugify
from random import randint


def home_view(request):
    """The Home Page, which includes a Site Description, a Contact Form, a Quote Request Form,
    a list of Company Members, a list of Store Items, and a list of Gallery Items"""


    # Initiates the two forms
    form = ContactForm(request.POST or None)
    getquote = GetQuoteForm(request.POST or None, request.FILES or None)

    # Session variables were used to temporarily store information about a selected item in the store
    # The following code resets these variables each time the home page is visited.
    request.session['item_name'] = 'no-item-selected'
    request.session['item_id'] = 'no-item-selected'
    request.session['amount'] = 'no-item-selected'
    request.session['invoice'] = 'no-item-selected'
    request.session['shipping_status'] = 'incomplete'
    request.session['ship_id'] = 'no-shipping-id'


    # The following code sends an email each time the two forms (Contact Form and the Quote Request Form) are used
    # The email address and email password that was used to generate emails is stored in settings.py with the variable EMAIL_HOST_USER
    # Note that if you use gmail, your email account's security settings must be altered to allow your site to access your email
    if request.method == 'POST':
        # The Contact Form
        if request.POST['form-type'] == u"contact-form":
            if form.is_valid():
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                website = form.cleaned_data['website']
                message = form.cleaned_data['message']

                subject = 'Contact Message [Automated]'
                from_email = settings.EMAIL_HOST_USER
                to_email = [from_email]
                contact_message = """
                Name: %s
                Email: %s
                Phone: %s
                Website: %s
                Message: %s"""%(name, email, phone, website, message)

                try:
                    if 'contactform' in request.POST:
                        send_mail(subject, contact_message, from_email, to_email, fail_silently=False)

                        msg = """Thank you for contacting us. We will review your message and get back to you.
                        
            The following message was sent to us:
            """
                        msg += contact_message
                        to_email = [email]
                        send_mail(subject, msg, from_email, to_email, fail_silently=True)

                except BadHeaderError:
                    return redirect('home')
                return redirect('home')

        # The Quote Request Form
        elif request.POST['form-type'] == u"quote-form":
            if getquote.is_valid():

                quote_name = getquote.cleaned_data['name']
                quote_email = getquote.cleaned_data['email']
                quote_phone = getquote.cleaned_data['phone']

                quote_itemtype = getquote.cleaned_data['item_type']
                quote_size = getquote.cleaned_data['size']
                quote_message = getquote.cleaned_data['message']
                getquote.save()

                quote_subject = 'Quote Request [Automated]'
                quote_from_email = settings.EMAIL_HOST_USER
                quote_to_email = [quote_email, quote_from_email]

                quote_contact_message = """
                Thank you for requesting a quote with us. We will get back to you soon with information regarding your desired item.
                
                The following message was sent to us, along with any images you uploaded:
                
                    Name: %s
                    Email: %s
                    Phone: %s
                    Item Type: %s
                    Size: %s
                    Message: %s
                """ % (quote_name, quote_email, quote_phone, quote_itemtype, quote_size, quote_message)


                try:

                    imgmail = EmailMessage(
                        quote_subject,
                        quote_contact_message,
                        quote_from_email,
                        quote_to_email,
                        attachments=[],
                    )
                    imgmail.send()

                except BadHeaderError:
                    return redirect('home')

                return redirect('home')

        # The following code stores information about a store item if a purchase button gets pressed for that item
        elif request.POST['form-type'] == u"purchase":

            # form-id is used in the button html to indicate which item the button corresponds to
            desired_item = StoreItem.objects.get(id=str(request.POST['form-id']))

            # Session Variables are used to temporarily save the selected item's information
            request.session['item_name'] = str(desired_item.title)
            request.session['item_id'] = str(request.POST['form-id'])
            request.session['amount'] = str(desired_item.price)
            # An invoice is generated, which will eventually be used in the django-paypal form
            # This invoice is used by paypal to notify your database of a successful purchase
            # Hence, it is important to store the item id, or other identifying information, in the invoice
            request.session['invoice'] = str(request.POST['form-id']) + 'z' + str(randint(1,100))

            # After the purchase button is pressed, this redirects the user to a page to collect their shipping information
            return redirect('shipping')



    # The Singleton Model (see singleton.py at https://gist.github.com/senko/5028413 and models.py) was used in this project to store the Site Description as an object in the database.
    # This allows only one Site Description object, which gets overwritten each time a new object is created using the Site Description model.
    # As it is possible for 0 Site Description items to exist, a try block is used to set a default site description.
    try:
        obj = SiteDescription.objects.all().first()
        description1 = obj.who_we_are
        description2 = obj.what_we_do
        facebook_url = obj.facebook
        twitter_url = obj.twitter
        instagram_url = obj.instagram
    except:
        description1 = '[ Area Under Construction: Please Come Back Later ]'
        description2 = '[ Area Under Construction: Please Come Back Later ]'
        facebook_url = 'https://www.facebook.com/your-default-facebook-link/'
        twitter_url = 'https://twitter.com/your-default-twitter-link'
        instagram_url = 'https://www.instagram.com/your-default-instagram-link/'


    my_context = {
        'who_we_are': description1,
        'what_we_do': description2,
        'facebook_url': facebook_url,
        'instagram_url': instagram_url,
        'twitter_url': twitter_url,
        'gallery': GalleryItem.objects.all(),
        'store': StoreItem.objects.all(),
        'store_available': StoreItem.objects.filter(sold=False), # sold=True indicates that this store item is completely sold out in your store
        'artists': Artist.objects.all(),
        'form': form,
        'getquote': getquote,
    }
    return render(request, "home.html", my_context)


def shipping_view(request):
    """This page collects shipping information from the user and stores it in the database (see ShippingDetails in forms.py).
    This page is accessed after an item is selected for purchase in the Home Page"""

    form = ShippingDetailsForm(request.POST or None)

    # Makes shipping.html unusable if no item is selected
    if (request.session['invoice'] == 'no-item-selected') or (request.session['invoice'] == None):
        return redirect('home')

    if request.method == 'POST':
        if form.is_valid():

            # Saves shipping information about the user using the ShippingDetails form,
            # and saves information about the item selected to be purchased (item name and invoice).
            to_save = form.save(commit=False)
            if request.session['invoice']:
                to_save.invoice = request.session['invoice']
            if request.session['item_name']:
                to_save.desired_item = request.session['item_name']

            to_save.save()

            # Stores the id of the ShippingDetails object in the invoice.
            # This way, when the paypal notifies your site of a successful purchase,
            # the ShippingDetails object can be easily updated to indicate that this user paid for the selected item.
            if to_save.id:
                request.session['ship_id'] = str(to_save.id)
                request.session['invoice'] = str(request.session['invoice']) + 'c' + str(request.session['ship_id'])
                to_save.invoice = request.session['invoice']
                to_save.save()

            request.session['shipping_status'] = 'complete'

            # Redirects the user to a review page, where they can be redirected to paypal to purchase their item
            return redirect('review')

    context = {
        'form': form,
    }

    return render(request, "shipping.html", context)


def review_view(request):
    """This page lets the user review the selected store item.
    This page contains a paypal button that is linked to the store item's name, invoice, and price information.
    When the user is ready, the user can click on paypal's Buy Now to proceed to paypal to make the transaction."""

    # PayPal forms (i.e., info for paypal Buy Now buttons)
    # By using an array to store paypal forms, multiple different Buy Now buttons could be added to one page, should you decide to do so.
    pp_forms = []

    # Makes review.html unusable if no item is selected
    if (request.session['invoice'] == 'no-item-selected') or (request.session['invoice'] == None):
        return redirect('home')

    # Session Variables are used to let the user double check important information about the selected item
    item_amount = request.session['amount']
    item_name = request.session['item_name']
    item_invoice = request.session['invoice']

    # Ensures that the shipping information was completed prior to item purchase
    if request.session['shipping_status']:
        shipping_status = request.session['shipping_status']
    else:
        shipping_status = 'incomplete'
        redirect('shipping')


    if shipping_status == 'complete':

        # This dictionary stores information that paypal uses to generate the Buy Now button
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL, # Your company's paypal account email can be stored in settings.py
            'amount': item_amount,
            'item_name': item_name,
            "currency_code": "USD",
            'invoice': item_invoice,
            'notify_url': request.build_absolute_uri(reverse('paypal-ipn')),  # the url where info gets stored
            'return': request.build_absolute_uri(reverse('payment_done')),  # return-view
            'cancel_return': request.build_absolute_uri(reverse('payment_cancel')),  # cancel-view
            # 'custom': "premium_plan",  # Custom command to correlate to some function later (optional)
        }
        pp_forms += [PayPalPaymentsForm(initial=paypal_dict)]

    context = {
        'item_amount': item_amount,
        'item_name': item_name,
        'item_invoice':item_invoice,
        'pp_forms': pp_forms,
        'shipping': ShippingDetail.objects.filter(invoice=item_invoice),
        'item': StoreItem.objects.filter(title=item_name),
    }

    return render(request, "review.html", context)


@csrf_exempt
def payment_done(request):
    """This code gets run whenever a user successfully completes a transaction and opts to return to your site.
    Session variables can be reset, and the corresponding Shipping Detail object can be updated
    to indicate that a particular user completed a successful purchase."""


    # Payment Successful: ensure shipping detail displays paid = True
    # Note that this is also done in the paypal_notification function below in views.py
    if request.session['ship_id']:
        shipping_obj = get_object_or_404(ShippingDetail, id=request.session['ship_id'])
        shipping_obj.paid = True
        shipping_obj.save()

    # Session Variables are reset
    request.session['item_name'] = 'no-item-selected'
    request.session['item_id'] = 'no-item-selected'
    request.session['amount'] = 'no-item-selected'
    request.session['invoice'] = 'no-item-selected'
    request.session['shipping_status'] = 'incomplete'

    # This can be changed to a different view if you wish to create a "Thank You for Your Purchase" page
    return redirect('home')


def payment_cancel(request):
    """This code gets run whenever a user does not complete a transaction but opts to return to your site from paypal."""

    # Session Variables are reset
    request.session['item_name'] = 'no-item-selected'
    request.session['item_id'] = 'no-item-selected'
    request.session['amount'] = 'no-item-selected'
    request.session['invoice'] = 'no-item-selected'
    request.session['shipping_status'] = 'incomplete'

    # This can be changed to a different view if you wish to include a page that asks for user feedback
    return redirect('home')


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    """This code updates objects in your database whenever paypal notifies your site of a successful transaction"""

    ipn = sender
    if ipn.payment_status == 'Completed':
        # Payment was successful

        # Obtains crucial information from the invoice that was given to paypal for this transaction
        # Note: The invoice for this site was originally generated as a string in the following format: {item id} z {random number} c {shipping id}
        # where z and c were letters arbitrarily chosen to separate the different numbers in the invoice
        itemid = str(ipn.invoice)
        itemid = itemid.split('z')
        shipid = itemid[1].split('c')
        ship_id = shipid[1]

        # Update the Store Item's Quantity and Invoices
        order = get_object_or_404(StoreItem, id=itemid[0])

        order.quantity = int(order.quantity) - 1
        if order.quantity == 0:
            order.sold = True # sold=True indicates that this store item is completely sold out in your store

        order.buyer_name = str(ipn.first_name) + ' ' + str(ipn.last_name)
        order.amount_paid = str(ipn.mc_gross)
        order.buyer_currency = str(ipn.mc_currency)

        if (order.invoice != "") and (order.invoice != None):
            order.invoice = str(ipn.invoice) + str(", ") + str(order.invoice)
        else:
            order.invoice = str(ipn.invoice)

        order.buyer_email = str(ipn.payer_email)
        order.buyer_phone = str(ipn.contact_phone)

        order.save()

        # Update the Shipping Detail to Paid
        shipping_obj = get_object_or_404(ShippingDetail, id=ship_id)
        shipping_obj.paid = True
        shipping_obj.paypal_email = str(ipn.payer_email)
        shipping_obj.save()
