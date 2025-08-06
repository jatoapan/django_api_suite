from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
from datetime import datetime

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "contact_messages"

    def get(self, request):
        ref = db.reference(f'{self.collection_name}')
        data = ref.get()
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        ref = db.reference(f'{self.collection_name}')
        current_time  = datetime.now()
        epoch_timestamp = int(current_time.timestamp())
        data.update({"timestamp": epoch_timestamp })
        new_resource = ref.push(data)
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)