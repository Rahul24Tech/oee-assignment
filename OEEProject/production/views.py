from rest_framework import generics
from rest_framework.response import Response
from django.db.models import Sum
from .models import Machines, ProductionLog
from .serializers import MachinesSerializer, ProductionLogSerializer
from datetime import timedelta

class OEECalculation:
    @staticmethod
    def calculate_oee(machine):
        production_logs = ProductionLog.objects.filter(machine=machine)
        
        total_available_time = 3 * 8  # 3 shifts of 8 hours each
        total_operating_time = production_logs.aggregate(Sum('duration'))['duration__sum'] or 0
        unplanned_downtime = total_available_time - total_operating_time
        
        ideal_cycle_time = 5 / 60  # 5 minutes converted to hours
        actual_output = production_logs.count()
        available_operating_time = actual_output * ideal_cycle_time
        
        no_of_good_products = production_logs.filter(duration=ideal_cycle_time).count()
        total_products_produced = actual_output
        
        if total_available_time == 0 or available_operating_time == 0 or total_products_produced == 0:
            return 0
        
        availability = (total_available_time - unplanned_downtime) / total_available_time * 100
        performance = available_operating_time / total_available_time * 100
        quality = no_of_good_products / total_products_produced * 100
        
        oee = (availability * performance * quality) / 100
        return oee

class MachineOEEView(generics.ListAPIView):
    queryset = Machines.objects.all()
    serializer_class = MachinesSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for machine in queryset:
            oee = OEECalculation.calculate_oee(machine)
            data.append({
                'machine_name': machine.machine_name,
                'machine_serial_no': machine.machine_serial_no,
                'oee': oee,
            })
        return Response(data)

class MachineOEEByDateView(generics.ListAPIView):
    serializer_class = MachinesSerializer

    def get_queryset(self):
        machine_id = self.request.query_params.get('machine_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if machine_id:
            queryset = Machines.objects.filter(id=machine_id)
        else:
            queryset = Machines.objects.all()
        
        if start_date and end_date:
            queryset = queryset.filter(productionlog__start_time__gte=start_date, productionlog__end_time__lte=end_date)
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = []
        for machine in queryset:
            oee = OEECalculation.calculate_oee(machine)
            data.append({
                'machine_name': machine.machine_name,
                'machine_serial_no': machine.machine_serial_no,
                'oee': oee,
            })
        return Response(data)
