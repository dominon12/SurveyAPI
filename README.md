# Документация
Данное приложение представляет из себя RESTful API для создания и управления опросов.

## Инструкция по разворачиванию

1. Запустите терминал
2. Выполните команду
```bash
git clone https://github.com/dominon12/SurveyAPI.git
```
3. Перейдите в папку
```bash
cd SurveyAPI
```
4. Созздайте виртуальное окружение и активируйте его
```bash
python3 -m venv venv
source venv/bin/activate
```
5. Установите зависимости
```bash
pip install -r requirements.txt
```

6. Создайте миграции и мигрируйте базу данных
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
```

7. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

8. Запустите локальный сервер
```bash
python manage.py runserver
```

## Документация

#### Базовый URL - /api/v0.1/

- Все данные отправляемые с помощью HTTP-запросов должны быть в формате JSON
- Для доступа к некоторым API ендпоинтам необходима пройти аутентификацию
(Ендпоинты для которых она нужна, будут помечены в данной документацией символом "*")

## Аутентификация
url - accounts/auth/
HTTP метод - POST

Тело запроса:
```json
{
    "username": "username",
    "password": "password"
}
```
Пример ответа с сервера:
```json
{
    "token": "73b0a4df6a3acfcd6dd63b1fa8827e7342dd91a2"
}
```

В последствии, полученный токен необходимо прикладывать в HTTP заголовок к каждому запросу, помеченным символом "*" в документации.

Пример HTTP заголовка:
```json
{
    "Authorization": "Token 73b0a4df6a3acfcd6dd63b1fa8827e7342dd91a2"
}
```

## Создание опроса *
url - surveys/
HTTP метод - POST

Аттрибуты опроса:

- **name** (имя опроса) - Строка длиной до 255 символов;
- **description** (описание) - Строка любой длины;
- **start_date** (дата начала опроса) - Дата и время в формате ISO 8601 (После создания опроса, изменить значение этого аттрибута будет невозможно);
- **end_date** (дата окончания опроса) - Дата и время в формате ISO 8601 (Пользователи не смогут видеть опрос, если дата окончания будет меньше времени на момент отправки запроса к API);
- **questions** - Список из объектов вопроса. 

Атрибуты вопроса:
 
- **text** (сам вопрос) - Строка любой длины;
- **question_type** (тип вопроса) - Целое число от 1 до 3 (1 - Ответ текстом, 2 - Ответ с выбором одного варианта, 3 - Ответ с выбором нескольких вариантов);
- **choices** (варианты ответа - необязательное поле, если тип вопроса - '1 - Ответ текстом') - Список из объектов вариантов ответа. 

Аттрибуты варианта ответа: 

- **text** (текст варианта ответа) - Cтрока любой длины.

Пример тела запроса:
```json
{
    "name": "Favourite colors poll!",
    "description": "This survey will ask you about your favourite color",
    "start_date": "2021-01-01T00:00:00.000Z",
    "end_date": "2021-12-31T00:00:00.000Z",
    "questions": [
        {
            "text": "What is your favourite color?",
            "question_type": 2,
            "choices": [
                {"text": "Red"},
                {"text": "Blue"},
                {"text": "Green"}
            ]
        },
        {
            "text": "Why do you like it?",
            "question_type": 1
        },
        {
            "text": "Select some other colors that you may like",
            "question_type": 3,
            "choices": [
                {"text": "White"},
                {"text": "Pink"},
                {"text": "Tiffany"}
            ]
        }
    ]  
}
```
Ответ с сервера:
```json
{
  "pk": 9,
  "name": "Favourite colors poll!",
  "description": "This survey will ask you about your favourite color",
  "start_date": "2021-01-01T00:00:00Z",
  "end_date": "2021-12-31T00:00:00Z",
  "questions": [
    {
      "pk": 59,
      "text": "What is your favourite color?",
      "question_type": 2,
      "choices": [
        { "pk": 95, "question": 59, "text": "Red" },
        { "pk": 96, "question": 59, "text": "Blue" },
        { "pk": 97, "question": 59, "text": "Green" }
      ]
    },
    {
      "pk": 60,
      "text": "Why do you like it?",
      "question_type": 1,
      "choices": []
    },
    {
      "pk": 61,
      "text": "Select some other colors that you may like",
      "question_type": 3,
      "choices": [
        { "pk": 98, "question": 61, "text": "White" },
        { "pk": 99, "question": 61, "text": "Pink" },
        { "pk": 100, "question": 61, "text": "Tiffany" }
      ]
    }
  ]
}
```
#### Таким образом, мы только что создали опрос с тремя вопросами:
- **What is your favourite color?** - Вопрос с возмоностью выбрать только один вариант ответа из трех
- **Why do you like it?** - Вопрос с ответом в свободной форме (текстом)
- **Select some other colours that you like too:** - Вопрос с возможностью выбора нескольких вариантов ответа

## Изменение опроса *
url - surveys/<pk>/
HTTP метод - PUT
* Вместо <pk> в url выше необходимо подставить pk (primary key) опроса, который необходимо изменить

Данный ендпоинт используется для полного изменение аттрибутов опроса.

Пример тела запроса:
```json
{
  "pk": 9,
  "name": "Updated favourite colors poll!",
  "description": "This survey will ask you about your favourite color",
  "start_date": "2021-01-01T00:00:00Z",
  "end_date": "2021-12-31T00:00:00Z",
  "questions": [
    {
      "pk": 59,
      "text": "What is your favourite color?",
      "question_type": 2,
      "choices": [
        { "pk": 95, "question": 59, "text": "Green" },
        { "pk": 96, "question": 59, "text": "Blue" },
        { "pk": 97, "question": 59, "text": "Red" }
      ]
    },
    {
      "pk": 60,
      "text": "Why do you like this color?",
      "question_type": 1,
      "choices": []
    },
    {
      "pk": 61,
      "text": "Select some other colors that you may like",
      "question_type": 3,
      "choices": [
        { "pk": 98, "question": 61, "text": "White" },
        { "pk": 99, "question": 61, "text": "Pink" },
        { "pk": 100, "question": 61, "text": "Tiffany" }
      ]
    }
  ]
}
```
Ответ с сервера:
```json
{
  "pk": 9,
  "name": "Updated favourite colors poll!",
  "description": "This survey will ask you about your favourite color",
  "start_date": "2021-01-01T00:00:00Z",
  "end_date": "2021-12-31T00:00:00Z",
  "questions": [
    {
      "pk": 59,
      "text": "What is your favourite color?",
      "question_type": 2,
      "choices": [
        { "pk": 95, "question": 59, "text": "Green" },
        { "pk": 96, "question": 59, "text": "Blue" },
        { "pk": 97, "question": 59, "text": "Red" }
      ]
    },
    {
      "pk": 60,
      "text": "Why do you like this color?",
      "question_type": 1,
      "choices": []
    },
    {
      "pk": 61,
      "text": "Select some other colors that you may like",
      "question_type": 3,
      "choices": [
        { "pk": 98, "question": 61, "text": "White" },
        { "pk": 99, "question": 61, "text": "Pink" },
        { "pk": 100, "question": 61, "text": "Tiffany" }
      ]
    }
  ]
}
```
#### Таким образом, мы изменили:
- Аттрибут опроса **name**
- Варианты ответа на вопрос **"What is your favourite color?"**
- Аттрибут **text** вопроса c pk **60**

## Удаление опроса *
url - surveys/<pk>/
HTTP метод - DELETE
* Вместо <pk> в url выше необходимо подставить pk опроса, который необходимо удалить

Данный ендпоинт используется для удаления опроса (также будут удалены и вопросы опроса и варианты ответа на вопрос)

Тело запроса - отсутствует
Ответ с сервера - 204 

## Получение списка активных опросов
url - surveys/
HTTP метод - GET

Тело запроса - отсутствует

Пример ответа с сервера:
```json
[
  {
    "pk": 9,
    "name": "Updated favourite colors poll!",
    "description": "This survey will ask you about your favourite color",
    "start_date": "2021-01-01T00:00:00Z",
    "end_date": "2021-12-31T00:00:00Z",
    "questions": [
      {
        "pk": 59,
        "text": "What is your favourite color?",
        "question_type": 2,
        "choices": [
          { "pk": 95, "question": 59, "text": "Red" },
          { "pk": 96, "question": 59, "text": "Blue" },
          { "pk": 97, "question": 59, "text": "Green" }
        ]
      },
      {
        "pk": 60,
        "text": "Why do you like it?",
        "question_type": 1,
        "choices": []
      },
     {
        "pk": 61,
        "text": "Select some other colors that you may like",
        "question_type": 3,
        "choices": [
          { "pk": 98, "question": 61, "text": "White" },
          { "pk": 99, "question": 61, "text": "Pink" },
          { "pk": 100, "question": 61, "text": "Tiffany" }
        ]
      }
    ]
  }
]
```

#### Обратите внимание
- Если к данному API ендпоинту обращается пользователь без прав администратора (is_staff), то все опросы, у который значени аттрибута end_date меньше чем дата и время на момент отправки запроса, не будут возвращены. 


## Создание вопроса *
url - questions/
HTTP метод - POST

Атрибуты вопроса:
- **survey** (pk опроса для которого необходимо создать вопрос) - Целое число;
- **text** (сам вопрос) - Строка любой длины;
- **question_type** (тип вопроса) - Целое число от 1 до 3 (1 - Ответ текстом, 2 - Ответ с выбором одного варианта, 3 - Ответ с выбором нескольких вариантов);
- **choices** (варианты ответа - необязательное поле, если тип вопроса - '1 - Ответ текстом') - Список из объектов вариантов ответа. 

Аттрибуты варианта ответа: 

- **text** (текст варианта ответа) - Cтрока любой длины.

Пример тела запроса:
```json
{
    "survey": 9,
    "text": "New question",
    "question_type": 1
}
```
Ответа с сервера:
```json
{
  "pk": 63,
  "text": "New question",
  "survey": 9,
  "question_type": 1,
  "choices": []
}

