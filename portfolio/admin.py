from django.contrib import admin
from . models import AssetEntry, User

# Register your models here.
admin.site.register(AssetEntry)
admin.site.register(User)