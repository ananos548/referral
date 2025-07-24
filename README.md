Referral API

Этот API предоставляет функциональность для регистрации пользователей, аутентификации и реферальной системы с использованием пригласительных кодов.

Эндпоинты API

Эндпоинты API доступны по базовому пути /profile/.

Аутентификация

POST /profile/login/

Создает нового пользователя, если такового не существует с предоставленным номером телефона. Возвращает auth_code для новых пользователей.

Тело запроса:
JSON

{
    "phone": "string"
}

Ответы:

    201 Created (Пользователь создан):
    JSON

{
    "success": true,
    "message": "User created",
    "data": {
        "auth_code": "string"
    }
}

200 OK (Пользователь уже существует):
JSON

{
    "success": false,
    "message": "User already exists"
}

400 Bad Request (Отсутствует номер телефона):
JSON

    {
        "message": "Phone is required"
    }

POST /profile/verify/

Проверяет auth_code для пользователя, идентифицированного по номеру телефона. В случае успеха очищает код и генерирует новый invite_code.

Тело запроса:
JSON

{
    "phone": "string",
    "auth_code": "string"
}

Ответы:

    200 OK (Пользователь подтвержден):
    JSON

{
    "success": true,
    "message": "User verified",
    "data": {
        "invite_code": "string"
    }
}

400 Bad Request (Неверные данные или верификация не удалась):
JSON

{
    "message": "Phone and auth_code required"
}

Или
JSON

    {
        "message": "Verification failed"
    }

Реферальная система

POST /profile/activate_invite_code/

Пользователь вводит invite_code другого пользователя. Сохраняет информацию о том, кто его пригласил.

Тело запроса:
JSON

{
    "phone": "string",
    "invite_code": "string"
}

Ответы:

    200 OK (Код приглашения активирован):
    JSON

{
    "success": true,
    "message": "Invite code activated",
    "data": {
        "referrer_phone": "string"
    }
}

400 Bad Request (Неверные данные, самоприглашение или код уже использован):
JSON

{
    "message": "Phone and invite_code are required"
}

Или
JSON

{
    "message": "Invalid invite code"
}

Или
JSON

{
    "message": "You cannot refer yourself."
}

Или
JSON

{
    "message": "Invite code already used."
}

404 Not Found (Пользователь не найден):
JSON

    {
        "message": "User not found"
    }

