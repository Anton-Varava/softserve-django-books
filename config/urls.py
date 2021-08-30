"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='books/'), name='home-page'),
    path('sign_up', user_views.UserCreateView.as_view(), name='sign-up'),
    path('sign_in', auth_views.LoginView.as_view(template_name='users/sign_in.html'), name='sign-in'),
    path('sign_out', auth_views.LogoutView.as_view(), name='sign-out'),
    path('users/', include(('users.urls', 'users'))),
    path('books/', include(('books.urls', 'books'))),
    path('authors/', include(('authors.urls', 'authors'))),
    path('api/', include(('authentication.urls', 'authentication'))),
    path('api/', include(('api.urls', 'api'))),
    path('__debug__/', include(debug_toolbar.urls)),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
