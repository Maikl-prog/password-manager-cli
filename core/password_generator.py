"""
Модуль для генерации надёжных паролей
"""

import secrets
import string


class PasswordGenerator:
    """Класс для генерации случайных паролей"""
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length: int = 16, use_uppercase: bool = True,
                 use_digits: bool = True, use_symbols: bool = True) -> str:
        
        if length < 8:
            length = 8
        if length > 64:
            length = 64
        
        alphabet = self.lowercase
        if use_uppercase:
            alphabet += self.uppercase
        if use_digits:
            alphabet += self.digits
        if use_symbols:
            alphabet += self.symbols
        
        password = []
        password.append(secrets.choice(self.lowercase))
        if use_uppercase:
            password.append(secrets.choice(self.uppercase))
        if use_digits:
            password.append(secrets.choice(self.digits))
        if use_symbols:
            password.append(secrets.choice(self.symbols))
        
        remaining = length - len(password)
        for _ in range(remaining):
            password.append(secrets.choice(alphabet))
        
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)