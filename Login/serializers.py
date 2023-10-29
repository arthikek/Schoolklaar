from rest_framework import serializers
from .models import Sessie, Begeleider, Leerling, School, Vak, User, LeerlingVakRating, Klas, Niveau,Teamleider, Materiaal, LeerlingVakRatingHistory

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # or other fields you want to include

class BegeleiderSerializer(serializers.ModelSerializer):
    scholen = SchoolSerializer(read_only=True, many=True)
    gebruiker = UserSerializer(read_only=True)
    
    class Meta:
        model = Begeleider
        fields = ['id', 'gebruiker', 'scholen']

class TeamleiderSerializer(serializers.ModelSerializer):
    gebruiker = UserSerializer(read_only=True)
    scholen = SchoolSerializer(read_only=True, many=True)
    class Meta:

        model = Teamleider
        fields = ('id', 'gebruiker', 'scholen')

class VakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vak
        fields = '__all__'

        
       
class MateriaalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materiaal
        fields = '__all__'
        
        
               
class LeerlingVakRatingHistorySerializer(serializers.ModelSerializer):
    leerling_vak_rating = serializers.PrimaryKeyRelatedField(queryset=LeerlingVakRating.objects.all())

    class Meta:
        model = LeerlingVakRatingHistory
        fields = '__all__'

        
        

        
        
        
class LeerlingVakRatingSerializer(serializers.ModelSerializer):
    vak = VakSerializer(read_only=True)
    histories = LeerlingVakRatingHistorySerializer(source='leerlingvakratinghistory_set', many=True, read_only=True)

    class Meta:
        model = LeerlingVakRating
        fields = ['leerling', 'vak', 'cijfer', 'beschrijving', 'histories']

   
        
class LeerlingSerializer(serializers.ModelSerializer):
    
    school = SchoolSerializer(read_only=True)  
    vak_ratings = LeerlingVakRatingSerializer(source='leerlingvakrating_set', many=True, read_only=True)
    
    class Meta:
        model = Leerling
        fields = '__all__'

    def create(self, validated_data):
        school_id = validated_data.pop('school', None)
        instance = Leerling.objects.create(**validated_data)
        
        if school_id:
            instance.school = School.objects.get(pk=school_id)
            instance.save()

        return instance



class SessieSerializer(serializers.ModelSerializer):
    Leerling = LeerlingSerializer(read_only=False)
    begeleider = UserSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    vak = VakSerializer(read_only=False)
    
    class Meta:
        model = Sessie
        fields = ['id', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'extra', 'datum', 'school', 'vak']
    
class ShallowSessieSerializer(serializers.ModelSerializer):
    begeleider = UserSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    vak = VakSerializer(read_only=True)
    
    class Meta:
        model = Sessie
        fields = ['id', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'extra', 'datum', 'school', 'vak']


class LeerlingDetailSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    vak_ratings = LeerlingVakRatingSerializer(source='leerlingvakrating_set', many=True, read_only=True)
    sessies = ShallowSessieSerializer(source='sessie_set', many=True, read_only=True)  # Add this line
    vak_ratings_history = LeerlingVakRatingHistorySerializer(source='leerlingvakratinghistory_set', many=True, read_only=True)
    class Meta:
        model = Leerling
        fields = ['naam', 'achternaam', 'email', 'school', 'klas', 'niveau', 'gebruiker', 'vak_ratings', 'vak_ratings_history','sessies']




   

class SessieSerializer_2(serializers.ModelSerializer):
    Leerling = serializers.PrimaryKeyRelatedField(queryset=Leerling.objects.all())
    begeleider = UserSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    vak = serializers.PrimaryKeyRelatedField(queryset=Vak.objects.all())

    class Meta:
        model = Sessie
        fields = ['id', 'Leerling', 'begeleider', 'inzicht', 'kennis', 'werkhouding', 'extra', 'datum', 'school', 'vak']



# Serializer for the Klas model
class KlasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klas
        fields = ['id', 'naam']


# Serializer for the Klas model
class NiveauSerializer(serializers.ModelSerializer):
    class Meta:
        model = Niveau
        fields = ['id', 'naam']
        
