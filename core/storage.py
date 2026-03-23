"""
Модуль для работы с хранилищем паролей
"""

import json
import os
from typing import Dict, List, Optional
from .encryption import PasswordEncryption


class PasswordStorage:
    """Класс для управления хранилищем паролей"""
    
    def __init__(self, encryption: PasswordEncryption):
        self.encryption = encryption
        self.vault_file = "data/vault.json"
        self.data = self._load_vault()
    
    def _load_vault(self) -> Dict:
        """Загрузить хранилище из файла"""
        if not os.path.exists(self.vault_file):
            return {"passwords": [], "version": "1.0"}
        
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted_data = f.read()
            
            if not encrypted_data:
                return {"passwords": [], "version": "1.0"}
            
            decrypted = self.encryption.decrypt(encrypted_data)
            return json.loads(decrypted)
        except Exception as e:
            print(f"⚠️ Ошибка загрузки хранилища: {e}")
            return {"passwords": [], "version": "1.0"}
    
    def _save_vault(self) -> bool:
        """Сохранить хранилище в файл"""
        try:
            json_data = json.dumps(self.data, ensure_ascii=False, indent=2)
            encrypted = self.encryption.encrypt(json_data)
            
            with open(self.vault_file, 'wb') as f:
                f.write(encrypted)
            return True
        except Exception as e:
            print(f"⚠️ Ошибка сохранения: {e}")
            return False
    
    def add_password(self, service: str, username: str, password: str) -> bool:
        for entry in self.data["passwords"]:
            if entry["service"].lower() == service.lower():
                return False
        
        self.data["passwords"].append({
            "service": service,
            "username": username,
            "password": password,
            "created": self._get_timestamp()
        })
        return self._save_vault()
    
    def get_password(self, service: str) -> Optional[Dict]:
        for entry in self.data["passwords"]:
            if entry["service"].lower() == service.lower():
                return entry
        return None
    
    def list_services(self) -> List[str]:
        return [entry["service"] for entry in self.data["passwords"]]
    
    def delete_password(self, service: str) -> bool:
        for i, entry in enumerate(self.data["passwords"]):
            if entry["service"].lower() == service.lower():
                del self.data["passwords"][i]
                return self._save_vault()
        return False
    
    def update_password(self, service: str, new_password: str) -> bool:
        for entry in self.data["passwords"]:
            if entry["service"].lower() == service.lower():
                entry["password"] = new_password
                entry["updated"] = self._get_timestamp()
                return self._save_vault()
        return False
    
    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()