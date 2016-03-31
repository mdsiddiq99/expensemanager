"""expensemanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('', 
    url(r'^$', 'transactions.views.dashboard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/create/$', 'users.views.create_account'),
    url(r'^account/delete/$', 'users.views.delete_account'),
    url(r'^account/edit/$', 'users.views.edit_account'),
    url(r'^transaction/make/$', 'transactions.views.make_transaction'),
    url(r'^transaction/delete/$', 'transactions.views.delete_transaction'),
    url(r'^transaction/edit/$', 'transactions.views.edit_transaction'),
	)
