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
        serializer.is_valid(raise_exception=True)
        traits_raw = serializer.validated_data.pop('traits')

        try:
            group = Group.objects.get(scientific_name__iexact=serializer.validated_data['group']['scientific_name'])
        except Group.DoesNotExist:
            group = Group.objects.create(**serializer.validated_data['group'])
        serializer.validated_data['group'] = group

        pet = Pet.objects.create(**serializer.validated_data)

        traits = []
        for curr in traits_raw:
            trait = Trait.objects.get(name__iexact=curr['name']) \
                if Trait.objects.filter(name__iexact=curr['name']).exists() \
                else Trait.objects.create(**curr)
            traits.append(trait)
        pet.traits.set(traits)
        serializer = PetSerializer(instance=pet)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, req: Request) -> Response:
        if 'trait' in req.query_params.keys():
            get_object_or_404(Trait, name__iexact=req.query_params['trait'])
            pets = Pet.objects.filter(traits__name__iexact=req.query_params['trait'])
        else:
            pets = Pet.objects.all()
        result_page = self.paginate_queryset(pets, req, view=self)
        serializer = PetSerializer(instance=result_page, many=True)
        return self.get_paginated_response(data=serializer.data)

class PetDetailsView(APIView, CustomPagination):
    def get(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def delete(self, req: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, req: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'group' in serializer.validated_data.keys():
            group_raw = serializer.validated_data.pop('group')
            print(group_raw['scientific_name'])
            name = group_raw['scientific_name']
            group, created = Group.objects.get_or_create(
                scientific_name=name
            )
            pet.group = group

        if 'traits' in serializer.validated_data.keys():
            traits_raw = serializer.validated_data.pop('traits')
            traits = []
            for curr in traits_raw:
                trait, created = Trait.objects.get_or_create(name__iexact=curr['name'])
                traits.append(trait)
            pet.traits.set(traits)

        for key, value in serializer.validated_data.items():

            setattr(pet, key, value)
        pet.save()

        serializer = PetSerializer(instance=pet)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

