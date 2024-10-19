from rest_framework import serializers
from .models import scheduleData

class CampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = scheduleData
        fields = ['campaignScheduling','caption','imageUrl' ]

class ScheduleDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = scheduleData
        fields = ['id', 'imageUrl', 'caption']
        

