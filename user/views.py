from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import status
import datetime
from django.contrib.auth import login, logout, authenticate
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .serializers import UsersSerializer, ChangePasswordSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class RegisterView(APIView):
    def post(self, request, format=None):
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                first_name=data['first_name'],
                last_name=data['last_name'],
                username=data['username'],
                email=data['email'],
                password=data['password'],
                date_joined=datetime.datetime.now())
            user.save()
            message = "User created successfully."
            return JsonResponse({"message": message},
                                status=status.HTTP_201_CREATED)
        except IntegrityError:
            message = "User already exists"
            return JsonResponse({"message": message},
                                status=status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        user = authenticate(
            username=data['username'],
            password=data['password'])
        if user:
            login(request, user)
            message = "Registered user"
            return JsonResponse({"message": message},
                                status=status.HTTP_200_OK)
        else:
            message = "Incorrect user or password"
            return JsonResponse({"message": message},
                                status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        SessionAuthentication)

    def post(self, request):
        logout(request)
        message = "User has logged out"
        return JsonResponse({"message": message}, status=status.HTTP_200_OK)


class UserDetail(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        SessionAuthentication)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UsersSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors)

    def delete(self, request, format=None):
        user = self.get_object(request.user.id)
        user.delete()
        message = "User Deleted"
        return JsonResponse({"message": message},
                            status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    authentication_classes = (
        CsrfExemptSessionAuthentication,
        SessionAuthentication)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, format=None):
        user = self.get_object(request.user.id)
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not user.check_password(serializer.data.get("old_password")):
                message = "Old password wrong"
                return JsonResponse({"message": message},
                                    status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            message = "password updated"
            return JsonResponse({"message": message},
                                status=status.HTTP_200_OK)
        return JsonResponse({"message": message})
