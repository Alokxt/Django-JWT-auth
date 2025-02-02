# Django-JWT-auth
#**Role Based Authentication and Authorization.**
This project has a role based authentication system. Authentication uses JWT(json web tokens).
It asks for the role/type of user at the login and redirect them accordingly.
Higher authorities(Schools in this project) has an admin-level control on student users.

#**Feature**

 **JWT Authentication**: Secure login and access control using JWT tokens. 
 **Role-Based Access**: Different user roles (School(admins), students, parents) with distinct permissions.
 **Forgot Password**: Allows users to reset their password.

 ## Installation
 **Clone the repository**:
  git clone 
**create a virtual env**
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate 
install  dependencies:
pip install -r requirements.txt

-setup the  environment variables like passwords,email,database.

**RUN MIGRATIONS**
python manage.py makemigrations.
python manage.py migrate.

**POSTMAN COLLECTION OF API's**
i've included the .json file of postman api collection with responses. here you can find it - 

**Technologies Used**
Django 
Django-REST framework
PyJWT
Mysql


