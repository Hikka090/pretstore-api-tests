import pytest
from src.api.petstore_api import PetStoreAPI
import random
import time


@pytest.fixture
def api_client():
    """Фикстура возвращает клиент для работы с API"""
    return PetStoreAPI()


@pytest.fixture
def random_pet_data():
    """Фикстура генерирует случайные данные для питомца"""
    # Используем микросекунды для большей уникальности
    timestamp = int(time.time() * 1000000) % 10000000
    pet_id = 10000000 + timestamp
    return {
        "id": pet_id,
        "category": {"id": 1, "name": "dogs"},
        "name": f"TestDog{pet_id}",
        "photoUrls": ["https://example.com/photo.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": "available"
    }


@pytest.fixture
def random_order_data():
    """Фикстура генерирует случайные данные для заказа"""
    timestamp = int(time.time() * 1000000) % 10000000
    return {
        "id": 20000000 + timestamp,
        "petId": 30000000 + timestamp,
        "quantity": 1,
        "shipDate": "2023-12-01T10:00:00.000Z",
        "status": "placed",
        "complete": True
    }


@pytest.fixture
def random_user_data():
    """Фикстура генерирует случайные данные для пользователя"""
    timestamp = int(time.time() * 1000000) % 10000000
    user_id = 40000000 + timestamp
    return {
        "id": user_id,
        "username": f"testuser{user_id}",
        "firstName": "Test",
        "lastName": "User",
        "email": f"test{user_id}@example.com",
        "password": "password123",
        "phone": "123-456-7890",
        "userStatus": 1
    }


@pytest.fixture(autouse=True)
def slow_down_tests():
    """Замедляет тесты чтобы избежать rate limiting"""
    yield
    time.sleep(1)  # Увеличим паузу до 1 секунды