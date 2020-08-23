from rest_framework import serializers

from apps.adv_board.models import Advertisement


class AdvDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class AdvEditingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ('title', 'description', 'price', 'location_a')
