import pytest
import random


class TestPetAPI:
    """Тесты для эндпоинтов работы с питомцами"""
    
    def test_create_pet_success(self, api_client, random_pet_data):
        """Тест успешного создания питомца - проверяем только ответ создания"""
        # Act
        response = api_client.create_pet(random_pet_data)
        
        # Assert - проверяем что создание возвращает 200 и корректные данные
        assert response.status_code == 200
        response_data = response.json()
        
        # Проверяем, что в ответе те же данные что мы отправляли
        assert response_data["id"] == random_pet_data["id"]
        assert response_data["name"] == random_pet_data["name"]
        assert response_data["status"] == random_pet_data["status"]
    
    def test_get_pet_by_id_behavior(self, api_client):
        """Тест поведения GET /pet/{id} - PetStore возвращает 404 для несуществующих"""
        # Act - пробуем получить несуществующего питомца
        response = api_client.get_pet_by_id(999999999)
        
        # Assert - PetStore возвращает 404 для несуществующих питомцев
        assert response.status_code == 404
        
        # Проверяем структуру ответа об ошибке
        response_data = response.json()
        assert "code" in response_data
        assert "type" in response_data
        assert "message" in response_data
        assert "Pet not found" in response_data["message"]
    
    def test_update_pet_success(self, api_client, random_pet_data):
        """Тест успешного обновления питомца - проверяем только ответ обновления"""
        # Arrange
        create_response = api_client.create_pet(random_pet_data)
        original_pet = create_response.json()
        
        # Подготавливаем данные для обновления
        updated_data = original_pet.copy()
        updated_data["name"] = "UpdatedName"
        updated_data["status"] = "sold"
        
        # Act
        response = api_client.update_pet(updated_data)
        
        # Assert - проверяем что обновление возвращает 200 и обновленные данные
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == "UpdatedName"
        assert response_data["status"] == "sold"
    
    def test_delete_pet_returns_known_behavior(self, api_client):
        """Тест что DELETE /pet/{id} возвращает предсказуемый результат"""
        # Act - пытаемся удалить несуществующего питомца
        response = api_client.delete_pet(999999999, api_key="special-key")
        
        # Assert - проверяем что ответ имеет предсказуемую структуру
        # PetStore может возвращать 200 или 404, но структура ответа должна быть consistent
        assert response.status_code in [200, 404]
        
        # Обрабатываем случай, когда ответ может быть пустым
        if response.content:  # Проверяем, что ответ не пустой
            try:
                response_data = response.json()
                # Проверяем что ответ имеет стандартную структуру PetStore
                assert "code" in response_data
                assert "type" in response_data
                if response.status_code == 200:
                    assert "message" in response_data
                else:  # 404
                    assert "message" in response_data
            except ValueError:
                # Если не удалось распарсить JSON, но статус код корректен - это приемлемо
                # для демо-API
                pass
    
    def test_pet_creation_with_different_categories(self, api_client):
        """Тест создания питомцев с разными категориями"""
        # Arrange - различные категории питомцев
        categories = [
            {"id": 1, "name": "Dogs"},
            {"id": 2, "name": "Cats"},
            {"id": 3, "name": "Birds"},
            {"id": 4, "name": "Fish"}
        ]
        
        for category in categories:
            # Act - создаем питомца с каждой категорией
            pet_data = {
                "id": random.randint(1000000, 9999999),
                "category": category,
                "name": f"TestPet{category['name']}",
                "photoUrls": ["https://example.com/photo.jpg"],
                "tags": [{"id": 1, "name": "test"}],
                "status": "available"
            }
            
            response = api_client.create_pet(pet_data)
            
            # Assert - проверяем что создание успешно и категория сохранена
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["category"]["id"] == category["id"]
            assert response_data["category"]["name"] == category["name"]
    
    def test_pet_creation_with_multiple_tags(self, api_client):
        """Тест создания питомца с несколькими тегами"""
        # Arrange
        pet_data = {
            "id": random.randint(1000000, 9999999),
            "name": "MultiTagPet",
            "photoUrls": ["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"],
            "tags": [
                {"id": 1, "name": "friendly"},
                {"id": 2, "name": "playful"},
                {"id": 3, "name": "smart"}
            ],
            "status": "available"
        }
        
        # Act
        response = api_client.create_pet(pet_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert len(response_data["tags"]) == 3
        assert response_data["tags"][0]["name"] == "friendly"
        assert response_data["tags"][1]["name"] == "playful"
        assert response_data["tags"][2]["name"] == "smart"
    
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, api_client, status):
        """Параметризованный тест поиска питомцев по разным статусам"""
        # Act
        response = api_client.find_pets_by_status(status)
        
        # Assert
        assert response.status_code == 200
        pets = response.json()
        
        # Проверяем, что это список
        assert isinstance(pets, list)
        
        # Если есть питомцы с таким статусом, проверяем что у всех правильный статус
        for pet in pets:
            assert pet["status"] == status
    
    def test_create_pet_with_minimal_data(self, api_client):
        """Тест создания питомца с минимальным набором данных"""
        # Arrange
        minimal_data = {
            "id": random.randint(1000000, 9999999),
            "name": "MinimalPet",
            "status": "available"
        }
        
        # Act
        response = api_client.create_pet(minimal_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == "MinimalPet"
        assert response_data["status"] == "available"
    
    def test_create_pet_with_full_data(self, api_client):
        """Тест создания питомца с полным набором данных"""
        # Arrange
        full_data = {
            "id": random.randint(1000000, 9999999),
            "category": {
                "id": 1,
                "name": "Cats"
            },
            "name": "Fluffy",
            "photoUrls": [
                "http://example.com/photo1.jpg",
                "http://example.com/photo2.jpg"
            ],
            "tags": [
                {
                    "id": 1,
                    "name": "friendly"
                },
                {
                    "id": 2, 
                    "name": "playful"
                }
            ],
            "status": "available"
        }
        
        # Act
        response = api_client.create_pet(full_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        # Проверяем основные поля
        assert response_data["id"] == full_data["id"]
        assert response_data["name"] == full_data["name"]
        assert response_data["status"] == full_data["status"]
        
        # Проверяем вложенные структуры
        assert response_data["category"]["name"] == full_data["category"]["name"]
        assert len(response_data["photoUrls"]) == len(full_data["photoUrls"])
        assert len(response_data["tags"]) == len(full_data["tags"])