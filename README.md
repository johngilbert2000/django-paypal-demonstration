# Django-Paypal Demonstration
This is sample code from a django project using django-paypal. This is to be used as a reference for implementing django-paypal IPN transactions with django. Most of the code for this project can be found in views.py.

In this implementation, after a user selects an item to purchase and fills out a form that saves shipping information, the selected item's information (such as item name, price, invoice, etc.) is pulled from an object stored in the database via django, and then a paypal Buy Now button is created using this information with django-paypal. The Buy Now button is then used to redirect a user to Paypal's website, where the user can complete a transaction for the item selected (using either a Paypal account or credit card). Upon completing a successful transaction, the database is then updated to indicate which item was purchased, as well as how many of those items are left in stock.

Versions Used:
- Django 2.1.4
- django-paypal 0.5.0 

See also:
- Django-Paypal IPN: https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
- ngrok: https://ngrok.com/ (for testing paypal transactions on your site)
- Django Singleton Model: https://gist.github.com/senko/5028413
