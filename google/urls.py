from django.urls import path, include
from . import views

app_name = "google"


urlpatterns = [
    path("", views.SearchView.as_view(), name="search_results"),
]
