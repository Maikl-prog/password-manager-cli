![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/Maikl-prog/password-manager-cli)
# 🔐 Password Manager CLI

Консольный менеджер паролей с шифрованием. Все пароли хранятся в зашифрованном виде и доступны только по мастер-паролю.

## ✨ Возможности

- 🔒 **Шифрование данных** — Fernet + PBKDF2
- 🎲 **Генерация паролей** — создание надёжных паролей с настройками
- 📋 **Копирование в буфер** — быстрая вставка паролей
- ➕ **CRUD операции** — добавление, просмотр, обновление, удаление
- 💾 **Автосохранение** — данные сохраняются в зашифрованном файле

## 🚀 Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/Maikl-prog/password-manager-cli.git
cd password-manager-cli

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate
# или (Mac/Linux)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить приложение
python main.py

📁 Структура проекта
text
password-manager-cli/
├── main.py                 # Точка входа, CLI интерфейс
├── core/
│   ├── encryption.py       # Шифрование данных
│   ├── storage.py          # Работа с хранилищем
│   └── password_generator.py # Генерация паролей
├── data/                   # Зашифрованное хранилище (создаётся при запуске)
├── requirements.txt        # Зависимости
└── README.md               # Документация
🛠️ Технологии
Python 3.8+

cryptography (Fernet, PBKDF2)

pyperclip (буфер обмена)

getpass (скрытый ввод пароля)

🔐 Как это работает
При первом запуске создаётся соль (salt) для шифрования

Мастер-пароль не хранится, а используется для генерации ключа через PBKDF2

Все пароли шифруются перед сохранением в data/vault.json

Без мастер-пароля расшифровать данные невозможно