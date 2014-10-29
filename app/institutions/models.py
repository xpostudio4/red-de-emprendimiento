#Stdlib Imports
import datetime

from django.db import models
from django.contrib.auth.models import (
        BaseUserManager, AbstractBaseUser
        )
#Third party libraries
from taggit.managers import TaggableManager
#from templated_email import send_templated_mail

class AppUserManager(BaseUserManager):

    def create_user(self, email, full_name, password=None):
        """
        Creates and saves a User with the given email, first_name, last_name
        and password.
        """
        if not email:
            raise ValueError('Todo usuario debe tener un email')

        user = self.model(
                email = AppUserManager.normalize_email(email),
                full_name = full_name,
                )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, password, email):
        """
            Creates and saves a Superuser with the given email, first_name, last_name
            and password.
        """
        user = self.create_user(email=email,
                full_name=full_name,
                password=password
                )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Organization(models.Model):
    """
    This class represents the institution profile, it must be approved by one of the members
    of the organization, every organization must be approved before being published.
    """
    name = models.CharField(max_length=40, verbose_name="Nombre de la Institucion")
    url = models.URLField(max_length=40, verbose_name="Pagina Web", blank=True, null=True)
    description = models.TextField(verbose_name="Descripcion", blank=True, null=True)
    logo = models.ImageField(upload_to="profile_pics",null=True, blank=True)
    phone = models.CharField(max_length=10,null=True, blank=True)
    is_phone_visible = models.BooleanField(default=False,verbose_name="Desea que el telefono se vea en sus anuncios")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Direccion")
    is_address_visible = models.BooleanField(default=False, verbose_name="Desea que su direccion se vea en los anuncios")
    province = models.CharField(max_length=100, null=True, blank=True)
    approved = models.BooleanField(default=False)
    categories = TaggableManager()

    def __unicode__(self):
        return self.name

class UserProfile(AbstractBaseUser):
    email = models.EmailField(
            verbose_name="Correo Electronico",
            max_length=255,
            unique=True,
            db_index=True
            )
    full_name = models.CharField(max_length=40, verbose_name="Nombre Completo")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = AppUserManager()
    organization = models.ForeignKey(Organization)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        #The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.id:
            #Create Organization for the user
            organization = Organization.objects.create(
                    name=str(self.full_name)+ "'s Organization"
                    )
            self.organization  = organization
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


class Event(models.Model):
    """
    The purpose of this class is to manage the dates of all the events of the
    national web of entrepreneurship.
    """
    name = models.CharField(max_length=80)
    description = models.TextField()
    created = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    organization = models.ForeignKey(Organization, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        '''On save, fill created field'''
        if not self.id:
            self.created = datetime.date.today()
        super(Event, self).save(*args, **kwargs)

class MailingList(models.Model):
    """
    This form contains all the people being subscribed
    to our mailing list. All fields are mandatory.
    """
    full_name = models.CharField(max_length=80)
    email = models.EmailField()
    province = models.CharField(max_length=24)

    def __unicode__(self):
        return self.full_name

