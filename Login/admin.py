from django.contrib import admin
from .models import Leerling, Employer, Sessie

@admin.register(Leerling)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk','naam', 'achternaam', 'email')
    search_fields = ('naam', 'achternaam', 'email')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('pk','naam', 'achternaam', 'email')
    search_fields = ('naam', 'achternaam', 'email')

@admin.register(Sessie)
class SessieAdmin(admin.ModelAdmin):
    list_display = ('pk','Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding')
    list_filter = ('inzicht', 'kennis', 'werkhouding')
    search_fields = ('student__naam', 'student__achternaam', 'begeleider__naam', 'begeleider__achternaam')
    autocomplete_fields = ('Leerling', 'begeleider')
