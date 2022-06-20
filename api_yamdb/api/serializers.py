from django.shortcuts import get_object_or_404

from rest_framework import serializers

from users.models import User
from reviews.models import Categories, Genres, Titles, GenreTitle


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
            current_genre = get_object_or_404(Genres, **genre)
            GenreTitle.objects.get_or_create(
                genre=current_genre, title=title
            )
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        # instance.genre = validated_data.get('genre', instance.genre)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()
        return instance
