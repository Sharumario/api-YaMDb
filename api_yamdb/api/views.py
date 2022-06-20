import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Categories, Genres, Titles
from .mixins import ListCreateDestroyViewSet
from users.models import User
from .permissions import IsAdmin, ReadOnly
from .serializers import (ProfileSerializer, UserSerializer,
                          SignupSerializer, TokenSerializer,
                          CategoriesSerializer, GenreSerializer,
                          TitleSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['get', 'patch'], detail=False, url_path='me',
            permission_classes=(IsAuthenticated,))
    def profile(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'PATCH':
            serializer = ProfileSerializer(
                user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


@api_view(['POST'])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    confirmation_code = ''.join(random.sample('0123456789', 8))
    if serializer.is_valid():
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        if (User.objects.filter(email__iexact=email).
                exclude(confirmation_code__exact='').exists()):
            return Response('Этот адрес электронной почты уже используются',
                            status=status.HTTP_400_BAD_REQUEST)
        if (User.objects.filter(username__iexact=username).
                exclude(confirmation_code__exact='').exists()):
            return Response('Это имя пользователя уже используются',
                            status=status.HTTP_400_BAD_REQUEST)
        user, _ = User.objects.get_or_create(
            username=username,
            email=email
        )
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            'Код подтверждения YaMDb',
            f'Ваш код подтверждения: {confirmation_code}',
            'signup@yamdb.com',
            [email],
            fail_silently=False
        )
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=serializer.data['username'])
        if serializer.data['confirmation_code'] == user.confirmation_code:
            return Response(
                {'token': str(RefreshToken.for_user(user).access_token)},
                status=status.HTTP_201_CREATED
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_permissions(self):
        if self.action == 'retrieve' or 'list':
            return (ReadOnly(),)
        return super().get_permissions()
