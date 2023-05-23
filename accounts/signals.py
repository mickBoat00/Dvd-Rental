from django.db.models.signals import post_save

from accounts.models import Manager, Staff, User


def update_other_user_models(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "manager":
            Manager.objects.create(user=instance)
        elif instance.user_type == "staff":
            Staff.objects.create(user=instance)


post_save.connect(update_other_user_models, User)