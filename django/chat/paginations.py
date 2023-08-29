from rest_framework.pagination import CursorPagination, PageNumberPagination


class MessagePagination(CursorPagination):
    page_size = 20
    ordering = "-created_at"


class RoomPagination(PageNumberPagination):
    page_size = 20
