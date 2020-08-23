from django.urls import path
from rest_framework import routers

from apps.api.v1.adv_board.views import AdvCreateView, AdvEditView, AdvListDetailView

urlpatterns = [
    path('adv_create/', AdvCreateView.as_view()),
    path('adv_edit/<int:pk>', AdvEditView.as_view()),
    path('all/', AdvListDetailView.as_view()),
]
