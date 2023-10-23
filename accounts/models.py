from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where membership_number is the unique identifiers
    for authentication.
    """

    def create_user(self, phone_number, email=None, password=None, **extra_fields):
        """
        Create and save a User with given membership_number and password.
        """
        if not phone_number:
            raise ValueError('The given mobile must be set')

        email = self.normalize_email(email) if email else None
        user = self.model(
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, phone_number, email=None, password=None, **extra_fields
    ):
        """
        Create and save a SuperUser with the given membership_number and password.
        """

        user = self.create_user(phone_number, email, password, **extra_fields)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class JhandiUser(AbstractUser):
    """
    Custom user model.
    """
    username = None
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17, unique=True)
    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last Name"), max_length=150)
    is_agent = models.BooleanField(default=False)

    # username = None
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email"]
