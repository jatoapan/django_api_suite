from django.shortcuts import render
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db

# Create your views here.


class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "votes"

    def get(self, request):
        ref = db.reference(self.collection_name)
        data = ref.get()
        if not data:
            return Response({"error": "No data found."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(data, status=status.HTTP_200_OK)

    
    def post(self, request):
      data = request.data
      # Referencia a la colección
      ref = db.reference(f'{self.collection_name}')
      current_time  = datetime.now()
      custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
      data.update({"timestamp": custom_format })
      # push: Guarda el objeto en la colección
      new_resource = ref.push(data)
      # Devuelve el id del objeto guardado
      return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
