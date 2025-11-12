import pytest


class TestUserAPI:
    """Тесты для эндпоинтов работы с пользователями"""
    
    def test_create_and_get_user(self, api_client, random_user_data):
        """Тест создания и получения пользователя"""
        # Arrange
        username = random_user_data["username"]
        
        # Act - создаем пользователя
        create_response = api_client.create_user(random_user_data)
        
        # Assert создания
        assert create_response.status_code == 200
        
        # Act - получаем пользователя
        get_response = api_client.get_user_by_username(username)
        
        # Assert получения
        assert get_response.status_code == 200
        user_data = get_response.json()
        assert user_data["username"] == username
        assert user_data["email"] == random_user_data["email"]
        
        # Cleanup
        api_client.delete_user(username)
    
    def test_create_update_get_user(self, api_client, random_user_data):
        """Тест создания, обновления и получения пользователя"""
        # Arrange
        username = random_user_data["username"]
        api_client.create_user(random_user_data)
        
        # Подготавливаем данные для обновления
        updated_data = random_user_data.copy()
        updated_data["email"] = "updated@example.com"
        updated_data["firstName"] = "UpdatedName"
        
        # Act - обновляем пользователя
        update_response = api_client.update_user(username, updated_data)
        
        # Assert обновления
        assert update_response.status_code == 200
        
        # Проверяем, что данные обновились
        get_response = api_client.get_user_by_username(username)
        assert get_response.status_code == 200
        user_data = get_response.json()
        assert user_data["email"] == "updated@example.com"
        assert user_data["firstName"] == "UpdatedName"
        
        # Cleanup
        api_client.delete_user(username)
    
    def test_create_users_with_list(self, api_client):
        """Тест создания нескольких пользователей через список"""
        # Arrange
        users_list = [
            {
                "id": 101,
                "username": "testuser101",
                "firstName": "John",
                "lastName": "Doe",
                "email": "john@example.com",
                "password": "password123",
                "phone": "123-456-7890",
                "userStatus": 1
            },
            {
                "id": 102,
                "username": "testuser102", 
                "firstName": "Jane",
                "lastName": "Smith",
                "email": "jane@example.com",
                "password": "password456",
                "phone": "098-765-4321",
                "userStatus": 1
            }
        ]
        
        # Act
        response = api_client.create_users_with_list(users_list)
        
        # Assert
        assert response.status_code == 200
        
        # Cleanup
        for user in users_list:
            api_client.delete_user(user["username"])
    
    def test_get_user_not_found(self, api_client):
        """Тест получения несуществующего пользователя"""
        # Act & Assert
        response = api_client.get_user_by_username("nonexistentuser12345")
        assert response.status_code == 404
    
    def test_delete_user_success(self, api_client, random_user_data):
        """Тест успешного удаления пользователя"""
        # Arrange
        username = random_user_data["username"]
        api_client.create_user(random_user_data)
        
        # Act
        delete_response = api_client.delete_user(username)
        
        # Assert
        assert delete_response.status_code == 200
        
        # Проверяем, что пользователь действительно удален
        get_response = api_client.get_user_by_username(username)
        assert get_response.status_code == 404