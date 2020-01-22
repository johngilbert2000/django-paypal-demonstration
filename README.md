# Django-Paypal Demonstration
This is sample code from a django project that used django-paypal. The sample code provided has been modified to give a general-purpose example of an e-commerce website that uses django-paypal, and all personal information from the original project (such as company name, email address, paypal account information, etc.) has been removed or modified in the code. This sample code is to be used primarily as a reference for implementing django-paypal IPN transactions with django, as well as to demonstrate my ability to work with django. Most of the relevant code from this project can be found in views.py, (particularly the review_view and payment_notification functions in views.py). A "Contact Form" and a "Quote Request Form" were also included in the sample code (home_view of views.py) to illustrate how other forms could be included in the same webpage or view, as well as how to generate an automated email response with those forms.

In this implementation, after a user selects an item to purchase and fills out a form that saves shipping information, the selected item's information (such as item name, price, invoice, etc.) is pulled from an object stored in the database and from user session variables, and then a paypal Buy Now button is created and displayed in review.html using this information with django-paypal. The Buy Now button is then used to redirect a user to Paypal's website, where the user can complete a transaction for the item selected. Upon completing a successful transaction, the database is then updated to indicate which item was purchased alongside the shipping information of the customer. Additionally, the quantity of that store item left in stock is also updated in the database to reflect the transaction.

**Video**: For reasons unrelated to the website, the following site was never put into production and deployed. However you can see part of video demonstration for it here:
https://www.youtube.com/watch?v=MhWF6bhqbDQ&feature=youtu.be&fbclid=IwAR0BjY4-6JoSAKF87hJKyRAy_0eqMpzpSh2DKINUoBEpOI0cyAmGJbe8xnA

Versions Used:
- Django 2.1.4
- django-paypal 0.5.0 

See also:
- Django-Paypal IPN: https://django-paypal.readthedocs.io/en/stable/standard/ipn.html
- ngrok: https://ngrok.com/ (for testing paypal transactions on your site)
- Django Singleton Model: https://gist.github.com/senko/5028413 (used to include a single Site Description object in the database)
