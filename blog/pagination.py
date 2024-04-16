from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class BlogPostPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class LikePagination(BlogPostPagination):
    page_size = 20