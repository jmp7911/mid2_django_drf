from collections import OrderedDict

from django.shortcuts import render
from django.urls import reverse
from openai import AsyncOpenAI, OpenAI
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from .models import Quote
from .permissions import UserPermission
from .serializers import QuoteSerializer, QuoteUserSerializer
from .paginator import ExtraLinksAwarePageNumberPagination


def create_link(desc, href, method=None):
  result = {
    'desc': desc,
    'href': href,
  }
  if method:
    result['method'] = method
  return result


class HateoasModelView(ModelViewSet):
  pagination_class = ExtraLinksAwarePageNumberPagination

  def get_list_links(self, request):
    return {}

  def get_paginated_response(self, data, links=None):
    assert self.paginator is not None
    return self.paginator.get_paginated_response(data, links)

  def linkify_list_data(self, request, data):
    return data

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      data = self.linkify_list_data(request, serializer.data)
      return self.get_paginated_response(data, links=self.get_list_links(request))

    serializer = self.get_serializer(queryset, many=True)
    data = self.linkify_list_data(request, serializer.data)

    return Response(OrderedDict([
      ('results', data),
      ('_links', self.get_list_links(request))
    ]))

  def get_retrieve_links(self, request, instance):
    return {}

  def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = QuoteUserSerializer(instance)
    data = serializer.data
    data['_links'] = self.get_retrieve_links(request, instance)
    return Response(data)

  def get_update_links(self, request, instance):
    return {}

  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    data = serializer.data
    data['_links'] = self.get_update_links(request, instance)
    return Response(data)

  def get_create_links(self, request, data):
    return {}

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    data = serializer.data
    data['_links'] = self.get_create_links(request, serializer.data)
    return Response(data, status=status.HTTP_201_CREATED, headers=headers)

  def get_destroy_links(self, request, instance):
    return {}

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    data = {'_links': self.get_destroy_links(request, instance)}
    self.perform_destroy(instance)
    return Response(data, status=status.HTTP_204_NO_CONTENT)


class QuoteAPIView(HateoasModelView):
  queryset = Quote.objects.all()
  serializer_class = QuoteSerializer
  permission_classes = [UserPermission]

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      data = self.linkify_list_data(request, serializer.data)
      return self.get_paginated_response(data, links=self.get_list_links(request))

    serializer = self.get_serializer(queryset, many=True)
    data = self.linkify_list_data(request, serializer.data)

    return Response(OrderedDict([
      ('results', data),
      ('_links', self.get_list_links(request))
    ]))

  def get_list_links(self, request):
    return [
      {
        'desc': 'Self',
        'href': request.build_absolute_uri(request.path),
        'method': 'GET',
      },
      {
        'desc': 'New Quote',
        'href': request.build_absolute_uri(request.path),
        'method': 'POST'
      }
    ]

  def linkify_list_data(self, request, data):
    for quote in data:
      detail_link = request.build_absolute_uri(reverse('quote-detail', kwargs={'pk': quote['id']}))
      quote['_links'] = [
        create_link('Quote detail', detail_link, 'GET'),
      ]
    return data

  def get_retrieve_links(self, request, instance):
    self_link = request.build_absolute_uri(request.path)

    return [
      create_link('Self', self_link, 'GET'),
      create_link('Update self', self_link, 'PUT'),
      create_link('Delete self', self_link, 'DELETE'),
    ]

  def get_create_links(self, request, data):
    detail_link = request.build_absolute_uri(reverse('quote-detail', kwargs={'pk': data['id']}))

    return [
      create_link('Detail of quote', detail_link, 'GET')
    ]

  def get_update_links(self, request, instance):
    detail_link = request.build_absolute_uri(reverse('quote-detail', kwargs={'pk': instance.pk}))

    return [
      create_link('Detail of quote', detail_link, 'GET')
    ]

