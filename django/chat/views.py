from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Message, Room
from .paginations import MessagePagination
from .serializers import (
    MessageCreateSerializer,
    RoomCreateSerializer,
    RoomListSerializer,
    RoomRetrieveSerializer,
    RoomUpdateSerializer,
)


class RoomCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter_by_user(user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomListSerializer
        return RoomCreateSerializer


class RoomRetrieveView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return RoomRetrieveSerializer
        return RoomUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter_by_user(user)


class MessageListCreateView(ListCreateAPIView):
    serializer_class = MessageCreateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["room"]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.accessed_by_user(user)
