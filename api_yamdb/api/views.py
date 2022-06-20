import random

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.mixins import ListCreateDestroyViewSet
from api.permissions import IsAdmin, OwnerOrReadOnly, ReadOnly
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SignupSerializer,
    TitleViewSerializer,
    TitleSerializer,
    TokenSerializer,
    UserSerializer
)
from reviews.models import Category, Genre, Title
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (SearchFilter,)
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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = (OwnerOrReadOnly,)
    # filter_backends = (SearchFilter,)
    # search_fields = ('text',)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()
        # return Review.objects.filter(title=title.id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментриев к отзыву."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        # review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()
        # return Review.objects.filter(review=review.id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    # def get_permissions(self):
    #     if self.action in ('retrieve', 'list'):
    #         return (ReadOnly(),)
    #     return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleViewSerializer
        return TitleSerializer
