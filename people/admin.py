from django.contrib import admin

from .models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'lahmanID', 'birth', 'death', 'debut',
                    'final_game')

admin.site.register(Person, PersonAdmin)
