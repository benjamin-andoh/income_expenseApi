from trial.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

        def validate(self, attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')

            if not username.isalnum():
                raise serializers.ValidationError(
                    "the username should be alpha-numeric"
                )
            return attrs

        def create(self, validated_data):
            return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=222)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=233, min_length=4)
    password = serializers.CharField(max_length=222, min_length=4, write_only=True)
    username = serializers.CharField(max_length=222, read_only=True)
    tokens = serializers.CharField(max_length=222, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        try:
            user = User.objects.get(email=email)
        except Exception:
            raise AuthenticationFailed('user is not registered')

        # if not user:
        #     raise AuthenticationFailed('Invalid credential, Try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled')

        # if not user.is_verified:
        #     raise AuthenticationFailed('Not not')

        if email == user.email:
            return {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens
            }


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerilizer(serializers.Serializer):
    password = serializers.CharField(min_length=4, write_only=True)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']
