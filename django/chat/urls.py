from chat.views import MessageListCreateView, RoomCreateView, RoomRetrieveView
from django.urls import path

urlpatterns = [
    path("room/", RoomCreateView.as_view()),
    path("room/<str:pk>/", RoomRetrieveView.as_view()),
    path("message/", MessageListCreateView.as_view()),
]
