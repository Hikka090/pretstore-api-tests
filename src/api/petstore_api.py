import requests
import json
from typing import Optional, Dict, Any


class PetStoreAPI:
    """
    Клиент для работы с PetStore API.
    Инкапсулирует всю логику взаимодействия с API.
    """
    
    def __init__(self, base_url: str = "https://petstore.swagger.io/v2"):
        self.base_url = base_url
        self.session = requests.Session()
        # Можно добавить общие заголовки здесь
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Базовый метод для выполнения HTTP запросов.
        Централизованная обработка ошибок и логирование.
        """
        url = f"{self.base_url}{endpoint}"
        print(f"Making {method.upper()} request to: {url}")  # Для дебага
        
        try:
            response = self.session.request(method, url, **kwargs)
            print(f"Response status: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            raise
    
    # === PET ENDPOINTS ===
    
    def create_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """POST /pet - Добавление нового питомца"""
        return self._make_request("POST", "/pet", json=pet_data)
    
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        """GET /pet/{petId} - Получение питомца по ID"""
        return self._make_request("GET", f"/pet/{pet_id}")
    
    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """PUT /pet - Обновление существующего питомца"""
        return self._make_request("PUT", "/pet", json=pet_data)
    
    def delete_pet(self, pet_id: int) -> requests.Response:
        """DELETE /pet/{petId} - Удаление питомца"""
        return self._make_request("DELETE", f"/pet/{pet_id}")
    
    def find_pets_by_status(self, status: str) -> requests.Response:
        """GET /pet/findByStatus - Поиск питомцев по статусу"""
        return self._make_request("GET", f"/pet/findByStatus?status={status}")
    
    # === STORE ENDPOINTS ===
    
    def get_inventory(self) -> requests.Response:
        """GET /store/inventory - Получение инвентаря"""
        return self._make_request("GET", "/store/inventory")
    
    def create_order(self, order_data: Dict[str, Any]) -> requests.Response:
        """POST /store/order - Размещение заказа"""
        return self._make_request("POST", "/store/order", json=order_data)
    
    def get_order_by_id(self, order_id: int) -> requests.Response:
        """GET /store/order/{orderId} - Получение заказа по ID"""
        return self._make_request("GET", f"/store/order/{order_id}")
    
    def delete_order(self, order_id: int) -> requests.Response:
        """DELETE /store/order/{orderId} - Удаление заказа"""
        return self._make_request("DELETE", f"/store/order/{order_id}")
    
    # === USER ENDPOINTS ===
    
    def create_user(self, user_data: Dict[str, Any]) -> requests.Response:
        """POST /user - Создание пользователя"""
        return self._make_request("POST", "/user", json=user_data)
    
    def get_user_by_username(self, username: str) -> requests.Response:
        """GET /user/{username} - Получение пользователя по имени"""
        return self._make_request("GET", f"/user/{username}")
    
    def update_user(self, username: str, user_data: Dict[str, Any]) -> requests.Response:
        """PUT /user/{username} - Обновление пользователя"""
        return self._make_request("PUT", f"/user/{username}", json=user_data)
    
    def delete_user(self, username: str) -> requests.Response:
        """DELETE /user/{username} - Удаление пользователя"""
        return self._make_request("DELETE", f"/user/{username}")
    
    def create_users_with_list(self, users_list: list) -> requests.Response:
        """POST /user/createWithList - Создание пользователей из списка"""
        return self._make_request("POST", "/user/createWithList", json=users_list)