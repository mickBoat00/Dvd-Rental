from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, email, user_type, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            user_type=user_type
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    CUSTOMER = "customer"
    MANAGER = "manager"
    STAFF = "staff"

    USER_TYPE = [
        (CUSTOMER, "Customer"),
        (MANAGER, "Manager"),
        (STAFF, "Staff"),
    ]

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    address = models.OneToOneField("Address", related_name="person", on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=8, choices=USER_TYPE)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField()

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email

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
    
    def __str__(self) -> str:
        return self.email


class BaseEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)


class Staff(BaseEmployee):
    def __str__(self) -> str:
        return f"Staff {self.user.email}"

class Manager(BaseEmployee):
    def __str__(self) -> str:
        return f"Staff {self.user.email}"


def update_other_user_models(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "manager":
            Manager.objects.create(user=instance)
        elif instance.user_type == "staff":
            Staff.objects.create(user=instance)


post_save.connect(update_other_user_models, User)


class Address(models.Model):
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self) -> str:
        return self.address
