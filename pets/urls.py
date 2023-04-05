from django.urls import path
from .views import PetsView, PetDetailsView

urlpatterns = [
    path('pets/', PetsView.as_view()),
    path('pets/<int:pet_id>/', PetDetailsView.as_view())
]
