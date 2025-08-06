from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

data_list = []

data_list.append({"id": str(uuid.uuid4()), "name": "User01", 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False})

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get('is_active', False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'name' not in data or 'email' not in data:
            return Response({"error": "Nombre y email requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        
        data['id'] = str(uuid.uuid4())
        data['is_active'] = True
        data_list.append(data)
        return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def _find_item_by_id(self, item_id):
        """Función auxiliar para encontrar un elemento por su ID"""
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                return i, item
        return None, None
    
    def put(self, request, id):
        """PUT - Reemplaza completamente los datos de un elemento, excepto el ID"""
        data = request.data
        
        # El ID viene del parámetro de la URL
        item_id = id
        index, existing_item = self._find_item_by_id(item_id)
        
        # Si no se encuentra el elemento, retornar error
        if existing_item is None:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar campos obligatorios
        if 'name' not in data or 'email' not in data:
            return Response({"error": "Nombre y email son requeridos."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear nuevo elemento manteniendo solo el ID del original
        new_item = {
            'id': item_id,  # Mantener el ID original
            'name': data['name'],
            'email': data['email'],
            'is_active': data.get('is_active', True)  # Valor por defecto si no se proporciona
        }
        
        # Reemplazar el elemento en la lista
        data_list[index] = new_item
        
        return Response({'message': 'Elemento actualizado completamente.', 'data': new_item}, status=status.HTTP_200_OK)
    
    def patch(self, request, id):
        """PATCH - Actualiza parcialmente los campos del elemento identificado por su ID"""
        data = request.data
        
        # El ID viene del parámetro de la URL
        item_id = id
        index, existing_item = self._find_item_by_id(item_id)
        
        # Si no se encuentra el elemento, retornar error
        if existing_item is None:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar solo los campos proporcionados, manteniendo los valores existentes
        updated_item = existing_item.copy()
        
        # Actualizar campos si están presentes en la solicitud (excepto el ID)
        for field in ['name', 'email', 'is_active']:
            if field in data:
                updated_item[field] = data[field]
        
        # Reemplazar el elemento en la lista
        data_list[index] = updated_item
        
        return Response({'message': 'Elemento actualizado parcialmente.', 'data': updated_item}, status=status.HTTP_200_OK)
    
    def delete(self, request, id):
        """DELETE - Elimina lógicamente un elemento del arreglo según el identificador"""
        # El ID viene del parámetro de la URL
        item_id = id
        index, existing_item = self._find_item_by_id(item_id)
        
        # Si no se encuentra el elemento, retornar error
        if existing_item is None:
            return Response({"error": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si el elemento ya está inactivo
        if not existing_item.get('is_active', True):
            return Response({"error": "El elemento ya está eliminado."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminación lógica: cambiar is_active a False
        existing_item['is_active'] = False
        data_list[index] = existing_item
        
        return Response({'message': 'Elemento eliminado lógicamente.', 'data': existing_item}, status=status.HTTP_200_OK)