"""
Модуль для шифрования и дешифрования данных
Использует библиотеку cryptography (Fernet)
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class PasswordEncryption:
    """Класс для шифрования паролей с мастер-паролем"""
    
    def __init__(self, master_password: str):
        """
        Инициализация с мастер-паролем
        
        Args:
            master_password: Мастер-пароль для генерации ключа
        """
        self.master_password = master_password.encode('utf-8')
        self.salt_file = "data/salt.bin"
        self.key = self._get_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _get_or_create_key(self) -> bytes:
        """Получить существующий ключ или создать новый"""
        if os.path.exists(self.salt_file):
            with open(self.salt_file, 'rb') as f:
                salt = f.read()
        else:
            salt = os.urandom(16)
            os.makedirs("data", exist_ok=True)
            with open(self.salt_file, 'wb') as f:
                f.write(salt)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        return key
    
    def encrypt(self, data: str) -> bytes:
        """Зашифровать строку"""
        return self.cipher.encrypt(data.encode('utf-8'))
    
    def decrypt(self, encrypted_data: bytes) -> str:
        """Расшифровать данные"""
        return self.cipher.decrypt(encrypted_data).decode('utf-8')