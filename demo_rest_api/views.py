from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    
    def get(self, request):
        try:
            active_items = [item for item in data_list if item.get('is_active', False)]
            return Response({
                'message': 'Elementos activos obtenidos exitosamente.',
                'data': active_items,
                'count': len(active_items)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor al obtener elementos.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = request.data
            
            if 'name' not in data or 'email' not in data:
                return Response({
                    'error': 'Faltan campos requeridos.',
                    'required_fields': ['name', 'email']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not data.get('name') or not data.get('email'):
                return Response({
                    'error': 'Los campos name y email no pueden estar vacíos.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            new_item = {
                'id': str(uuid.uuid4()),
                'name': data['name'],
                'email': data['email'],
                'is_active': True
            }
            
            data_list.append(new_item)
            
            return Response({
                'message': 'Dato guardado exitosamente.',
                'data': new_item
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor al crear elemento.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def put(self, request, id):
        try:
            data = request.data
            
            if 'name' not in data or 'email' not in data:
                return Response({
                    'error': 'Los campos name y email son requeridos para PUT.',
                    'required_fields': ['name', 'email']
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for i, item in enumerate(data_list):
                if item['id'] == id:
                    new_item = {
                        'id': id,
                        'name': data['name'],
                        'email': data['email'],
                        'is_active': data.get('is_active', True)
                    }
                    data_list[i] = new_item
                    
                    return Response({
                        'message': 'Elemento actualizado completamente.',
                        'data': new_item
                    }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor al actualizar elemento.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def patch(self, request, id):
        try:
            data = request.data
            
            if not data:
                return Response({
                    'error': 'No se enviaron datos para actualizar.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for item in data_list:
                if item['id'] == id:
                    for key, value in data.items():
                        if key != 'id':
                            item[key] = value
                    
                    return Response({
                        'message': 'Elemento actualizado parcialmente.',
                        'data': item
                    }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor al actualizar parcialmente elemento.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, id):
        try:
            for item in data_list:
                if item['id'] == id:
                    if not item.get('is_active', True):
                        return Response({
                            'message': 'El elemento ya estaba eliminado.',
                            'data': item
                        }, status=status.HTTP_200_OK)
                    
                    item['is_active'] = False
                    
                    return Response({
                        'message': 'Elemento eliminado lógicamente.',
                        'data': item
                    }, status=status.HTTP_200_OK)
            
            return Response({
                'error': 'Elemento no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor al eliminar elemento.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)