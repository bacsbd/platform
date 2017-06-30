from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from django.views import View
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response

from django.contrib import messages
from django.contrib.messages import get_messages

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
        storage = get_messages(request)
        flash_message = {
            'error': [],
            'success': [],
            'warning': [],
            'info': [],
        }

        for message in storage:
            flash_message[message.tags].append(message.__str__())

        return render(request, 'authentication/signup.html', {
            'error_message': flash_message['error'],
            'success_message': flash_message['success'],
            'warning_message': flash_message['warning'],
            'info_message': flash_message['info'],
        })

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
        serializer.is_valid()

        for field, error in serializer.errors.items():
            messages.error(request, "'"+field + "': " + error[0])

        if serializer.errors:
            return redirect('/user/signup')

        serializer.save()
        messages.success(request, "User Registration was successful! You may now login.")
        return redirect('/user/login')

class LoginView(View):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def get(self, request):
        storage = get_messages(request)
        flash_message = {
            'error': [],
            'success': [],
            'warning': [],
            'info': [],
        }

        for message in storage:
            flash_message[message.tags].append(message.__str__())

        return render(request, 'authentication/login.html', {
            'error_message': flash_message['error'],
            'success_message': flash_message['success'],
            'warning_message': flash_message['warning'],
            'info_message': flash_message['info'],
        })

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
        serializer.is_valid()

        for field, error in serializer.errors.items():
            messages.error(request, "'"+field + "': " + error[0])

        user = authenticate(username=username, password=password)

        if not user is None:
            if user.verified and user.is_active:
                login(request, user)
                messages.success(request, "Login Successful!")
                return redirect('/user/welcome')
        else:
            messages.error(request, "A user with similar Username and Password was not found")

        return redirect('/user/login')


@method_decorator(login_required, name='get')
@method_decorator(login_required, name='post')
class UserRetrieveUpdateView(View):
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request):
        """ GET """

        storage = get_messages(request)
        flash_message = {
            'error': [],
            'success': [],
            'warning': [],
            'info': [],
        }

        for message in storage:
            flash_message[message.tags].append(message.__str__())

        serializer = self.serializer_class(request.user)

        return render(request, 'authentication/profile.html', {
            'user': serializer.data,
            'error_message': flash_message['error'],
            'success_message': flash_message['success'],
            'warning_message': flash_message['warning'],
            'info_message': flash_message['info'],
        })

    def post(self, request):
        """ POST """
        serializer_data = request.POST

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid()

        if password != confirm_password:
            messages.error(request, "'password' and 'confirm_password' fields must match")
            return redirect('/user/profile/')

        for field, error in serializer.errors.items():
            messages.error(request, "'"+field + "': " + error[0])

        if serializer.errors:
            return redirect('/user/profile')

        serializer.save()

        return redirect('/user/profile')


class LogoutView(View):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        logout(request)
        return redirect('/user/login/')

@method_decorator(login_required, name='get')
class LandingPageView(View):
    permission_classes = (IsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = LoginSerializer

    def get(self, request):
        storage = get_messages(request)
        flash_message = {
            'error': [],
            'success': [],
            'warning': [],
            'info': [],
        }

        for message in storage:
            flash_message[message.tags].append(message.__str__())

        return render(request, 'authentication/landing_page.html', {
            'error_message': flash_message['error'],
            'success_message': flash_message['success'],
            'warning_message': flash_message['warning'],
            'info_message': flash_message['info'],
        })

    def post(self, request):
        return redirect('/user/welcome')
