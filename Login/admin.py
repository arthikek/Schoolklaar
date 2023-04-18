from django.contrib import admin
from .models import Employer, School, Leerling, Sessie

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('naam', 'achternaam', 'email')
    search_fields = ('naam', 'achternaam', 'email')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('naam', 'grootte')
    search_fields = ('naam',)
    list_filter = ('grootte',)

@admin.register(Leerling)
class LeerlingAdmin(admin.ModelAdmin):
    list_display = ('naam', 'achternaam', 'email', 'school')
    search_fields = ('naam', 'achternaam', 'email')
    list_filter = ('school',)

@admin.register(Sessie)
class SessieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding')
    list_filter = ('inzicht', 'kennis', 'werkhouding')
    search_fields = ('Leerling__naam', 'Leerling__achternaam', 'begeleider__naam', 'begeleider__achternaam')
    autocomplete_fields = ('Leerling', 'begeleider')
    fieldsets = (
        ('Algemeen', {
            'fields': ('Leerling', 'begeleider', 'datum'),
        }),
        ('Beoordeling', {
            'fields': ('inzicht', 'kennis', 'werkhouding'),
            'description': 'Geef een cijfer tussen 1 en 5',
        }),
        ('Extra', {
            'fields': ('extra',),
        }),
    )