from django.contrib import admin

from accounts.models import Address, Manager, Staff, User

admin.site.register(User)
admin.site.register(Manager)
admin.site.register(Staff)
admin.site.register(Address)
