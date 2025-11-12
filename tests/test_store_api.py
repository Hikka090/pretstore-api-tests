import pytest


class TestStoreAPI:
    """Тесты для эндпоинтов работы с магазином"""
    
    def test_get_inventory(self, api_client):
        """Тест получения инвентаря"""
        # Act
        response = api_client.get_inventory()
        
        # Assert
        assert response.status_code == 200
        inventory = response.json()
        
        # Проверяем структуру ответа
        assert isinstance(inventory, dict)
        
        # Проверяем, что есть ожидаемые статусы
        expected_statuses = ["available", "pending", "sold"]
        for status in expected_statuses:
            assert status in inventory
        
        # Проверяем, что значения - числа
        for status, count in inventory.items():
            assert isinstance(count, int)
    
    def test_create_and_get_order(self, api_client, random_order_data):
        """Тест создания заказа и его получения"""
        # Arrange
        create_response = api_client.create_order(random_order_data)
        order_id = random_order_data["id"]
        
        # Assert создания
        assert create_response.status_code == 200
        created_order = create_response.json()
        assert created_order["id"] == order_id
        assert created_order["status"] == "placed"
        
        # Act - получаем заказ
        get_response = api_client.get_order_by_id(order_id)
        
        # Assert получения
        assert get_response.status_code == 200
        retrieved_order = get_response.json()
        assert retrieved_order["id"] == order_id
        assert retrieved_order["quantity"] == random_order_data["quantity"]
    
    def test_create_and_delete_order(self, api_client, random_order_data):
        """Тест создания и удаления заказа"""
        # Arrange
        create_response = api_client.create_order(random_order_data)
        order_id = random_order_data["id"]
        assert create_response.status_code == 200
        
        # Act - удаляем заказ
        delete_response = api_client.delete_order(order_id)
        
        # Assert удаления
        assert delete_response.status_code == 200
        
        # Проверяем, что заказ действительно удален
        get_response = api_client.get_order_by_id(order_id)
        assert get_response.status_code == 404
    
    def test_get_order_not_found(self, api_client):
        """Тест получения несуществующего заказа"""
        # Act & Assert
        response = api_client.get_order_by_id(999999)
        assert response.status_code == 404