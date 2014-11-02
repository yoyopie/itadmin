from django.contrib import admin
from models import Share,Partition,Server

# Register your models here.

admin.site.register(Server)
admin.site.register(Partition)
admin.site.register(Share)
