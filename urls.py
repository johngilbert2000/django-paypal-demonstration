""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include


from polidoboards.views import home_view, payment_done, payment_cancel, shipping_view, review_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    url(r'^paypal/', include('paypal.standard.ipn.urls')), # you can make this url harder to guess
    path('payment_done/', payment_done, name='payment_done'),
    path('payment_cancel/', payment_cancel, name='payment_cancel'),
    path('shipping/',shipping_view, name='shipping'),
    path('review/', review_view, name='review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
