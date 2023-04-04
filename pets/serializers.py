from rest_framework import serializers
from .models import SexPet
from traits.serializers import TraitSerializer
from groups.serializers import GroupSerializer

class PetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    age = serializers.IntegerField(),
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=SexPet.choices
    )
    group = GroupSerializer()
    traits = TraitSerializer(many=True)
