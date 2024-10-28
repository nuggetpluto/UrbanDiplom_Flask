
# Flask Project

## Обзор проекта

Проект представляет собой веб-приложение для онлайн-магазина, где пользователи могут регистрироваться, входить в систему, просматривать и добавлять товары в корзину. Интерфейс создан с использованием HTML-шаблонов и CSS для стилизации страниц.

## Основные возможности

- Регистрация и авторизация пользователей.
- Просмотр и управление профилем пользователя.
- Просмотр товаров и добавление их в корзину.
- Форма обратной связи для связи с поддержкой.

## Структура проекта

```
Flask_project/
│
├── app.py
├── instance/
│   └── users.db
├── static/
│   ├── images/
│   │   ├── background.jpg
│   │   ├── hide_password.png
│   │   ├── show_password.png
│   │   ├── product1.jpg
│   │   ├── product2.jpg
│   │   └── product4.jpg
│   └── styles.css
├── templates/
│   ├── about.html
│   ├── base.html
│   ├── cart.html
│   ├── contact.html
│   ├── index.html
│   ├── login.html
│   ├── product.html
│   ├── profile.html
│   ├── register.html
│   ├── reset_request.html
│   ├── reset_token.html
│   ├── support.html
│   └── view_users.html
├── models.py
└── requirements.txt
```

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/flask_project.git
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите приложение:
   ```bash
   python app.py
   ```

4. Откройте в браузере:
   ```
   http://127.0.0.1:5000
   ```

## Дополнительная информация

Проект разработан на Flask и включает основные функции для управления товарами в онлайн-магазине. Будущие улучшения могут включать интеграцию с платежными системами и добавление рекомендаций на основе покупок пользователя.
