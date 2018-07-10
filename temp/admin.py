# Register your models here.

from django.contrib import admin
from .models import Entry
from .models import History
from .models import Coins
from .models import Difficulty

admin.site.register(Entry)
admin.site.register(History)
admin.site.register(Coins)
admin.site.register(Difficulty)
