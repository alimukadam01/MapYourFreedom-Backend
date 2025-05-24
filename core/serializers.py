from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer, 
    UserSerializer as BaseUserSerializer,
    PasswordRetypeSerializer
)
from djoser import utils
from djoser.conf import settings

from core.models import Book

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name',)


class SimpleUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.SerializerMethodField()
    email = serializers.EmailField()

    def get_name(self, user):
        return f'{str(user.first_name)} {str(user.last_name)}'


class UserSerializer(BaseUserSerializer):

    has_ev_access = serializers.BooleanField()
    has_sv_access = serializers.BooleanField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
                settings.LOGIN_FIELD,
                settings.USER_ID_FIELD,
                "password",
                'has_ev_access',
                'has_sv_access'
            )

class CustomPasswordResetConfirmRetypeSerializer(PasswordRetypeSerializer, serializers.Serializer):
    uid = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    def create(self, validated_data):
        try:
            uid = utils.decode_uid(self.context['view'].kwargs.get('uid'))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            key_error = "invalid_uid"
            raise ValidationError(
                {"uid": [self.error_messages[key_error]]}, code=key_error
            )
        
        is_token_valid = self.context["view"].token_generator.check_token(
            user, self.context['view'].kwargs.get('token')
        )
        
        if is_token_valid:
            user.set_password(validated_data['new_password'])
            user.save()
            return user
        else:
            key_error = "invalid_token"
            raise ValidationError(
                {"token": [self.error_messages[key_error]]}, code=key_error
            )


class BookSerializer(serializers.ModelSerializer):

    has_book_access = serializers.SerializerMethodField()

    def get_has_book_access(self, obj):

        permission_mapping = {
            'english': 'has_ev_access',
            'spanish': 'has_sv_access'
        }

        return self.context.get(permission_mapping[obj.language], False)

    class Meta:
        model = Book
        fields = ['id', 'name', 'price', 'language', 'path', 'has_book_access']   