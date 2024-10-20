from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django_resized import ResizedImageField
from rest_framework.validators import UniqueValidator
# from django.contrib.postgres.fields import ArrayField
from user.models import User,Parent, Professeur, Eleve, Admin
from .models import Parent,Enfant,cv_file_name,diplome_file_name
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
#from .models import Transaction



from dj_rest_auth.serializers import UserDetailsSerializer

from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


from rest_framework import serializers

class CustomUserDetailsSerializer(UserDetailsSerializer):
    role = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'last_login','is_active', 'is_parent', 'is_eleve', 'is_professeur', 'role', 'info')
        read_only_fields = ('is_active','is_admin', 'is_parent', 'is_eleve', 'is_professeur', 'image_profil')

    def get_role(self, instance):
        if instance.is_parent:
            return 'parent'
        elif instance.is_professeur:
            return 'prof'
        elif instance.is_eleve:
            return 'eleve'
        else:
            return ''

    def get_info(self, instance):
        if instance.is_parent:
            parent = instance.parent
            return parent.to_json()
        elif instance.is_professeur:
            professeur = instance.professeur
            return professeur.to_json()
        elif instance.is_eleve:
            eleve = instance.eleve
            return eleve.to_json()
        else:
            return {}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user_details'] = {
            'role': representation.pop('role'),
            'info': representation.pop('info')
        }
        if instance.image_profil:
            representation['image_profil'] = instance.image_profil.url
        return representation

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = ['prenom', 'nom', 'date_naissance', 'niveau_scolaire', 'etablissement']



class ParentRegisterSerializer(RegisterSerializer):
    nom = serializers.CharField(max_length=50)
    prenom = serializers.CharField(max_length=30)
    date_naissance = serializers.DateField()
    ville = serializers.CharField(max_length=100)
    numero_telephone = serializers.CharField(max_length=12)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    enfants = EnfantSerializer(many=True)
    

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['is_parent'] = True
        # Récupérer l'image de la requête correctement
        image_profil = self.context["request"].FILES.get('image_profil')
        if image_profil:
            cleaned_data['image_profil'] = image_profil
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.is_parent = True
        # Save the image in the user instance
        image_profil = self.validated_data.get('image_profil')
        if image_profil:
            user.image_profil = image_profil
        user.save()
        parent_data = {
            'user': user,
            'nom': self.validated_data.get('nom'),
            'prenom': self.validated_data.get('prenom'),
            'ville': self.validated_data.get('ville'),
            'date_naissance': self.validated_data.get('date_naissance'),
            'numero_telephone': self.validated_data.get('numero_telephone'),
            'latitude': self.validated_data.get('latitude'),
            'longitude': self.validated_data.get('longitude'),
        }
        parent = Parent.objects.create(**parent_data)

        enfants_data = self.validated_data.get('enfants')
        for enfant_data in enfants_data:
            Enfant.objects.create(parent=parent, **enfant_data)

        return user



from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Professeur
from api.models import Matiere

