from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView


urlpatterns = [
    path("", include("apps.game.urls")),
    path("lotteries/", include("apps.lottery.urls")),
    path("accounts/", include("accounts.urls")),
    path('admin/', admin.site.urls)
]
