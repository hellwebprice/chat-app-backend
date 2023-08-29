from django.urls import path

from .views import FriendListUpdateView, UserListView

urlpatterns = [
    path("friend/", FriendListUpdateView.as_view()),
    path("user/", UserListView.as_view()),
]
