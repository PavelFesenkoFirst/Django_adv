from rest_framework import generics

from apps.api.v1.adv_board.serializers import AdvDetailSerializer, AdvEditingSerializer
from apps.adv_board.models import Advertisement



class AdvListDetailView(generics.ListAPIView):
    serializer_class = AdvDetailSerializer
    queryset = Advertisement.objects.all()

class AdvCreateView(generics.CreateAPIView):
    serializer_class = AdvDetailSerializer
    queryset = Advertisement.objects.all()


class AdvEditView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdvEditingSerializer
    queryset = Advertisement.objects.all()
