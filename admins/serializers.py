from dataclasses import field
from rest_framework import serializers
from .models import *
from doctor.models import DoctorRatingReview



class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorRatingReview
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
       


    # def create(self, validated_data):
    #     return Location.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.section = validated_data.get('section', instance.section)
    #     instance.is_cat = validated_data.get('is_cat', instance.is_cat)
    #     instance.save()
    #     return instance

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'icon']

    def create(self, validated_data):
        return Speciality.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.icon = validated_data.get('icon', instance.icon)
        instance.save()
        return instance


class QualificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qualification
        fields = ['id', 'name', ]

    def create(self, validated_data):
        return Qualification.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

