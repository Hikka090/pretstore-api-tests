import pytest


class TestStoreAPI:
    """Тесты для эндпоинтов работы с магазином"""
    
    def test_get_inventory(self, api_client):
        """Тест получения инвентаря - этот endpoint работает надежно"""
        response = api_client.get_inventory()
        
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
    
    def test_create_order_success(self, api_client, random_order_data):
        """Тест успешного создания заказа - проверяем только ответ создания"""

        response = api_client.create_order(random_order_data)
        
        assert response.status_code == 200
        created_order = response.json()
        
        # Проверяем основные поля
        assert created_order["id"] == random_order_data["id"]
        assert created_order["status"] == "placed"
        assert created_order["complete"] == True
    
    def test_get_order_behavior(self, api_client):
        """Тест поведения GET /order/{id}"""
        # Пробуем получить несуществующий заказ
        response = api_client.get_order_by_id(999999999)
        
        # PetStore возвращает 404 для несуществующих заказов
        assert response.status_code == 404
    
    def test_delete_order_behavior(self, api_client):
        """Тест поведения DELETE /order/{id}"""
        # Пробуем удалить несуществующий заказ
        response = api_client.delete_order(999999999)
        
        # PetStore возвращает 404 для несуществующих заказов
        assert response.status_code == 404
    
    def test_create_order_with_minimal_data(self, api_client):
        """Тест создания заказа с минимальными данными"""
        minimal_order = {
            "id": 1,
            "petId": 1,
            "quantity": 1,
            "status": "placed",
            "complete": True
        }
        
        response = api_client.create_order(minimal_order)
        
        assert response.status_code == 200
        order_data = response.json()
        assert order_data["status"] == "placed"