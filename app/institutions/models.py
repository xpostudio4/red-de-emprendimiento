#Stdlib Imports
import datetime

from django.db import models
from django.contrib.auth.models import (
        BaseUserManager, AbstractBaseUser, PermissionMixin
        )
#Third party libraries
#from templated_email import send_templated_mail

class AppUserManager(BaseUserManager):

    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, first_name, last_name
        and password.
        """
        if not email:
            raise ValueError('Todo usuario debe tener un email')

        user = self.model(
                email = AppUserManager.normalize_email(email),
                name = name,
                )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password):
        """
            Creates and saves a Superuser with the given email, first_name, last_name
            and password.
        """
        user = self.create_user(email,
                name=name,
                password=password
                )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
            verbose_name="Correo Electronico",
            max_length=255,
            unique=True,
            db_index=True
            )
    name = models.CharField(max_length=40, verbose_name="Nombre de la Institucion")
    url = models.URLField(max_length=40, verbose_name="Pagina Web")
    description = models.TextField(verbose_name="Descripcion")
    logo = models.ImageField(upload_to="profile_pics", blank=True)
    phone = models.CharField(max_length=10,null=True, blank=True)
    is_phone_visible = models.BooleanField(default=False,verbose_name="Desea que el telefono se vea en sus anuncios")
    address = models.TextField(null=True, blank=True, verbose_name="Direccion")
    is_address_visible = models.BooleanField(default=False, verbose_name="Desea que su direccion se vea en los anuncios")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'description', 'logo', 'phone','url']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        #The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        #if not self.id:
            #send_templated_mail(
            #    template_name='user_creation',
            #    from_email='info@mypimes.com',
            #    recipient_list = [self.email],
            #    context={
            #        'username': self.email,
            #        'full_name': self.get_full_name,
            #        'signup_date': datetime.datetime.today(),
            #        },
            #    )
        super(UserProfile, self).save(*args, **kwargs)


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

