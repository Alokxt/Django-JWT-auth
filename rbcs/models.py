from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("role") == "school":
            extra_fields.setdefault("is_staff", True)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active",True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = [
        ('school', 'School'),
        ('student', 'Student'),
        ('parent','Parent'),
    ]
    
    name = models.CharField(max_length=250,null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
   
    username = None  # We are using email for authentication
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"
    


    @property
    def is_school(self):
        return self.role == 'school'

    


class Schools(models.Model):
    name = models.CharField(max_length=250)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'school'},related_name="school_admin")

    def __str__(self):
        return self.name


class students(models.Model):
    name = models.CharField(max_length=250)
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'student'}) 
    linked_student_id = models.IntegerField()
    school = models.ForeignKey(Schools, on_delete=models.CASCADE, related_name="students")
    
    
    def __str__(self):
        return self.name


class Achievements(models.Model):
    name = models.CharField(max_length=250)
    student = models.OneToOneField(students,related_name='acheivements',on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    achieved_on = models.DateTimeField(auto_now_add=True)
    linked_student_id = models.IntegerField()
    st_school = models.ForeignKey(Schools,related_name="student_achievements",on_delete=models.CASCADE,null=True)


   
    
    def school(self):
        return self.student.school
    

class parent(models.Model):
    name = models.CharField(max_length=250)
    child = models.ForeignKey(students,related_name="parent",on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUser,related_name="are_parents",on_delete=models.CASCADE,limit_choices_to={'role':'parent'})
    linked_student_id = models.IntegerField()
    child_school = models.OneToOneField(Schools,on_delete=models.CASCADE,related_name="parentslist",null=True)

    def __str__(self):
        return self.name