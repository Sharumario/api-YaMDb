from django.shortcuts import get_object_or_404
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError
)

from reviews.models import Comment, Review, Title
from users.models import User


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(Serializer):
    email = EmailField(max_length=254, required=True)
    username = CharField(max_length=150, required=True)

    class Meta:
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Использовать имя "me" запрещено')
        return value


class TokenSerializer(Serializer):
    username = CharField(max_length=150, required=True)
    confirmation_code = CharField(max_length=8, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')


class ReviewSerializer:
    """Сериализатор для отзывов."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

        def validate(self, data):
            title_id = self.context.get('request').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            author = self.context.get('request').user
            if Review.objects.get(title=title, author=author):
                raise ValidationError((
                    'Пользователь может написать только один отзыв '
                    'на каждое произведение'))
            return data


class CommentSerializer:
    """Сериализатор для комментриев к отзывам."""

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
