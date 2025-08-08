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

        required_fields = {
            "name": str,
            "email": str,
            "address": str,
            "phone": str,
            "topic": str,
            "message": str
        }

        errors = {}

        # Validación de campos obligatorios, tipos y contenido
        for field, field_type in required_fields.items():
            value = data.get(field)

            if value is None:
                errors[field] = "This field is required."
            elif not isinstance(value, field_type):
                errors[field] = f"Must be of type {field_type.__name__}."
            elif isinstance(value, str) and not value.strip():
                errors[field] = "This field cannot be empty."

        # Verificación de campos adicionales no permitidos
        allowed_fields = set(required_fields.keys())
        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            errors["extra_fields"] = f"Invalid fields: {', '.join(extra_fields)}."

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Campos generados automáticamente
        data["status"] = "new"
        data["timestamp"] = int(datetime.now().timestamp() * 1000)

        # Guardar en Firebase
        ref = db.reference(self.collection_name)
        new_resource = ref.push(data)

        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)