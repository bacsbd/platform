from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from django.views import View
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

# from .renderers import UserJSONRenderer

from .serializers import (
    RegistrationSerializer, LoginSerializer, UserSerializer,
)


class RegistrationView(View):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def get(self, request):
        """ GET """
        return render(request, 'authentication/signup.html', {})

    def post(self, request):
        """
        Handle post request
        """

        user = request.POST
        password = user.get('password', None)
        confirm_password = user.get('confirm_password', None)

        if password != confirm_password:
            return redirect('/user/signup/')

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return redirect('/user/login')

class LoginView(View):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self, request):
        return render(request, 'authentication/login.html', {})

    def post(self, request):
        """
        Handle post request
        """
        username = request.POST.get('username', {})
        password = request.POST.get('password', {})
        user = {
            'username': username,
            'password': password,
        }

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=username, password=password)

        if not user is None:
            if user.verified and user.is_active:
                login(request, user)
                return redirect('/user/profile/')

        return redirect('/user/login')


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class UserRetrieveUpdateView(View):
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request):
        """ GET """
        serializer = self.serializer_class(request.user)

        return render(request, 'authentication/profile.html', {
            'user': serializer.data
        })

    def post(self, request):
        """ POST """
        serializer_data = request.POST

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return redirect('/user/profile')


class LogoutView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return redirect('/user/login/')
