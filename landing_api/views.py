from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "contact_messages"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()
        if not data:
            return Response({"error": "No data found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        # Validación de la estructura de los datos
        required_fields = {
            "name": str,
            "email": str,
            "address": str,
            "phone": str,
            "status": str,
            "topic": str
        }

        # Verifica que todos los campos obligatorios estén presentes y con el tipo correcto
        for field, field_type in required_fields.items():
            if field not in data:
                return Response({"error": f"Field '{field}' is required."}, status=status.HTTP_400_BAD_REQUEST)
            if not isinstance(data[field], field_type):
                return Response({"error": f"Field '{field}' must be of type {field_type.__name__}."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificación de campos adicionales no permitidos
        allowed_fields = set(required_fields.keys())
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            return Response({"error": f"Invalid fields: {', '.join(extra_fields)}."}, status=status.HTTP_400_BAD_REQUEST)

        # Agregar timestamp a los datos
        current_time = datetime.now()
        epoch_timestamp = int(current_time.timestamp())
        data.update({"timestamp": epoch_timestamp})

        # Guardar en Firebase
        ref = db.reference(self.collection_name)
        new_resource = ref.push(data)

        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
