from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict

from rest_framework.response import Response


class ExtraLinksAwarePageNumberPagination(PageNumberPagination):
  page_size = 5
  page_size_query_param = 'per_page'
  def get_paginated_response(self, data, links=[]):
    return Response(OrderedDict([
      ('count', self.page.paginator.count),
      ('next', self.get_next_link()),
      ('previous', self.get_previous_link()),
      ('results', data),
      ('_links', links),
    ]))