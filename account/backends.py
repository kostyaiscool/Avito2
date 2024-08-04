import logging
import datetime

import jwt
from django.contrib.auth.models import AnonymousUser

from django.utils import translation, deprecation
from rest_framework import authentication, exceptions
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from account.models import User, ActiveSession


# class ActiveSessionAuthentication(authentication.BaseAuthentication):
#
#     def authenticate(self, request):
#         request.user = None
#
#         auth_header = authentication.get_authorization_header(request)
#
#         if not auth_header:
#             return None
#
#         # Ensure the token is in the correct format
#         auth_header = auth_header.decode("utf-8")
#         if auth_header.startswith("Bearer "):
#             token = auth_header.split(" ")[1]
#         else:
#             raise exceptions.AuthenticationFailed(
#                 status=403,
#                 message=_("Provided token is not bearer"),
#                 system=True,
#             )
#         return self._authenticate_credentials(request, token)
#
#     def _authenticate_credentials(self, request, token):
#         try:
#             decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         except jwt.ExpiredSignatureError:
#             # Token expired, check if session is still active
#             try:
#                 active_session = ActiveSession.objects.get(token=token)
#                 if active_session.is_active():
#                     # Generate a new token
#                     new_token = self._generate_jwt_token(active_session.user)
#                     active_session.token = new_token
#                     active_session.save(request=request)
#                     request.META['HTTP_AUTHORIZATION'] = f"Bearer {new_token}"
#                     return active_session.user, new_token
#                 else:
#                     raise exceptions.AuthenticationFailed(
#                         status=403,
#                         message=_("Session has expired"),
#                         system=True,
#                     )
#             except ActiveSession.DoesNotExist:
#                 raise exceptions.AuthenticationFailed(
#                     status=403,
#                     message=_("Session does not exist"),
#                     system=True,
#                 )
#
#         except jwt.InvalidTokenError:
#             raise exceptions.AuthenticationFailed(
#                 status=403,
#                 message=_("Provided token is invalid"),
#                 system=True,
#             )
#
#         try:
#             active_session = ActiveSession.objects.get(token=token)
#         except ActiveSession.DoesNotExist:
#             raise exceptions.AuthenticationFailed(
#                 status=403,
#                 message=_("User is not logged on"),
#                 system=True,
#             )
#
#         try:
#             user = active_session.user
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed(
#                 status=401,
#                 message=_("No user matching this token was found"),
#                 system=True,
#             )
#
#         if not user.is_active:
#             raise exceptions.AuthenticationFailed(
#                 status=403,
#                 message=_("This user has been deactivated"),
#                 system=True,
#             )
#
#         return user, token
#
#     def _generate_jwt_token(user):
#         dt = datetime.datetime.now() + datetime.timedelta(seconds=settings.JWT_EXPIRATION_DELTA)
#         token = jwt.encode({
#             'id': user.id,
#             'exp': int(dt.strftime('%s'))
#         }, settings.SECRET_KEY, algorithm='HS256')
#         return token
class ActiveSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('No such user')

        return (user, None)