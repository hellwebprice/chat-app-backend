from chat.views import MessageListCreateView, RoomListCreateView, RoomRetrieveView
from django.urls import path

urlpatterns = [
    path("room/", RoomListCreateView.as_view()),
    path("room/<str:pk>/", RoomRetrieveView.as_view()),
    path("message/", MessageListCreateView.as_view()),
]
