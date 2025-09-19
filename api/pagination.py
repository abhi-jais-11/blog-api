from rest_framework.pagination import CursorPagination

class PostCursorPagination(CursorPagination):
    page_size = 10
    ordering = "-created_at"   # default sort; cursor will be based on created_at
    cursor_query_param = "cursor"
