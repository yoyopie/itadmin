from django.contrib import admin
from models import Share,Partition,Server,Savedate

# Register your models here.

admin.site.register(Savedate)
admin.site.register(Server)
admin.site.register(Partition)
admin.site.register(Share)
