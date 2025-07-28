from django.urls import path
from . import views
import firebase_admin
from firebase_admin import credentials

# Coloque la ruta relativa al archivo con la clave privada
FIREBASE_CREDENTIALS_PATH = credentials.Certificate("secrets/landing-key.json")

# Inicialice la conexión con el Realtime Database con la clave privada y la URL de referencia
firebase_admin.initialize_app(FIREBASE_CREDENTIALS_PATH, {
   'databaseURL': 'https://proyecto-kain-landing-page-default-rtdb.firebaseio.com/'
})

urlpatterns = [
    path("", views.DemoRestApi.as_view(), name="demo_rest_api_collection"),
    path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources"),
    path("<str:id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]