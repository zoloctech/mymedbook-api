from dataclasses import field, fields
from tokenize import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Roles, TempData
from knox.models import AuthToken
from rest_framework.validators import UniqueTogetherValidator
from doctor.models import Doctor, DoctorRatingReview

User = get_user_model()


# Create your serializers here.

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'
        read_only_fields = ['id']
        validators = [
            UniqueTogetherValidator(
                queryset=Roles.objects.all(),
                fields=['role',],
                message="Role already exists"
            )
        ]
        
    def create(self, validated_data):
        if validated_data['role'] == 'admin':
            raise serializers.ValidationError('admin is a reserved role')
        return Roles.objects.create(**validated_data)



class TempDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempData
        fields = '__all__'
        read_only_fields = ['id']


class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# UserSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fname", "lname", "phone" ,"email","address"]


# RegisterSerializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "fname", "lname", "phone" ,"email","state","city","area"]
        extra_kwargs = {
            "id": {"read_only": True},
            "email": {"required": True},
            "phone": {"required": True},
            "lname": {"required": True},
            "fname": {"required": True},
        }

class DoctorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRatingReview
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True},
            "user": {"required": True},
            "doctor": {"required": True},
            "rating": {"required": True},
            "review": {"required": True},
        }