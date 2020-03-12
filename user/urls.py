from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from .views import AuthorViewSet, UserViewSet

router = routers.DefaultRouter()
# Note: rest_auth.urls may clash with router.urls, name paths carefully.
router.register("author", AuthorViewSet, basename="author")
router.register("admin_users", UserViewSet, basename="user")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("signup/", include("rest_auth.registration.urls")),
    path("", include("rest_auth.urls")),
    path("", include(router.urls)),
]
