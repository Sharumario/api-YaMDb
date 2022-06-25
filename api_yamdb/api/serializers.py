from django.conf import settings
from rest_framework import relations, serializers

from reviews.validators import validate_username, validate_year
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    User
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')

    def validate_username(self, value):
        return validate_username(value)


class ProfileSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.LENGTH_EMAIL_FIELD,
        required=True
    )
    username = serializers.CharField(
        max_length=settings.LENGTH_USERNAME_FIELD,
        required=True,
        validators=(validate_username,)
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.LENGTH_USERNAME_FIELD,
        required=True,
        validators=(validate_username,)
    )
    confirmation_code = serializers.CharField(
        max_length=settings.LENGTH_CONFIRMATION_CODE,
        required=True
    )


class ReviewSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        title_id = (self.context.get('request').parser_context.
                    get('kwargs').get('title_id'))
        author = self.context.get('request').user
        if Review.objects.filter(title=title_id, author=author).exists():
            raise serializers.ValidationError((
                'Пользователь может написать только один отзыв '
                'на каждое произведение'))
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = relations.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('__all__',)


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        return validate_year(value)
