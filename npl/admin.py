from django.contrib import admin

# Register your models here.
from .models import Encounter, Team, Laborer
from import_export import resources


admin.site.register(Laborer)
admin.site.register(Team)
admin.site.register(Encounter)


class EncounterResource(resources.ModelResource):

    class Meta:
        model = Encounter
        fields = ('laborer__user__username', 'name', 'action_prayer', 'action_testimony', 'action_gospel', 'phone_number', 'response', 'notes',
                  'date_time', 'street_address_number', 'street_address_name', 'apt_or_unit', 'city', 'state', 'zip',
                  'lat', 'lng', 'full_address')
        export_order = fields
