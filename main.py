"""
Password Manager CLI - Менеджер паролей с шифрованием
"""

import os
import sys
import getpass
from core.encryption import PasswordEncryption
from core.storage import PasswordStorage
from core.password_generator import PasswordGenerator


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    print("=" * 50)
    print("         🔐 PASSWORD MANAGER CLI")
    print("=" * 50)


def print_menu():
    print("\n📌 ГЛАВНОЕ МЕНЮ:")
    print("  1. Добавить пароль")
    print("  2. Показать все сервисы")
    print("  3. Получить пароль")
    print("  4. Удалить пароль")
    print("  5. Обновить пароль")
    print("  6. Сгенерировать пароль")
    print("  7. Выход")
    print("-" * 50)


def add_password(storage: PasswordStorage):
    print("\n➕ ДОБАВЛЕНИЕ ПАРОЛЯ")
    service = input("Название сервиса (например, Google): ").strip()
    
    if not service:
        print("❌ Название сервиса не может быть пустым")
        return
    
    username = input("Имя пользователя / email: ").strip()
    
    gen_choice = input("Сгенерировать пароль? (y/n): ").strip().lower()
    
    if gen_choice == 'y':
        gen = PasswordGenerator()
        length = int(input("Длина пароля (8-64, по умолчанию 16): ") or "16")
        password = gen.generate(length)
        print(f"✅ Сгенерирован пароль: {password}")
    else:
        password = getpass.getpass("Введите пароль: ")
    
    if storage.add_password(service, username, password):
        print(f"✅ Пароль для '{service}' успешно сохранён!")
    else:
        print(f"⚠️ Сервис '{service}' уже существует")


def list_services(storage: PasswordStorage):
    services = storage.list_services()
    
    if not services:
        print("\n📭 Нет сохранённых паролей")
        return
    
    print("\n📋 СОХРАНЁННЫЕ СЕРВИСЫ:")
    print("-" * 40)
    for i, service in enumerate(services, 1):
        print(f"  {i}. {service}")
    print("-" * 40)


def get_password(storage: PasswordStorage):
    service = input("\nВведите название сервиса: ").strip()
    
    if not service:
        print("❌ Введите название сервиса")
        return
    
    entry = storage.get_password(service)
    
    if entry:
        print(f"\n🔓 ДАННЫЕ ДЛЯ '{service}':")
        print(f"  👤 Логин: {entry['username']}")
        print(f"  🔑 Пароль: {entry['password']}")
        
        copy_choice = input("\nСкопировать пароль в буфер обмена? (y/n): ").strip().lower()
        if copy_choice == 'y':
            try:
                import pyperclip
                pyperclip.copy(entry['password'])
                print("✅ Пароль скопирован в буфер обмена!")
            except ImportError:
                print("⚠️ Библиотека pyperclip не установлена")
    else:
        print(f"❌ Сервис '{service}' не найден")


def delete_password(storage: PasswordStorage):
    service = input("\nВведите название сервиса для удаления: ").strip()
    
    if not service:
        print("❌ Введите название сервиса")
        return
    
    confirm = input(f"⚠️ Точно удалить пароль для '{service}'? (y/n): ").strip().lower()
    
    if confirm == 'y':
        if storage.delete_password(service):
            print(f"✅ Пароль для '{service}' удалён")
        else:
            print(f"❌ Сервис '{service}' не найден")
    else:
        print("❌ Удаление отменено")


def update_password(storage: PasswordStorage):
    service = input("\nВведите название сервиса: ").strip()
    
    if not service:
        print("❌ Введите название сервиса")
        return
    
    entry = storage.get_password(service)
    
    if not entry:
        print(f"❌ Сервис '{service}' не найден")
        return
    
    print(f"\nТекущий пароль для '{service}': {entry['password']}")
    
    gen_choice = input("Сгенерировать новый пароль? (y/n): ").strip().lower()
    
    if gen_choice == 'y':
        gen = PasswordGenerator()
        length = int(input("Длина пароля (8-64, по умолчанию 16): ") or "16")
        new_password = gen.generate(length)
        print(f"✅ Сгенерирован новый пароль: {new_password}")
    else:
        new_password = getpass.getpass("Введите новый пароль: ")
    
    if storage.update_password(service, new_password):
        print(f"✅ Пароль для '{service}' обновлён")
    else:
        print("❌ Ошибка обновления")


def generate_password():
    print("\n🎲 ГЕНЕРАЦИЯ ПАРОЛЯ")
    
    gen = PasswordGenerator()
    
    try:
        length = int(input("Длина пароля (8-64, по умолчанию 16): ") or "16")
        use_uppercase = input("Использовать заглавные буквы? (y/n, по умолчанию y): ").strip().lower() != 'n'
        use_digits = input("Использовать цифры? (y/n, по умолчанию y): ").strip().lower() != 'n'
        use_symbols = input("Использовать спецсимволы? (y/n, по умолчанию y): ").strip().lower() != 'n'
        
        password = gen.generate(length, use_uppercase, use_digits, use_symbols)
        
        print(f"\n✅ Сгенерированный пароль: {password}")
        
        copy_choice = input("Скопировать в буфер обмена? (y/n): ").strip().lower()
        if copy_choice == 'y':
            try:
                import pyperclip
                pyperclip.copy(password)
                print("✅ Пароль скопирован в буфер обмена!")
            except ImportError:
                print("⚠️ Библиотека pyperclip не установлена")
    except ValueError:
        print("❌ Неверный формат длины пароля")


def main():
    clear_screen()
    print_header()
    
    print("\n🔐 Введите мастер-пароль для доступа к хранилищу")
    master_password = getpass.getpass("Мастер-пароль: ")
    
    if not master_password:
        print("❌ Мастер-пароль не может быть пустым")
        sys.exit(1)
    
    try:
        encryption = PasswordEncryption(master_password)
        storage = PasswordStorage(encryption)
        
        print("✅ Доступ разрешён!")
        
        while True:
            print_menu()
            choice = input("\nВыберите действие (1-7): ").strip()
            
            if choice == '1':
                add_password(storage)
            elif choice == '2':
                list_services(storage)
            elif choice == '3':
                get_password(storage)
            elif choice == '4':
                delete_password(storage)
            elif choice == '5':
                update_password(storage)
            elif choice == '6':
                generate_password()
            elif choice == '7':
                print("\n👋 До свидания! Ваши пароли в безопасности.")
                sys.exit(0)
            else:
                print("❌ Неверный выбор. Попробуйте снова.")
            
            input("\nНажмите Enter для продолжения...")
            clear_screen()
            print_header()
            
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        print("Возможно, неверный мастер-пароль или файл повреждён")
        sys.exit(1)


if __name__ == "__main__":
    main()