from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.serializers import UserSerializer
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .paginations import FriendPagination
from .serializers import FriendUpdateSerializer, UserListSerializer


class FriendListUpdateView(ListAPIView, UpdateAPIView):
    model = get_user_model()
    pagination_class = FriendPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

    def get_queryset(self):
        if pk := self.request.parser_context["kwargs"].get("pk"):
            user = get_object_or_404(get_user_model(), pk=pk)
        else:
            user = self.request.user
        return user.get_friends()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return FriendUpdateSerializer

    def get_object(self):
        return self.request.user


class FriendRequestListView(ListAPIView, UpdateAPIView):
    model = get_user_model()
    pagination_class = FriendPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]

    def get_queryset(self):
        user = self.request.user
        return user.get_friend_requests()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return UserSerializer
        return FriendUpdateSerializer

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    queryset = get_user_model().objects.all()
    model = get_user_model()
    serializer_class = UserListSerializer
    pagination_class = FriendPagination
    filter_backends = [SearchFilter]
    search_fields = ["username", "email"]
