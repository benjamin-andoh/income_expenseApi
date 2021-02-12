import jwt
from django.conf import settings
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from trial.models import User
from trial.renderers import UserRenderer
from trial.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
    ResetPasswordRequestSerializer, SetNewPasswordSerilizer
from trial.utils import Utils
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = UserRenderer,

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relative_link = reverse('email-verify')

        abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)

        email_body = "Hi" + user.username + "use the link to verify your email\n" + abs_url

        data = {
            'to': user.email,
            'body': email_body
        }

        # Utils.send_email(data)

        return Response({'token': user.tokens()}, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successful activation'}, status=status.HTTP_201_CREATED)
        except jwt.ExpiredSignatureError:
            return Response({'Error': ' Activation Expired'}, status=status.HTTP_404_NOT_FOUND)
        except jwt.exceptions.DecodeError:
            return Response({'Error': ' Invalid token '}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(
                request=request).domain

            relative_link = reverse('password_reset_confirm',
                                    kwargs={'uid64': uid64,
                                            'token': token}
                                    )

            abs_url = 'http://' + current_site + relative_link

            email_body = "Hello, \n use the link to reset your password\n" + abs_url

            data = {
                'to': user.email,
                'body': email_body,
                'subject': 'reset your password'
            }
            # Utils.send_email(**data)
        return Response({
            'to': user.email,
            'body': email_body,
            'subject': 'reset your password'
        },
            # {'success': 'we have sent you a link to reset your password'},
            status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uid64, token):
        try:
            # uid64 contains the user 
            id = smart_str(urlsafe_base64_decode(uid64))
            user = User.objects.get(id=id)

            # the user should not use the rest kay the second time
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid , please request a new one'})

            return Response({'success': True,
                             'message': 'Credentials valid',
                             uid64: uid64, token: token},
                            status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid , please request a new one'})


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerilizer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            password = request.data['password']
            token = request.data['token']
            uidb46 = request.data['uidb46']

            id = force_str(urlsafe_base64_decode(uidb46))

            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('the reset link is invalid', 401)

            user.set_password(password)
            user.save()

        except Exception:
            raise AuthenticationFailed('the reset link is invalid', 401)

        return Response({'success': True, 'message': 'password reset success'},
                        status=status.HTTP_200_OK)
