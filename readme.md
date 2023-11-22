# ChatGPT를 이용한 챗봇 애플리케이션
드라마 스토브리그의 명대사를 찾아 봅시다. OpenAI ChatGPT API


## 목차
1. 요구사항
2. 프로젝트 구조
3. 데이터베이스 구조
4. 기능명세서
5. 화면설계
6. 관련 이슈
7. 회고

---

## 요구사항 명세
- 프로젝트 일정: **11월 21일(화) ~ 11월 30일(목)**
- DRF(Django Rest Framework)를 이용하여 서버를 구현합니다. 
- 로그인/회원가입을 구현합니다.
- ChatGPT로 요청을 보내주는 API를 Django내에 구현합니다.
    - (기존JS를 이용한방식) 프론트엔드에서 OpenAI API로 요청을 보냄
        - 프론트엔드 → OpenAI api 로 요청 → 응답값 프론트엔드에 반영
    - (변경해야 할 사항) 프론트엔드에서 Django서버를 통해 요청을 보내줍니다.
        - 프론트엔드 → Django서버 → Django서버에서 OpenAI api 로 요청 → Django서버에서 응답 받고 프론트엔드로 전달 → 응답값 프론트엔드에 반영
- 챗봇 API는 로그인을 한 유저만 사용가능합니다.
- 각 user 당 하루 5번만 요청할 수 있도록 구현합니다.
- 채팅을 데이터베이스에 저장합니다.
- 저장된 채팅 내역을 조회 할 수 있도록 구현합니다.
- 저장된 채팅 내역은 로그인한 본인만 볼 수 있습니다.
- (권장) 개인 도메인 등록, 프론트엔드, 백엔드 배포: https 추가하기 + front 따로 배포
    
    <aside>
    💡 https를 직접 진행하기 위해서는 도메인 구매가 필요합니다! 추가 점수는 아니니 상황에 맞게 선택해주세요.
    
    </aside>
    
    1. 내 서버에 https 적용하기
        
        keyword - domain 등록, https, nameserver, dns, let’s-encripts
        
        - 서버에 https를 적용하는 방법은 아래 페이지에서 배포하기(lightsail) 챕터를 참고해보세요 :)
            - [나의 MBIT(My Best IT personalities) Page 만들기!](https://www.notion.so/da22ebf1642c400cbb9cd4020649a1a7?pvs=21)
    2. 내 github-page를 http로 배포하기
        - github-page에서 커스텀 도메인을 등록한 후 github-page의 EnforceHTTPS 설정을 해제하고 http로 접속해보세요
- kakao, github 등 OAuth2 연결해보기

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title       챗봇 어플리케이션
    excludes    weekends
    %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)

    section  전체
    요구사항 분석            :done,    des1, 2023-11-21, 0d
    데이터베이스 설계         :done,  des, 2023-11-21, 0d
    기능명세서 작성         :done,  des2, 2023-11-21, 2d
    서버환경 생성         :done,  des3, 2023-11-21, 1d
    개발                   :active, des4, after des2, 5d
    프레젠테이션             :des5, after des4, 2d

    section  개발
    FE            : active,   dev1, after des3, 1d
    회원가입 / 로그인 구현 :   dev2, after dev1, 1d
    chat with GPT 구현 :   dev3, after dev2, 1d
    prompt 요청/관리 구현 :   dev4, after dev3, 1d 
    social account 구현 :   dev5, after dev4, 1d 

    
    
