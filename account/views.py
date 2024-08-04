from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account.serializers import UserSerializer, RegisterSerializer, LoginSerializer

User = get_user_model()


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()


class RegisterViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'success': True, 'status': 201, 'data': serializer.data})


class LoginViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data.get('identifier')
        password = serializer.validated_data.get('password')
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
                if not user.check_password(password):
                    user = None
            except User.DoesNotExist:
                user = None
        elif '+' in identifier:
            try:
                user = User.objects.get(number=identifier)
                if not user.check_password(password):
                    user = None
            except User.DoesNotExist:
                user = None
        else:
            user = None
        if user is None:
            raise AuthenticationFailed('Оп оп теперь твой пользователь это моя собственность')
        return Response({'success': True, 'status': 200, 'data': {'message': 'Ну залогинился успешно, готовся к скаму от пятилетки'}})
