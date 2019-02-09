# Django-Paypal Demonstration
This is sample code from a django project that used django-paypal. The sample code provided has been modified to give a general-purpose example of django-paypal, and all personal information from the original project (such as company name, email address, paypal account information, etc.) has been removed or modified. This is to be used primarily as a reference for implementing django-paypal IPN transactions with django. Most of the relevant code for from this project can be found in views.py.

In this implementation, after a user selects an item to purchase and fills out a form that saves shipping information, the selected item's information (such as item name, price, invoice, etc.) is pulled from an object stored in the database via django, and then a paypal Buy Now button is created and displayed in review.html using this information with django-paypal. The Buy Now button is then used to redirect a user to Paypal's website, where the user can complete a transaction for the item selected. Upon completing a successful transaction, the database is then updated to indicate which item was purchased alongside the shipping information of the customer. Additionally, the quantity of that store item left in stock is also updated in the database to reflect the transaction.

Versions Used:
- Django 2.1.4
- django-paypal 0.5.0 

See also:
- Django-Paypal IPN: https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
- ngrok: https://ngrok.com/ (for testing paypal transactions on your site)
- Django Singleton Model: https://gist.github.com/senko/5028413
