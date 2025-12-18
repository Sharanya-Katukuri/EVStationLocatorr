from django.urls import path
from .views import (
    register_user,
    login_user,
    get_profile,
    update_profile
)

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("profile/", get_profile),
    path("profile/update/", update_profile),
]
