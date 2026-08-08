from rest_framework import serializers
from .models import VaseReceived, VaseReturned


class VaseReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaseReceived
        fields = '__all__'


class VaseReturnedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaseReturned
        fields = '__all__'