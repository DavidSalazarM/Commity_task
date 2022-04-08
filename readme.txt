this project needs Python version 3.6.9 

run the command "python manage.py migrate" to apply the migrations

run the command "python manage.py runserver" to start the server

run the command "python manage.py test" to run the tests

register users:
your localhost/monnity/register/ with POST method
request body JSON
{
    "first_name":"your_last_name",
    "last_name":"your_last_name",
    "username":"your_username",
    "email":"your_email,
    "password":"your_password"
}

login:
your localhost/monnity/login/ with POST method
request body JSON
{
    "username":"your_username",
    "password":"your_password"
}

logout:
your localhost/monnity/logout/ with POST method

user information:
your localhost/monnity/user_detail/ with GET method

update user:
your localhost/monnity/user_detail/ with PUT method
request body JSON
{
    "first_name":"your_last_name",
    "last_name":"your_last_name",
    "username":"your_username",
    "email":"your_email,
}
you only need to send the field you want to update

delete user:
your localhost/monnity/user_detail/ with DELETE method

change password:
your localhost/monnity/change_pasword/ with PUT method
request body JSON
{
    "old_password":"1234",
    "new_password":"123456"
}






