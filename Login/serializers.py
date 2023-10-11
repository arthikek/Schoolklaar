from rest_framework import serializers
from .models import Sessie, Begeleider, Leerling, School, Vak, User, LeerlingVakRating

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class BegeleiderSerializer(serializers.ModelSerializer):
    scholen = SchoolSerializer(read_only=True, many=True)

    class Meta:
        model = Begeleider
        fields = ['id', 'gebruiker', 'scholen']
        
class VakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vak
        fields = '__all__'
        
class LeerlingVakRatingSerializer(serializers.ModelSerializer):
    vak = VakSerializer(read_only=True)
    class Meta:
        model = LeerlingVakRating
        fields = ['leerling', 'vak', 'cijfer', 'beschrijving']
        

        
class LeerlingSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)  
    vak_ratings = LeerlingVakRatingSerializer(source='leerlingvakrating_set', many=True, read_only=True)
    class Meta:
        model = Leerling
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # or other fields you want to include

class SessieSerializer(serializers.ModelSerializer):
    Leerling = LeerlingSerializer(read_only=True)
    begeleider = UserSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    vak = VakSerializer(read_only=True)

    class Meta:
        model = Sessie
        fields = ['id', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'extra', 'datum', 'school', 'vak']
