from django.http import response
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json


class RegisterView(APITestCase):
    def test_create_user(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201
        data = json.loads(response.content)
        assert data["message"] == "User created successfully."

    def test_try_create_user_existing(self):
        user = User.objects.create(**{
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "pbkdf2_sha256$260000$QlcSFq5XxanBg8tGBoWTZB$n8byU1TTlzg0Vi13iK9wgw0HlvzRaDtr+IUMGlBXwZM="
        })
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "User already exists"


class LoginView(APITestCase):
    def test_login_user(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

    def test_try_login_user_with_bad_username_and_password(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "salazar",
            "password": "12345"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data["message"] == "Incorrect user or password"


class LogoutView(APITestCase):
    def test_logout_user(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        response = self.client.post('/monnity/logout/', format='json')
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data["message"] == "User has logged out"

    def test_try_logout_no_user(self):
        response = self.client.post('/monnity/logout/', format='json')
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data["message"] == "User has logged out"


class UserDetail(APITestCase):
    def test_get_user(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        response = self.client.get('/monnity/user_detail/', format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        user = User.objects.filter(username=data['username'])
        assert data['first_name'] == user[0].first_name
        assert data['last_name'] == user[0].last_name
        assert data['username'] == user[0].username
        assert data['email'] == user[0].email

    def test_try_get_user_whit_no_session(self):
        request_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_data,
            format='json')
        assert response.status_code == 201

        response = self.client.get('/monnity/user_detail/', format='json')
        assert response.status_code == 404

    def test_update_user(self):

        request_initial_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_initial_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        request_data = {
            "first_name": "davida",
            "last_name": "salazara",
            "username": "sazara",
            "email": "dav@gmail.com",
        }
        response = self.client.put(
            '/monnity/user_detail/',
            request_data,
            format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        user = User.objects.filter(username=data['username'])
        assert data['first_name'] == user[0].first_name
        assert data['last_name'] == user[0].last_name
        assert data['username'] == user[0].username
        assert data['email'] == user[0].email

        assert data['first_name'] != request_initial_data['first_name']
        assert data['last_name'] != request_initial_data['last_name']
        assert data['username'] != request_initial_data['username']
        assert data['email'] != request_initial_data['email']

    def test_delete_user(self):

        request_initial_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_initial_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        response = self.client.delete('/monnity/user_detail/', format='json')
        assert response.status_code == 204


class ChangePasswordView(APITestCase):
    def test_change_user_password(self):

        request_initial_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_initial_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        request_data = {
            "old_password": "1234",
            "new_password": "12345"
        }
        response = self.client.put(
            '/monnity/change_pasword/',
            request_data,
            format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "password updated"

    def test_try_change_user_password_bad_old_password(self):

        request_initial_data = {
            "first_name": "david",
            "last_name": "salazar",
            "username": "sazar",
            "email": "da@gmail.com",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/register/',
            request_initial_data,
            format='json')
        assert response.status_code == 201

        request_data = {
            "username": "sazar",
            "password": "1234"
        }
        response = self.client.post(
            '/monnity/login/', request_data, format='json')
        assert response.status_code == 200
        data = json.loads(response.content)
        assert data["message"] == "Registered user"

        request_data = {
            "old_password": "123444",
            "new_password": "1234"
        }
        response = self.client.put(
            '/monnity/change_pasword/',
            request_data,
            format='json')
        assert response.status_code == 400
        data = json.loads(response.content)
        assert data["message"] == "Old password wrong"