class ProfesseurRegisterSerializer(RegisterSerializer):
    nom = serializers.CharField(max_length=50)
    prenom = serializers.CharField(max_length=30)
    ville = serializers.CharField(max_length=30)
    date_naissance = serializers.DateField()
    numero_telephone = serializers.CharField(max_length=12)
    cv = serializers.FileField(write_only=True, required=False, allow_empty_file=False, use_url=False)
    diplome = serializers.FileField(write_only=True, required=False, allow_empty_file=False, use_url=False)
    matieres_a_enseigner = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    niveau_etude = serializers.CharField(max_length=50)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['is_professeur'] = True
        cleaned_data.update({
            'nom': self.validated_data.get('nom', ''),
            'prenom': self.validated_data.get('prenom', ''),
            'ville': self.validated_data.get('ville', ''),
            'date_naissance': self.validated_data.get('date_naissance', None),
            'numero_telephone': self.validated_data.get('numero_telephone', ''),
            'cv': self.validated_data.get('cv', None),
            'diplome': self.validated_data.get('diplome', None),
            'matieres_a_enseigner': self.validated_data.get('matieres_a_enseigner', []),
            'niveau_etude': self.validated_data.get('niveau_etude', ''),
            'latitude': self.validated_data.get('latitude', 0.0),
            'longitude': self.validated_data.get('longitude', 0.0),
        })
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.is_professeur = True
        user.save()

        professeur_data = {
            'user': user,
            'nom': self.validated_data.get('nom'),
            'prenom': self.validated_data.get('prenom'),
            'ville': self.validated_data.get('ville'),
            'date_naissance': self.validated_data.get('date_naissance'),
            'numero_telephone': self.validated_data.get('numero_telephone'),
            'cv': self.validated_data.get('cv'),
            'diplome': self.validated_data.get('diplome'),
            'niveau_etude': self.validated_data.get('niveau_etude'),
            'latitude': self.validated_data.get('latitude'),
            'longitude': self.validated_data.get('longitude'),
        }

        # Retrieve address from coordinates
        from .views import obtenir_adresse_depuis_coordonnees
        latitude = professeur_data['latitude']
        longitude = professeur_data['longitude']
        professeur_data['adresse'] = obtenir_adresse_depuis_coordonnees(latitude, longitude)

        professeur = Professeur.objects.create(**professeur_data)
        matieres = self.validated_data.get('matieres_a_enseigner')
        professeur.matieres_a_enseigner.set(matieres)
        return user




class EleveRegisterSerializer(RegisterSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    nom = serializers.CharField(max_length=50)
    prenom = serializers.CharField(max_length=30)
    ville = serializers.CharField(max_length=30)
    date_naissance = serializers.DateField()
    Etablissement = serializers.CharField(max_length=100)
    numero_telephone = serializers.CharField(max_length=12)
    niveau_scolaire = serializers.CharField(max_length=100)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['is_eleve'] = True
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.is_eleve = True
        user.save()
        eleve_data = {
            'user': user,
            'nom': self.validated_data.get('nom'),
            'prenom': self.validated_data.get('prenom'),
            'ville': self.validated_data.get('ville'),
            'date_naissance': self.validated_data.get('date_naissance'),
            'niveau_scolaire': self.validated_data.get('niveau_scolaire'),
            'numero_telephone': self.validated_data.get('numero_telephone'),
            'Etablissement': self.validated_data.get('Etablissement'),
            'latitude': self.validated_data.get('latitude'),
            'longitude': self.validated_data.get('longitude'),
        }
        Eleve.objects.create(**eleve_data)
        return user

class AdminRegisterSerializer(RegisterSerializer):

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data['is_admin'] = True
        return cleaned_data

    def save(self, request):
        user = super().save(request)
        user.is_admin = True
        user.save()
        admin_data = {
            'user': user,
        }
        Admin.objects.create(**admin_data)
        return user

from rest_framework import serializers
from .models import User

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    image_profil = serializers.ImageField()  # Add image_profil field
    is_admin = serializers.BooleanField()  # Add is_admin field

    class Meta:
        model = User
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'image_profil', 'is_admin']  # Define the default display fields
        read_only_fields = ['pk', 'email']  # Define the read-only fields


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = "__all__"



try:

    from user.models import Parent

except:
    pass 

class ParentSerializer(serializers.ModelSerializer):
    class Meta:

        try:
            model = Parent
        except:
            pass    
        fields = '__all__'

class EleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleve
        fields = ['id', 'user', 'ville', 'adresse', 'prenom', 'nom', 'date_naissance', 'Etablissement', 'niveau_scolaire', 'genre', 'numero_telephone']

class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = ['id', 'user', 'ville', 'prenom', 'nom', 'adresse', 'quartier_résidence', 'numero_telephone', 'experience_enseignement', 'certifications', 'tarif_horaire', 'date_naissance', 'niveau_etude']

class CustomLoginSerializer(LoginSerializer):
    pass

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = '__all__'

       

        



#class TransactionSerializer(serializers.ModelSerializer):
  #  class Meta:
    #    model = Transaction
      #  fields = '__all__'
# serializers.py

