from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import UserModel

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']



    def validate_password(self, password):
        validate_password(password, self.instance)
        return password


    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        return user



class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'profile_image', 'date_joined']