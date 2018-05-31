from rest_framework import serializers
from .models import SurgeAlert, Subscription
from api.serializers import MiniEventSerializer

class SurgeAlertSerializer(serializers.ModelSerializer):
    event = MiniEventSerializer()
    class Meta:
        model = SurgeAlert
        fields = ('atype', 'category', 'operation', 'message', 'deployment_needed', 'is_private', 'event',)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ('user', 'stype', 'rtype', 'country', 'region', 'dtype', 'lookup_id',)
