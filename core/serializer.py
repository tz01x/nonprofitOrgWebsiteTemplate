from re import I
from rest_framework import serializers
from .models import ClubEvent, Images

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Images 
        fields=['img','width','height']
class EventSerializer(serializers.ModelSerializer):
    url=serializers.URLField(source='get_absolute_url', read_only=True)
    images=ImageSerializer(many=True)
    class Meta:
        model=ClubEvent

        fields=['title','url','images']
        

'''
from core.models import ClubEvent,Images
from core.serializer import ImageSerializer,EventSerializer

event=ClubEvent.objects.all()
s=EventSerializer(event,many=True)

'''