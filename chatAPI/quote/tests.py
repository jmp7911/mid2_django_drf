from django.contrib.auth.models import User
from django.test import TestCase, Client


class QuoteTest(TestCase):
  def setUp(self):
    self.client = Client(
      headers={
        'Content-Type': 'application/json'
      }
    )

    self.user = User.objects.create(username='test', email='exam@test.com', password='1234')
    self.quote0001 = {
      'title': 'title',
      'content': 'content',
      'user': '1',
      'is_apply': 'False',
      'description': 'description',
    }

  def test_quote(self):
    """
    모든 페이지 접속 가능 확인
    """
    res = self.client.get('http://localhost:8000/quote/')
    self.assertEquals(res.status_code, 200)

    res = self.client.post('http://localhost:8000/quote/', self.quote0001)
    print(res.json())
    self.assertEquals(res.status_code, 201)

    res = self.client.get('http://localhost:8000/quote/1')
    self.assertNotEquals(res.status_code, 404)

    res = self.client.delete('http://localhost:8000/quote/1')
    self.assertEquals(res.status_code, 204)
