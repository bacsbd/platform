from django.conf.urls import include, url
from .views import (
    LoginView, RegistrationView, UserRetrieveUpdateView, LogoutView
)

urlpatterns = [
    url(r'^signup/?$', RegistrationView.as_view()),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^profile/?$', UserRetrieveUpdateView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
]