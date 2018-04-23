# Register your models here.

from django.contrib import admin
from .models import Entry
from .models import History

admin.site.register(Entry)
admin.site.register(History)
