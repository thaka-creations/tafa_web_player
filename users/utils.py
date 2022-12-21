import pytz
import jwt
import requests
from datetime import timedelta, datetime
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import APIException
from oauth2_provider.generators import generate_client_id, generate_client_secret
from oauth2_provider.models import get_application_model

CALLBACK_URL = settings.SERVICES_URLS['callback_url']


class UserManager(BaseUserManager):
    def create_user(self, username, is_staff, password=None):
        if not username:
            raise ValueError("Enter a valid username")

        user = self.model(
            username=username,
            is_staff=True,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username, is_staff=True, password=password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

        return user


class ApplicationUser:

    @staticmethod
    def create_application_user(user):
        with transaction.atomic():
            username = user.username
            try:
                data = {
                    'client_id': generate_client_id(),
                    'client_secret': generate_client_secret(),
                    'client_type': 'confidential',
                    'skip_authorization': False,
                    'name': username,
                    'user': user,
                    'redirect_uris': '',
                    'authorization_grant_type': 'password'
                }

                get_application_model().objects.create(**data)
            except Exception as e:
                raise APIException(e)

    @staticmethod
    def get_client_details(payload):
        url = CALLBACK_URL + 'o/token/'
        resp = requests.post(url, data=payload)

        if resp.status_code == 200:
            return resp.json()
        return False

    @staticmethod
    def logout(token, user_id):
        try:
            user_details = get_application_model().objects.get(user_id=user_id)
        except (ValidationError, ObjectDoesNotExist):
            return False, "User does not exist"
        revoke_url = CALLBACK_URL + 'o/revoke_token/'
        payload_data = {
            'token': token,
            'client_id': user_details.client_id,
            'client_secret': user_details.client_secret,
        }
        response = requests.post(revoke_url, data=payload_data)
        if response.status_code == 200:
            return True, "Logout Successful"
        return False, "Could Not Log you Out"

    @staticmethod
    def get_user_roles(user):
        user_roles = [role.name for role in user.groups.all()]
        return user_roles

    def generate_jwt_token(self, user):
        timezone = pytz.timezone(settings.TIME_ZONE)
        time = datetime.now(tz=timezone)
        access_token_expiry = time + timedelta(seconds=int(settings.ACCESS_TOKEN_EXPIRY))

        payload = {
            'user': str(user.id),
            'roles': self.get_user_roles(user),
            'exp': access_token_expiry,
            'iat': time,
            "aud": "urn:jst"
        }
        encoded = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm='HS512')
        return encoded