```

## Изменение вопроса *
url - questions/<pk>/
HTTP метод - PUT
* Вместо <pk> в url выше необходимо подставить pk вопроса, который необходимо изменить

Данный ендпоинт используется для изменения данных вопроса

Пример тела запроса:
```json
{
  "text": "Updated question",
  "survey": 9,
  "question_type": 2,
  "choices": [
    {"text": "New answer option"}
  ]
}
```
Ответа с сервера:
```json
{
  "pk": 63,
  "text": "Updated question",
  "survey": 9,
  "question_type": 2,
  "choices": [
    {
      "pk": 101, 
      "question": 63, 
      "text": "New answer option" }
  ]
}
```

## Удаление вопроса *
url - questions/<pk>/
HTTP метод - DELETE
* Вместо <pk> в url выше необходимо подставить pk вопроса, который необходимо удалить

Данный ендпоинт используется для удаления вопроса

Тело запроса - отсутствует
Ответ с сервера - 204 

## Прохождение опроса пользователем
url - completed-surveys/
HTTP метод - POST

Аттрибуты пройденного опроса:

- **survey** (pk опроса) - Целое число;
- **user_id** (id пользователя) - Целое число, либо null (для анонимных пользователей);
- **answers** - Список из объектов ответа на вопрос. 
 
Аттрибуты объекта ответа на вопрос:

- **question** (pk вопроса) - Целое число;
- **text_answer** (ответ пользователя на вопрос) - Строка любой длины. Используется, если тип вопроса - "1 - Ответ текстом";
- **answer_choices** - Список, состоящий из pk вариантов ответа на вопрос. Используется, если тип вопроса - "2 - Ответ с выбором" или "3 - Ответ с выбором нескольких вариантов".

Пример тела запроса:
```json
{
    "user_id": 1,
    "survey": 9,
    "answers": [
        {
            "question": 59,
            "text_answer": "",
            "answer_choices": [97]
        },
        {
            "question": 60,
            "text_answer": "Because green is the color of nature"
        },
        {
            "question": 61,
            "text_answer": "",
            "answer_choices": [99, 100]
        }
    ]
}
```
Ответа с сервера:
```json
{
  "pk": 22,
  "user_id": 1,
  "survey": 9,
  "answers": [
    {
      "pk": 36, 
      "question": 59, 
      "text_answer": "", 
      "answer_choices": [97] 
    },
    {
      "pk": 37,
      "question": 60,
      "text_answer": "Because green is the color of nature",
      "answer_choices": []
    },
    { 
      "pk": 38, 
      "question": 61, 
      "text_answer": "", 
      "answer_choices": [99, 100] 
    }
  ]
}

```

## Получение опросов, пройденных пользователем 
url - completed-surveys?user_id=<user_id>
HTTP метод - GET

*вместо <user_id> в url необходимо подставить id пользователя

Ответ с сервера:
```json
[
  {
    "pk": 22,
    "user_id": 1,
    "survey": 9,
    "answers": [
      {
        "pk": 36,
        "question": 59,
        "text_answer": "",
        "answer_choices": [97]
      },
      {
        "pk": 37,
        "question": 60,
        "text_answer": "Because green is the color of nature",
        "answer_choices": []
      },
      {
        "pk": 38,
        "question": 61,
        "text_answer": "",
        "answer_choices": [99, 100]
      }
    ]
  }
]

```

**Спасибо что дочитали до конца :)**