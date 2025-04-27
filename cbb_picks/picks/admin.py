from django.contrib import admin
from .models import Team, Game, Pick, Location

admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Pick)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country')
    list_filter = ('state', 'country')
    search_fields = ('city',)
