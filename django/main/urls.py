from django.urls import path

from .views import FriendListUpdateView, FriendRequestListView, UserListView

urlpatterns = [
    path("users/friend/", FriendListUpdateView.as_view()),
    path("users/friend/request/", FriendRequestListView.as_view()),
    path("users/", UserListView.as_view()),
]
