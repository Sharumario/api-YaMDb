import datetime as dt

from django.shortcuts import get_object_or_404

from rest_framework import relations, serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.models import User


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    class Meta:
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Использовать имя "me"'
                                              ' запрещено')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=8, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name',
                  'bio', 'role')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""
    author = relations.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    # def validate(self, data):
    #     title_id = self.context.get('request').kwargs.get('title_id')
    #     title = get_object_or_404(Title, id=title_id)
    #     author = self.context.get('request').user
    #     if Review.objects.get(title=title, author=author):
    #         raise serializers.ValidationError((
    #             'Пользователь может написать только один отзыв '
    #             'на каждое произведение'))
    #     return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментриев к отзывам."""
    author = relations.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        # read_only_fields = ('id', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


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
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value
