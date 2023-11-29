from collections import OrderedDict

from django.shortcuts import render
from django.urls import reverse
from openai import AsyncOpenAI, OpenAI
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.conf import settings

from chatAPI.chatAPI.settings import BASE_DIR

from .models import Chat
from .permissions import UserPermission
from .serializers import ChatSerializer
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
    serializer = self.get_serializer(instance)
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


class ChatAPIView(HateoasModelView):
  queryset = Chat.objects.all()
  serializer_class = ChatSerializer
  permission_classes = [UserPermission]

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    queryset = queryset.filter(user=request.user)

    page = self.paginate_queryset(queryset)
    if page is not None:
      serializer = self.get_serializer(page, many=True)
      return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

  def get_list_links(self, request):
    return [
      {
        'desc': 'Self',
        'href': request.build_absolute_uri(request.path),
        'method': 'GET',
      },
      {
        'desc': 'New Chat',
        'href': request.build_absolute_uri(request.path),
        'method': 'POST'
      }
    ]

  def linkify_list_data(self, request, data):
    for chat in data:
      detail_link = request.build_absolute_uri(reverse('chat-detail', kwargs={'pk': chat['id']}))
      chat['_links'] = [
        create_link('Chat detail', detail_link, 'GET'),
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
    detail_link = request.build_absolute_uri(reverse('chat-detail', kwargs={'pk': data['id']}))

    return [
      create_link('Detail of chat', detail_link, 'GET')
    ]

  def get_update_links(self, request, instance):
    detail_link = request.build_absolute_uri(reverse('chat-detail', kwargs={'pk': instance.pk}))

    return [
      create_link('Detail of chat', detail_link, 'GET')
    ]


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def chatbot(request):
  if request.method == 'POST':
    client = OpenAI(
      api_key=settings.OPENAI_API_KEY
    )
    f = open(BASE_DIR / "chatAPI/quote.txt", 'r')
    data = f.read()
    f.close()

    input = request.POST.get('input')
    prompt = f'드라마 명대사: ${data} "숫자."로 장면이 구분되어 있습니다'
    contents = f'''키워드와 관련된 장면이 있으면 장면을 찾아줘. 키워드는 이중 백틱(``)으로 구분되어 있습니다. ``${input}``.해당하는 결과가 없으면
        '해당 장면을 찾을 수 없습니다'
        를 
        문자열로
        응답
        해줘.결과가
        있으면
        장면번호, 대사, 설명을
        포함하고
        scene, quote, description
        키값을
        사용하는
        json객체
        1
        개로
        해줘
        '''
    chat_completion = client.chat.completions.create(
      messages=[
        {
          "role": "system",
          "content": "assistant는 키워드만 보고 드라마 명장면 명대사를 찾아줍니다."
        },
        {
          "role": "user",
          "content": "스토브리그의 명대사를 알려줘"
        },
        {
          "role": "assistant",
          "content": prompt
        },
        {
          "role": "user",
          "content": contents
        }
      ],
      model="gpt-3.5-turbo",
    )

    return Response(chat_completion.choices[0].message.content, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def delete_chat(request):
  if request.method == 'POST':
    Chat.objects.filter(user=request.user).delete()

  return Response(status=status.HTTP_204_NO_CONTENT)
