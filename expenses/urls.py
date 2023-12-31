"""
URL configuration for expenses project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from moneyflow.views import *
import moneyflow.urls
import users.urls

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns

i18n_urlpatterns = i18n_patterns(
    path("", include(moneyflow.urls)),
    path("kayttajatilit/", include(users.urls)),
    path("admin/", admin.site.urls),
    prefix_default_language=True,
)

normal_urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns = i18n_urlpatterns + normal_urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)