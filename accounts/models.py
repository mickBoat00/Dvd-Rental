from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save

from accounts.managers import UserManager


class User(AbstractBaseUser):
    CUSTOMER = "customer"
    MANAGER = "manager"
    STAFF = "staff"
    ADMIN = "admin"

    USER_TYPE = [
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (STAFF, "Staff"),
        (CUSTOMER, "Customer"),
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
    
def update_other_user_models(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "manager":
            Manager.objects.create(user=instance)
        elif instance.user_type == "staff":
            Staff.objects.create(user=instance)


post_save.connect(update_other_user_models, User)


class BaseEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(null=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)


class Staff(BaseEmployee):
    def __str__(self) -> str:
        return f"Staff {self.user.email}"

class Manager(BaseEmployee):
    def __str__(self) -> str:
        return f"Manager {self.user.email}"
    
class Customer(BaseEmployee):
    def __str__(self) -> str:
        return f"Customer {self.user.email}" 


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
