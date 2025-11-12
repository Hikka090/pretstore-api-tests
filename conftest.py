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
    pet_id = random.randint(1000, 9999)
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
    return {
        "id": random.randint(1, 1000),
        "petId": random.randint(1000, 9999),
        "quantity": 1,
        "shipDate": "2023-12-01T10:00:00.000Z",
        "status": "placed",
        "complete": True
    }


@pytest.fixture
def random_user_data():
    """Фикстура генерирует случайные данные для пользователя"""
    user_id = random.randint(100, 999)
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


@pytest.fixture
def created_pet(api_client, random_pet_data):
    """
    Фикстура создает питомца перед тестом и удаляет после.
    Пример фикстуры с setup/teardown.
    """
    # Setup - создаем питомца
    response = api_client.create_pet(random_pet_data)
    assert response.status_code == 200
    pet_id = response.json()["id"]
    
    yield pet_id  # Это значение передается в тест
    
    # Teardown - удаляем питомца после теста
    try:
        api_client.delete_pet(pet_id)
    except:
        pass  # Игнорируем ошибки при удалении в teardown