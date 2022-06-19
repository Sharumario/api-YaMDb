import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdmin, OwnerOrReadOnly
from api.serializers import (
    CommentSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer
)
from reviews.models import Review, Title
from users.models import User


class UserViewSet(ModelViewSet):
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
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        user.confirmation_code = confirmation_code
        user.save()
        if created or user.confirmation_code is not None:
            send_mail(
                'Код подтверждения YaMDb',
                f'Ваш код подтверждения: {confirmation_code}',
                'signup@yamdb.com',
                [email],
                fail_silently=False
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
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


class ReviewViewSet(ModelViewSet):
    """Вьюсет для отзывов на произведения."""
    serializer_class = ReviewSerializer
    permission_classes = OwnerOrReadOnly
    filter_backends = (SearchFilter,)
    search_fields = ('text',)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return Review.objects.filter(title=title.id)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ReviewViewSet):
    """Вьюсет для комментриев к отзыву."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return Review.objects.filter(review=review.id)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
