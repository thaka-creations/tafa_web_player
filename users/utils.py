import pytz
import jwt
import requests
from copy import deepcopy
from datetime import timedelta, datetime
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import authentication, status
from rest_framework.exceptions import APIException, NotAuthenticated, NotAcceptable, AuthenticationFailed, ErrorDetail
from rest_framework.utils.serializer_helpers import ReturnDict
from oauth2_provider.generators import generate_client_id, generate_client_secret
from oauth2_provider.models import get_application_model
from oauth2_provider.oauth2_backends import get_oauthlib_core
from .models import User

CALLBACK_URL = settings.SERVICES_URLS['callback_url']


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
            'username': user.username,
            'phone': user.phone,
            'name': f'{user.first_name} {user.last_name}',
            'roles': self.get_user_roles(user),
            'exp': access_token_expiry,
            'iat': time,
            "aud": "urn:jst"
        }
        encoded = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm='HS512')
        return encoded


class SystemAuthentication(authentication.BaseAuthentication):

    def __init__(self):
        self.authentication_header_prefix = 'Bearer'

    @staticmethod
    def get_jwt_header(request):
        auth = request.headers.get('JWTAUTH', b'')
        return auth

    def authenticate(self, request):
        request.user = None
        oauthlib_core = get_oauthlib_core()
        valid, r = oauthlib_core.verify_request(request, scopes=[])

        if not valid:
            return None

        jwt_header = self.get_jwt_header(request).split()
        header_prefix = self.authentication_header_prefix.lower()
        if not jwt_header:
            return None
        if len(jwt_header) == 1 or len(jwt_header) > 2:
            raise NotAuthenticated(
                {"message": "Could Not Authenticate User", "status_code": status.HTTP_401_UNAUTHORIZED}
            )

        try:
            prefix = jwt_header[0]
            token = jwt_header[1]
        except Exception:
            raise NotAcceptable(
                {"message": "No Token Present", "status_code": status.HTTP_406_NOT_ACCEPTABLE})

        if prefix.lower() != header_prefix:
            return None
        return self.authenticate_credentials(request, token)

    @staticmethod
    def authenticate_credentials(request, token):
        try:
            decoded = jwt.decode(token, settings.TOKEN_SECRET_KEY, audience="urn:jst", algorithms=['HS512'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(
                {"message": "User Logged Out.Please Try Again",
                 "status_code":
                     status.HTTP_401_UNAUTHORIZED})

        except jwt.InvalidTokenError:
            raise AuthenticationFailed(
                {"message": "Please Login Again",
                 "status_code":
                     status.HTTP_401_UNAUTHORIZED})

        except Exception as e:
            print(e)
            raise AuthenticationFailed(
                {"message": "Invalid Verification",
                 "status_code": status.HTTP_401_UNAUTHORIZED})

        try:
            user = User.objects.get(id=decoded['user'])
        except User.DoesNotExist:

            raise AuthenticationFailed(
                {"message": "Invalid User",
                 "status_code":
                     status.HTTP_401_UNAUTHORIZED})
        return user, token


def verify_otp(otp, send_to):
    url = "https://tafa.co.ke/api/v1/mfa/otp/verify"
    payload = {
        "otp": otp,
        "send_to": send_to
    }
    try:
        response = requests.post(url, json=payload)
    except requests.exceptions.ConnectionError:
        return False, "Connection Error"

    if response.status_code == 200:
        return True, "OTP Verified"
    else:
        return False, response.json()['message']


def format_error(errors):
    if type(errors) == str:
        return errors
    elif (type(errors) == ReturnDict) or (type(errors) == dict):
        return get_error_message_from_dict(dict(errors))
    return get_error_message_from_dict(errors)


def get_error_message_from_dict(error):
    # print("unprocessed error:-> ", error)
    if type(error) == str:
        return error
    finished_processed_errors = []
    list_of_string_objects = [error]
    count = 0
    processing = True
    while processing:
        # print('list_of_string_objects:-> ', list_of_string_objects)
        for index, i in enumerate(list_of_string_objects):
            if type(i) == str:
                finished_processed_errors.append(
                    list_of_string_objects.pop(index))
                continue
            if type(i) == dict:
                # print("object being processed:->", i)
                list_of_string_objects.append(recursive_dict_error(i))
                list_of_string_objects.pop(index)
            elif type(i) == list:
                # print("list in get_error_message_from_dict: deal with it!!! :-> ", error)
                list_of_string_objects.append(recursive_list_error(i))
                list_of_string_objects.pop(index)
            else:
                list_of_string_objects.append(str(i))
                list_of_string_objects.pop(index)
            del i
        count += 1
        if count > 20:
            processing = False
    # print('finished_processed_errors:-> ', finished_processed_errors)
    final_error = ''.join(finished_processed_errors)
    return final_error


def recursive_dict_error(error):
    copy_of_error = deepcopy(error)
    if isinstance(error, dict):
        stored_keys = tuple(copy_of_error.keys())
        string_list_objects = []
        value_ = None
        for i in stored_keys:
            # print('type:-> ', type(copy_of_error[i]))
            if type(copy_of_error[i]) == list:
                # print('type:-> ', tuple(copy_of_error[i]))
                for indiv in copy_of_error[i]:
                    if type(indiv) == ErrorDetail:
                        if i == 'non_field_errors':
                            value_ = str(indiv)
                        else:
                            value_ = str(i) + " : " + str(indiv)
                    else:
                        if i == 'non_field_errors':
                            value_ = recursive_dict_error(indiv)
                        else:
                            value_ = {i: recursive_dict_error(indiv)}
            elif type(copy_of_error[i]) == dict:
                value_ = {i: recursive_dict_error(copy_of_error[i])}
            elif type(copy_of_error[i]) == str:
                value_ = str(i) + " : " + str(copy_of_error[i])
            elif copy_of_error[i] is None:
                pass
            else:
                raise Exception(type(copy_of_error[i]))
        string_list_objects.append(value_)
        # print('string_list_objects:-> ', string_list_objects)
        return string_list_objects
    return error


def recursive_list_error(error):
    if type(error) == list:
        return error[0]
    return error


