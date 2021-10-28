from django.urls import path

from . import views


urlpatterns = [
    path('raw_mini', views.raw_mini),
    path('raw_tsi', views.raw_tsi),
]
