from django.urls import path, re_path

from .views import FriendListUpdateView, FriendRequestListView, UserViewSet

urlpatterns = [
    re_path(r"^users/friend/(?:(?P<pk>[0-9]+)/)?$", FriendListUpdateView.as_view()),
    path("users/friend/request/", FriendRequestListView.as_view()),
    path("users/", UserViewSet.as_view({"get": "list", "post": "create"})),
]
