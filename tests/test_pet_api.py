import pytest
import random


class TestPetAPI:
    """Тесты для эндпоинтов работы с питомцами"""
    
    def test_create_pet_success(self, api_client, random_pet_data):
        """Тест успешного создания питомца"""
        # Act
        response = api_client.create_pet(random_pet_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        
        # Проверяем, что все данные сохранились правильно
        assert response_data["id"] == random_pet_data["id"]
        assert response_data["name"] == random_pet_data["name"]
        assert response_data["status"] == random_pet_data["status"]
        assert response_data["category"]["name"] == random_pet_data["category"]["name"]
    
    def test_get_pet_by_id_success(self, api_client, random_pet_data):
        """Тест успешного получения питомца по ID"""
        # Arrange
        create_response = api_client.create_pet(random_pet_data)
        pet_id = create_response.json()["id"]
        
        # Act
        response = api_client.get_pet_by_id(pet_id)
        
        # Assert
        assert response.status_code == 200
        assert response.json()["id"] == pet_id
    
    def test_get_pet_by_id_not_found(self, api_client):
        """Тест получения несуществующего питомца"""
        # Act
        response = api_client.get_pet_by_id(999999)  # Несуществующий ID
        
        # Assert
        assert response.status_code == 404
        error_data = response.json()
        assert error_data["code"] == 1
        assert error_data["type"] == "error"
        assert "Pet not found" in error_data["message"]
    
    def test_update_pet_success(self, api_client, random_pet_data):
        """Тест успешного обновления питомца"""
        # Arrange
        create_response = api_client.create_pet(random_pet_data)
        pet_id = create_response.json()["id"]
        
        # Подготавливаем данные для обновления
        updated_data = random_pet_data.copy()
        updated_data["name"] = "UpdatedName"
        updated_data["status"] = "sold"
        
        # Act
        response = api_client.update_pet(updated_data)
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["name"] == "UpdatedName"
        assert response_data["status"] == "sold"
        
        # Дополнительная проверка: получаем питомца и проверяем, что данные обновились
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.json()["name"] == "UpdatedName"
    
    def test_delete_pet_success(self, api_client, random_pet_data):
        """Тест успешного удаления питомца"""
        # Arrange
        create_response = api_client.create_pet(random_pet_data)
        pet_id = create_response.json()["id"]
        
        # Act
        delete_response = api_client.delete_pet(pet_id)
        
        # Assert
        assert delete_response.status_code == 200
        
        # Проверяем, что питомец действительно удален
        get_response = api_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 404
    
    @pytest.mark.parametrize("status", ["available", "pending", "sold"])
    def test_find_pets_by_status(self, api_client, status):
        """Параметризованный тест поиска питомцев по разным статусам"""
        # Act
        response = api_client.find_pets_by_status(status)
        
        # Assert
        assert response.status_code == 200
        pets = response.json()
        
        # Проверяем, что это список (может быть пустым)
        assert isinstance(pets, list)
        
        # Если есть питомцы с таким статусом, проверяем что у всех правильный статус
        for pet in pets:
            assert pet["status"] == status
    
    def test_create_pet_with_invalid_data(self, api_client):
        """Тест создания питомца с невалидными данными"""
        # Arrange - данные с строкой вместо числа для ID
        invalid_data = {
            "id": "invalid_id",  # Должно быть число!
            "name": "TestPet",
            "status": "available"
        }
        
        # Act
        response = api_client.create_pet(invalid_data)
        
        # Assert - API возвращает 500 на невалидные данные
        assert response.status_code == 500