```
---

### 개발환경 및 기술

<div style="display:inline-block;">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white">
    <img src="https://img.shields.io/badge/AWS Cloud-232F3E?style=for-the-badge&logo=amazon&logoColor=white">
</div>

---

### 프로젝트 구조

---

### 데이터베이스 구조
```mermaid
erDiagram
    user ||--o{ chat : has
    user {
      integer id PK
      varchar email
      varchar nickname
      varchar password
      datetime created_at
      varchar ip_address
      datetime last_login
    }
    chat {
      integer id PK
      integer user FK
      text content
      datetime created_at
      datetime updated_at
      chat chat_reply FK
    }
    user ||--o{ quote : has
    quote {
      integer id PK
      integer user FK
      text content
      boolean is_apply
      datetime created_at
      datetime updated_at
      datetime applied_at
    }
    
```
---

### 기능명세서
- **기본url** : 52.78.247.51:8000
- **Content-Type** : application/json
- 공통 **Header**  
```
{
  Authentication : bearer TOKEN
}
```
|URL|GET|POST|PUT|DELETE|Description|
|---|---|---|---|---|---|
|/accounts/login|O|O|---|---|로그인|
|/accounts/logout|O|---|---|---|로그인|
|/accounts/join|O|O|---|---|회원 가입|
|/accounts/profile|O|---|O|O|회원 정보 수정 / 탈퇴|
|/chat|O|O|---|O|채팅|
|/quote|O|O|O|O|명대사 요청 게시판|


### /chat
- GET
  - queryString

  |Key|Value|Default|Description|
  |---|---|---|---|
  |page|1|1|paging offset ( > 0)|
  |per_page|10|10|paging limit ( >= 5)|

  - Response
  ```
  HTTP/1.1 200 OK
  Link: 
  <52.78.247.51:8000/chat?page=10&per-page=10>; rel="next",
  <52.78.247.51:8000/chat?page=50&per-page=10>; rel="last",
  <52.78.247.51:8000/chat?page=0&per-page=10>; rel="first",
  <52.78.247.51:8000/chat?page=0&per-page=0>; rel="prev",
  [
      {
        "id": 1,
        "user": "useremail",
        "content":"text",
        "created_at":"datetime",
        "chat_reply": {
          "id": 2,
          "user": "useremail",
          "content":"text",
          "created_at":"datetime",
        }
      },
      {2, ...},
      ...
      {10,...},
      "links": [
        {
            "rel": "next",
            "method": "GET",
            "link": "52.78.247.51:8000/chat?page=10&per-page=10
        },
        {
            "rel": "last",
            "method": "GET",
            "link": "52.78.247.51:8000/chat?page=50&per-page=10
        },
        {
            "rel": "first",
            "method": "GET",
            "link": "52.78.247.51:8000/chat?page=0&per-page=10
        },
        {
            "rel": "prev",
            "method": "GET",
            "link": "52.78.247.51:8000/chat?page=0&per-page=0
        },
    ]
  ]
  ```

  - POST
    - Response 
    ```
    HTTP/1.1 201 Created
    {
      "id": 1,
      "content": "text",
      "user": "useremail",
      "created_at": "2018-07-04 14:00:00",
      "chat_reply": {
        "id": 2,
        "content": "text",
        "user": "useremail",
        "created_at": "2018-07-04 14:00:00"
      }
      "links": [
          {
              "rel": "self",
              "href": "http://52.78.247.51:8000/chat/1",
              "method": "GET"
          },
          {
              "rel": "delete",
              "href": "http://52.78.247.51:8000/chat/1",
              "method": "DELETE"
          }
      ]
    }

    ```

- DELETE
  - Response 
  ```
  HTTP/1.1 204 No Content
  {

  }
  ```

### /quote
- GET
  - queryString

  |Key|Value|Default|Description|
  |---|---|---|---|
  |page|1|1|paging offset ( > 0)|
  |per_page|10|10|paging limit ( >= 5)|

  - Response
  ```
  HTTP/1.1 200 OK
  Link: 
  <52.78.247.51:8000/quote?page=10&per-page=10>; rel="next",
  <52.78.247.51:8000/quote?page=50&per-page=10>; rel="last",
  <52.78.247.51:8000/quote?page=0&per-page=10>; rel="first",
  <52.78.247.51:8000/quote?page=0&per-page=0>; rel="prev",
  [
      {
        "id": 1,
        "user": "useremail",
        "content":"text",
        "is_apply":True,
        "created_at":"datetime",
        "updated_at":"datetime",
        "applied_at":"datetime",
      },
      {2, ...},
      ...
      {10,...},
      "links": [
        {
            "rel": "next",
            "method": "GET",
            "link": "52.78.247.51:8000/quote?page=10&per-page=10
        },
        {
            "rel": "last",
            "method": "GET",
            "link": "52.78.247.51:8000/quote?page=50&per-page=10
        },
        {
            "rel": "first",
            "method": "GET",
            "link": "52.78.247.51:8000/quote?page=0&per-page=10
        },
        {
            "rel": "prev",
            "method": "GET",
            "link": "52.78.247.51:8000/quote?page=0&per-page=0
        },
    ]
  ]
  ```

- POST
  - Response 
  ```
  HTTP/1.1 201 Created
  {
    "id": 1,
    "content": "text",
    "user": "useremail",
    "created_at": "2018-07-04 14:00:00",
    "applied_at": "2018-07-04 14:00:00",
    "updated_at": "2018-07-04 14:00:00"
    "links": [
        {
            "rel": "self",
            "href": "http://52.78.247.51:8000/quote/1",
            "method": "GET"
        },
        {
            "rel": "patch",
            "href": "http://52.78.247.51:8000/quote/1",
            "method": "PUT"
        },
        {
            "rel": "delete",
            "href": "http://52.78.247.51:8000/quote/1",
            "method": "DELETE"
        }
    ]
  }
  ```

- PUT
  - Response 
  ```
  HTTP/1.1 201 Created
  {

  }
  ```

- DELETE
  - Response 
  ```
  HTTP/1.1 204 No Content
  {

  }
  ```



---

### 화면설계

---

### 관련 이슈

---

### 회고

---
