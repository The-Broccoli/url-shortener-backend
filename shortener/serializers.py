from rest_framework import serializers
from .models import Urls


class UrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Urls
        fields = '__all__'



