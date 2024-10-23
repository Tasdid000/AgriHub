from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

class Farm_Type(models.Model):
    Farm_Type= models.CharField(max_length=200, primary_key=True)
    def __str__(self):
        return self.Farm_Type

# Create your models here.
# Create user manager
class MyUserManager(BaseUserManager):
    def create_user(self, email, name, phone_Number, password=None):
        """
        Creates and saves a User with the given email, name, phone_Number, and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_Number=phone_Number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_Number, password=None):
        """
        Creates and saves a superuser with the given email, name, phone_Number and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
            phone_Number=phone_Number
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True, 
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    image = models.ImageField(upload_to='media/userimage', default="media/userimage/userimage.png")
    name = models.CharField(max_length=255)
    phone_Number = models.CharField(max_length=11, default="")
    address = models.CharField(max_length=300, default="")
    Farm_Name = models.CharField(max_length=256, default="", null=True, blank=True)
    Farm_Type = models.ForeignKey(Farm_Type, on_delete=models.CASCADE, null=True, blank=True)
    Farm_Size = models.CharField(max_length=1230, null=True, blank=True)
    Farm_Location = models.CharField(max_length=1000, default="", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_expert = models.BooleanField(default=False)  # New field for expert users
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    email_verified  = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone_Number"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?
        Only admins should have full permissions.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?
        Only admins should have full permissions.
        """
        return self.is_admin

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        All admins are considered staff.
        """
        return self.is_admin
  

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=200)
    Last_Name = models.CharField(max_length=200)
    Email = models.EmailField(max_length=500)
    Phone_Number= models.CharField(max_length=11, blank= False)
    Farm_Type = models.ForeignKey(Farm_Type, on_delete=models.CASCADE, null=False, blank=False, default="")
    Message = models.TextField()


class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="media/Event/images", default ="")
    Blog_title = models.CharField(max_length=1000)
    date = models.DateField()
    category = models.CharField(max_length=200)
    content = models.TextField()

class Appointment_time_slot(models.Model):
    time = models.CharField(max_length=10, primary_key=True)
    
    def __str__(self):
        return self.time
    
class Video_conference_appointment(models.Model):
    id= models.AutoField(primary_key=True)
    Topic = models.CharField(max_length=2000, default="")
    UserId = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default="")
    Date = models.DateField()
    Description = models.TextField()
    Time = models.ForeignKey(Appointment_time_slot, on_delete=models.CASCADE, null=False, blank=False, default="")


class Government_Support(models.Model):
    SupportId = models.CharField(primary_key=True, max_length=200, unique=True)
    image = models.ImageField(upload_to="media/Government_Support")
    Title = models.CharField(max_length=2000, default="")
    date = models.DateField()
    category = models.CharField(max_length=200)
    content = models.TextField()

