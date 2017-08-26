from django.conf.urls import include, url
from .views import (
    LoginView, RegistrationView, UserRetrieveUpdateView, LogoutView, LandingPageView, EmailVerificationView,
    VerificationResendView,
)

urlpatterns = [
    url(r'^signup/?$', RegistrationView.as_view()),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^welcome/?$', LandingPageView.as_view()),
    url(r'^profile/?$', UserRetrieveUpdateView.as_view()),
    url(r'^logout/?$', LogoutView.as_view()),
    url(r'^verify/(?P<token>[\w:\.-]+)/$', EmailVerificationView.as_view(),
        name='email_verification_view'),
    url(r'^verification/resend/?$', VerificationResendView.as_view()),
]