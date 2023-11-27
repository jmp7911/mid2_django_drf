from django.test import TestCase, Client
from .models import Chat
from dotenv import load_dotenv
from django.contrib.auth import get_user_model

import os
import asyncio
from openai import AsyncOpenAI, OpenAI

load_dotenv()


User = get_user_model()

# Create your tests here.
class ChatTest(TestCase):
  def setUp(self):
    self.client = Client(
      headers={
        'Content-Type': 'application/json'
      }
    )

    self.LoginInfo = {
      'email': 'jmp7911@gmail.com',
      'password': '1234'
    }

    self.user = User.objects.create(
      email='test@example.com',
      password='12345678!'
    )

    print(self.user)
    chat001 = Chat.objects.create(
      prompt= 'prompt',
      user= self.user
    )

  def test_chatbot(self):
    """
    /chat/api/ 엔드포인트 post 테스트
    """
    data = {
      'input': '파벌싸움 성적으로 하세요'
    }
    res = self.client.post('http://localhost:8000/chat/api/', data=data)
    print(res.json())
  def test_chat(self):
    """
    채팅목록 페이지 접속
    내 채팅 가져오기
    새로운 채팅
    채팅 내역 삭제
    """

    client = OpenAI(
      # defaults to os.environ.get("OPENAI_API_KEY")
      api_key=os.getenv('OPENAI_API_KEY'),
    )
    f = open("quote.txt", 'r')
    data = f.read()
    f.close()


    input = '파벌싸움 성적으로 하세요'
    prompt = f'드라마 명대사: \`\`\`${data}\`\`\` "숫자."로 장면이 구분되어 있습니다'
    contents = f'''키워드와 관련된 장면이 있으면 장면 전체를 찾아줘. 키워드는 이중 백틱(\`\`)으로 구분되어 있습니다. \`\`${input}\`\`.해당하는 결과가 없으면
    '해당 장면을 찾을 수 없습니다'
    를
    문자열로
    응답
    해줘.결과가
    있으면
    씬
    단위로
    문장을
    제외하고
    장면번호, 대사를
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
    print(chat_completion.choices[0].message.content)
    chat_data = {
      'prompt': input,
      'user': '1'
    }
    answer_data = {
      'prompt': chat_completion.choices[0].message.content,
      'user': '1'
    }
    print(chat_data)
    res = self.client.post('http://localhost:8000/chat/model/', data=chat_data)

    print(res.json())






