from rest_framework import serializers
from .models import Appointment, Speciality, Qualification, Doctor, BookAppointment


# DoctorSerializer
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        extra_kwargs = {
            "id": {"read_only": True},
            "profile_photo": {"required": True},
            "registration_number": {"required": True},
            "qualification_id": {"required": True},
            "clinic_name": {"required": True},
            "clinic_registration_number": {"required": True},
            "digital_signature": {"read_only": True},
            "address_proof_of_clinic_regetration": {"required": True},
            "degree_certificate": {"required": True},
            "doctor_regestration_no_proof": {"required": True},
            "clinic_regestration_certificate": {"required": True},
            "bio": {"required": True},
            "specilization_id": {"required": True},
            "experience_years": {"required": True},
        }


class ViewDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

# update profile


class UpdateDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        # fields = ['id', 'name', 'email', 'mobile', 'document','registration_number','clinic_name','clinic_registration_number','bio','experience',]

    def validate_email(self, value):
        user = self.context['request'].user
        if Doctor.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.email = validated_data['email']
        instance.mobile = validated_data['mobile']
        instance.document = validated_data['document']
        instance.registration_number = validated_data['registration_number']
        instance.clinic_name = validated_data['clinic_name']
        instance.clinic_registration_number = validated_data['clinic_registration_number']
        instance.bio = validated_data['bio']
        instance.experience = validated_data['experience']
        instance.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'


class BookAnAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookAppointment
        fields = '__all__'
