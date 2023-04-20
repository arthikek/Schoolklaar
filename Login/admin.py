from django.contrib import admin
from .models import School, Leerling, Sessie, Begeleider, Teamleider


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
            'fields': ('Leerling', 'begeleider'),
        }),
        ('Beoordeling', {
            'fields': ('inzicht', 'kennis', 'werkhouding'),
            'description': 'Geef een cijfer tussen 1 en 5',
        }),
        ('Extra', {
            'fields': ('extra',),
        }),
    )
    exclude = ['datum']


@admin.register(Begeleider)
class BegeleiderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    search_fields = ('user__username', 'school__naam')
    autocomplete_fields = ('user', 'school')


@admin.register(Teamleider)
class TeamleiderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'school')
    search_fields = ('user__username', 'school__naam')
    autocomplete_fields = ('user', 'school')

