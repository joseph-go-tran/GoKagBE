from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("", views.api_home),
    path("v1/", include("api.routes")),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
