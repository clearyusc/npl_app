from django.contrib import admin

# Register your models here.
from .models import Encounter, Team, Laborer

admin.site.register(Laborer)
admin.site.register(Team)
admin.site.register(Encounter)
