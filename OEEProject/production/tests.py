from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Machines, ProductionLog
from datetime import datetime, timedelta

class OEECalculationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.machine = Machines.objects.create(machine_name="Machine1", machine_serial_no="12345")
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=5)
        ProductionLog.objects.create(
            cycle_no="CN001", unique_id="UID001", material_name="Material1",
            machine=self.machine, start_time=start_time, end_time=end_time, duration=0.0833)
        
    def test_oee_calculation(self):
        response = self.client.get(reverse('oee'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('oee', response.data[0])
        
    def test_oee_by_date(self):
        response = self.client.get(reverse('oee_by_date'), {'machine_id': self.machine.id, 'start_date': '2024-01-01', 'end_date': '2024-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('oee', response.data[0])
