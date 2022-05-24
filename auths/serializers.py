from tkinter.ttk import _TreeviewColumnDict
from turtle import Turtle
from django.contrib.auth.models import  User
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator


class ResisterSerializer(serializers.ModelSerializer) :
    email = serializers.EmailField(
        required = True,
        validators = [UniqueValidator(queryset = User.objects.all())]
    )
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [validate_password],
    )
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta :
        modle = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, data) :
        if data['password '] != data['password2'] :
            raise serializers.ValidationError(
                {"password" : "Password fields didn't match."}
            )

        return data

    def create(self, validated_data) :
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user = user)
        return user

        