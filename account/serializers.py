import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'number', 'name', 'avatar')


class RegisterSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=5, max_length=15, write_only=True)
    email = serializers.EmailField(required=True)
    number = serializers.CharField(required=False, min_length=8, max_length=20, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'number', 'name', 'avatar', 'password')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        number = attrs.get('number')
        if email:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError('Зач ты неправильно написал, иди обратно на урок информатики')
            if User.objects.filter(email = email).exists():
                raise ValidationError('ЗАНЯТО НАХУ*')
        if number:
            phone_regex = re.compile(r'^\+?1?\d{8,20}$')
            if not phone_regex.match(str(number)):
                raise ValidationError('Тебе либо 5 лет и ты думаешь что умный, либо ты ввёл всё правильно но по ошыбке '
                                      'тебе выдало ошибку, свяжись с поддержкой если это так')
            if User.objects.filter(number = number).exists():
                raise ValidationError('ЗАНЯТО НАХУ')
        if password:
            if len(password) > 15:
                raise ValidationError('Конечно круто что у тебя нет проблем с памятью, но больше 15 символов нельзя')
            elif len(password) < 5:
                raise ValidationError('МНе жаль то что проблем с памятью у тебя больше чем у меня, но как минимум 5 символов')

        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(
            number=validated_data['number'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(min_length=5, max_length=15, write_only=True)

class ChangePassSerializer(serializers.Serializer):
    class Meta:
        fields = ('old password', 'new password')

class ChangeEmailSerializer(serializers.Serializer):
    class Meta:
        fields = ('password', 'old email', 'new email')

class ChangeNumberSerializer(serializers.Serializer):
    class Meta:
        fields = ('password', 'old number', 'new number')