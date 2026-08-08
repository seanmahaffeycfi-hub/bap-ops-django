from rest_framework import serializers
from .models import MileageEntry


class MileageEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageEntry
        fields = '__all__'