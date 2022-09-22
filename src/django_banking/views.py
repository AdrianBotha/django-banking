from datetime import datetime

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from django_banking import tasks
from django_banking.models import Trade
from django_banking.serializers import TradeCSVSerializer, TradeSerializer
from django_banking.services import csv_import


class TradeCSVUploadView(APIView):
    serializer_class = TradeCSVSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        new_file_name = csv_import.save_file(file)
        import_obj = csv_import.log_file_upload(file.name, new_file_name)
        tasks.import_trades_csv.delay(import_obj.id)
        return Response({'detail': 'success'})


class TradeViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    http_method_names = ('get',)

    def get_queryset(self):
        queryset = self.queryset

        country = self.request.query_params.get('country')
        if country:
            queryset = queryset.filter(country__slug=country)

        date = self.request.query_params.get('date')
        if date:
            date = datetime.strptime(date, '%Y/%m/%d')
            # In hindsight, poor choice to name the date field date as it looks confusing
            queryset = queryset.filter(date__date=date)

        return queryset
