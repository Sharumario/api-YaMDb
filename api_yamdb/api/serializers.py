import datetime as dt

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
from reviews.models import Categories, Genres, Titles, GenreTitle


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

class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = GenreSerializer(many=True)

    class Meta:
        model = Titles
        fields = ('name', 'year', 'description', 'category', 'genre')

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        title = Titles.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genres.objects.get(**genre)
            GenreTitle.objects.create(
                genre=current_genre, title=title
            )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()
        return instance

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError('Проверьте год выпуска!')
        return value
