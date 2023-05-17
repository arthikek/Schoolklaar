from django.contrib import admin
from .models import School, Leerling, Sessie, Begeleider, Teamleider, Niveau, Vak, Klas, Materiaal


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
    search_fields = ('Leerling__naam', 'Leerling__achternaam', 'begeleider__username')
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
    list_display = ('id', 'gebruiker')
    search_fields = ('gebruiker__username', 'scholen__naam')
    autocomplete_fields = ('gebruiker', 'scholen')


@admin.register(Teamleider)
class TeamleiderAdmin(admin.ModelAdmin):
    list_display = ('id', 'gebruiker', 'school')
    search_fields = ('gebruiker__username', 'school__naam')
    autocomplete_fields = ('gebruiker', 'school')


@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('naam',)
    search_fields = ('naam',)


@admin.register(Vak)
class VakAdmin(admin.ModelAdmin):
    list_display = ('naam',)
    search_fields = ('naam',)


@admin.register(Klas)
class KlasAdmin(admin.ModelAdmin):
    list_display = ('naam',)
    search_fields = ('naam',)


@admin.register(Materiaal)
class MateriaalAdmin(admin.ModelAdmin):
    list_display = ('titel', 'vak', 'niveau', 'klas')
    search_fields = ('titel', 'vak__naam', 'niveau__naam', 'klas__naam')
    list_filter = ('vak', 'niveau', 'klas')
