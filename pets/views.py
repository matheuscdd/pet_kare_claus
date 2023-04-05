from rest_framework.views import APIView, status, Request
from rest_framework.response import Response
from .serializers import PetSerializer
from .models import Pet
from groups.models import Group
from pet_kare.pagination import CustomPagination
from traits.models import Trait
from django.shortcuts import get_object_or_404


class PetsView(APIView, CustomPagination):
    def post(self, req: Request) -> Response:
        serializer = PetSerializer(data=req.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        traits_raw = serializer.validated_data.pop('traits')

        try:
            group = Group.objects.get(scientific_name__iexact=serializer.validated_data['group']['scientific_name'])
        except Group.DoesNotExist:
            group = Group.objects.create(**serializer.validated_data['group'])
        serializer.validated_data['group'] = group

        pet = Pet.objects.create(**serializer.validated_data)

        for curr in traits_raw:
            trait = Trait.objects.get(name__iexact=curr['name']) \
                if Trait.objects.filter(name__iexact=curr['name']).exists() \
                else Trait.objects.create(**curr)
            pet.traits.add(trait)

        serializer = PetSerializer(instance=pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, req, view=self)
        serializer = PetSerializer(instance=result_page, many=True)
        return self.get_paginated_response(data=serializer.data)
