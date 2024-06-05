from django.urls import path
from .views import MachineOEEView, MachineOEEByDateView

urlpatterns = [
    path('oee/', MachineOEEView.as_view(), name='oee'),
    path('oee_by_date/', MachineOEEByDateView.as_view(), name='oee_by_date'),
]
