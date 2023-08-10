from django.urls import path

from .migrations import views

app_name = "polls"
urlpatterns = [
    # ex: /metacodes/
    path("", views.IndexView.as_view(), name="index"),
]

