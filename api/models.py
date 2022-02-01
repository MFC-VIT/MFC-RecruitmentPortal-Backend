from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'

class UserManager(BaseUserManager):

    def create_user(self, username, email, phone_number, reg_no, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, reg_no = reg_no)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password should not be none')

        phone_number = '1234567890'
        reg_no = '19BIT0000'
        user = self.create_user(username, email, phone_number, reg_no, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = MyValidator()
    username = models.CharField(max_length=150,validators=[username_validator])
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = PhoneNumberField()
    reg_no = models.CharField(max_length=10,default='19BIT0000')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    technical_test = models.BooleanField(default=False)
    management_test = models.BooleanField(default=False)
    editorial_test = models.BooleanField(default=False)
    design_test = models.BooleanField(default=False)
    media_test = models.BooleanField(default=False)
    technical_test_passed = models.BooleanField(default=False)
    management_test_passed = models.BooleanField(default=False)
    editorial_test_passed = models.BooleanField(default=False)
    design_test_passed = models.BooleanField(default=False)
    media_test_passed = models.BooleanField(default=False)
    otp = models.IntegerField(blank=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class Domain(models.Model):
    domain_name = models.CharField(max_length=250)

    def __str__(self):
        return self.domain_name

class mcqQuestions(models.Model):
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_mcq_questions")
    question_id = models.CharField(max_length=250, unique=True, primary_key=True)
    question = models.TextField()
    option_1 = models.CharField(max_length=500)
    option_2 = models.CharField(max_length=500)
    option_3 = models.CharField(max_length=500)
    option_4 = models.CharField(max_length=500)

    def __str__(self):
        return self.question

class typeQuestions(models.Model):
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_type_questions")
    question_id = models.CharField(max_length=250, unique=True, primary_key=True)
    question = models.TextField()

    def __str__(self):
        return self.question

class Responses(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_responses")
    domain = models.ForeignKey(Domain,on_delete=models.CASCADE,related_name="domain_responses")
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question



# from django.contrib.auth.models import AbstractUser

# class MyUser(AbstractUser):
#     username_validator = MyValidator()
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and @/./ /-/_ only.'),
#         validators=[username_validator],
#             error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
