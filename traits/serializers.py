from rest_framework import serializers


class TraitSerializer(serializers.Serializer):
    trait_name = serializers.CharField(source='name')
    # name = serializers.CharField(source='trait_name')
