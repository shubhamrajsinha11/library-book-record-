"""
URL configuration for slms_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home),
    path('home', home),
    path('readers/', students_tab, name='students_tab'),
    path('students/add/', save_student, name='save_student'),
    path('books/', books_tab, name='books_tab'),
    path('toggle_bag/<int:book_id>/', toggle_bag, name='toggle_bag'),
    path('bag/', bag_view, name='bag_view'),
    path('clear-bag/', clear_bag, name='clear_bag'),
    path('bag/search/', bag_list, name='bag_search'),
    path('get_student/', get_student_details, name='get_student'),
    path('checkout/', checkout, name='checkout'),
    path('returns/', returns, name='returns'),
    path('toggle_return/<int:rental_id>/', toggle_return, name='toggle_return'),
]




if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)