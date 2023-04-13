from django.contrib import admin
from .models import Student, Employer, Sessie

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk','naam', 'achternaam', 'email')
    search_fields = ('naam', 'achternaam', 'email')

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('pk','naam', 'achternaam', 'email')
    search_fields = ('naam', 'achternaam', 'email')

@admin.register(Sessie)
class SessieAdmin(admin.ModelAdmin):
    list_display = ('pk','student', 'begeleider', 'inzicht', 'kennis', 'werkhouding')
    list_filter = ('inzicht', 'kennis', 'werkhouding')
    search_fields = ('student__naam', 'student__achternaam', 'begeleider__naam', 'begeleider__achternaam')
    autocomplete_fields = ('student', 'begeleider')
