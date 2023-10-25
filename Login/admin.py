from django.contrib import admin
from .models import School, Leerling, Sessie, Begeleider, Teamleider, Niveau, Vak, Klas, Materiaal, LeerlingVakRating, LeerlingVakRatingHistory


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('naam', 'grootte')
    search_fields = ('naam',)
    list_filter = ('grootte',)



@admin.register(LeerlingVakRatingHistory)
class LeerlingVakRatingHistoryAdmin(admin.ModelAdmin):
    list_display = ('vak_name', 'date_recorded', 'cijfer', 'beschrijving')
    search_fields = ('leerling_vak_rating__vak__name', 'date_recorded')
    list_filter = ('date_recorded',)
    ordering = ('-date_recorded',)

    def get_queryset(self, request):
        # Use select_related to optimize database queries when accessing related models
        return super().get_queryset(request).select_related('leerling_vak_rating', 'leerling_vak_rating__vak')


class LeerlingVakInline(admin.TabularInline):
    model = LeerlingVakRating
    extra = 1  # Number of blank forms to display


@admin.register(Leerling)
class LeerlingAdmin(admin.ModelAdmin):
    list_display = ('naam', 'achternaam', 'email', 'school', 'gebruiker','pk')
    search_fields = ('naam', 'achternaam', 'email')
    list_filter = ('school',)
    inlines = [LeerlingVakInline]

# ... remaining admin classes ...

@admin.register(LeerlingVakRating)
class LeerlingVakAdmin(admin.ModelAdmin):
    list_display = ('leerling', 'vak', 'cijfer', 'beschrijving')
    search_fields = ('leerling__naam', 'leerling__achternaam', 'vak__naam')

@admin.register(Sessie)
class SessieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'school')
    list_filter = ('inzicht', 'kennis', 'werkhouding', 'school')
    search_fields = ('Leerling__naam', 'Leerling__achternaam', 'begeleider__username', 'school__naam', 'vak__naam')
    autocomplete_fields = ('Leerling', 'begeleider', 'school')
    fieldsets = (
        ('Algemeen', {
            'fields': ('Leerling', 'begeleider', 'school', 'vak', 'datum'),
        }),
        ('Beoordeling', {
            'fields': ('inzicht', 'kennis', 'werkhouding'),
            'description': 'Geef een cijfer tussen 1 en 5',
        }),
        ('Extra', {
            'fields': ('extra',),
        }),
    )
 



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
    list_display = ('naam', 'pk')
    search_fields = ('naam',)


@admin.register(Klas)
class KlasAdmin(admin.ModelAdmin):
    list_display = ('naam' , 'pk')	

    search_fields = ('naam',)


@admin.register(Materiaal)
class MateriaalAdmin(admin.ModelAdmin):
    list_display = ('titel', 'vak', 'niveau', 'klas')
    search_fields = ('titel', 'vak__naam', 'niveau__naam', 'klas__naam')
    list_filter = ('vak', 'niveau', 'klas')
