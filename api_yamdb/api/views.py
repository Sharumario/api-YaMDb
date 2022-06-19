import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from api.permissions import IsAdmin
from api.serializers import (ProfileSerializer,
                             UserSerializer,
                             SignupSerializer,
                             TokenSerializer)


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
            return Response(serializer.data,
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
        # if created or user.confirmation_code is not None:
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
