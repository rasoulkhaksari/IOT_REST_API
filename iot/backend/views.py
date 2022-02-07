import logging
from django.conf import settings
from rest_framework import permissions,status 
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view,permission_classes,renderer_classes
from .serializers import IOTdeviceSerializer 
from .models import IOTdevice
import json
import pandas as pd
from datetime import datetime,timedelta

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([JSONRenderer])
def device_create(request):
    try:
        device_data = JSONParser().parse(request)
        if any(item['customer_id'] != request.user.customer.customer_id for item in device_data):
            raise ValueError("you can only save your own data, customer ID in data should be your ID")
        device_serializer = IOTdeviceSerializer(data=device_data,many=True)
        if device_serializer.is_valid():
            device_serializer.save()
            return Response(data=device_serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=device_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        logger.error(exc.args[0])
        return Response(data={'error':'Something went wrong. Please check your parameter values and try again.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@renderer_classes([JSONRenderer])
def device_list(request):
    try:
        start_date = request.GET.get('start',(datetime.now() - timedelta(int(settings.QUERY_LIMIT_DAYS))).isoformat())
        end_date = request.GET.get('end',datetime.now().isoformat())
        aggregation_size=int(request.GET.get('aggregation_size',5))
        customer_id = request.GET.get('customer_id',None)
        device_id = request.GET.get('device_id',None)

        queryset = IOTdevice.objects
        if not request.user.is_superuser:
            queryset = queryset.filter(customer_id=request.user.customer.customer_id)
        if not customer_id is None:
            queryset = queryset.filter(customer_id=customer_id)
        if not device_id is None:
            queryset = queryset.filter(device_id=device_id)

        queryset = queryset.filter(timestamp__range=(start_date, end_date))
        serializer = IOTdeviceSerializer(queryset, many=True)
        df=pd.read_json(json.dumps(serializer.data))
        df.set_index('timestamp',inplace=True)
        result = []
        df = df.groupby(['customer_id','device_id']).resample(f'{aggregation_size}min').agg({'reading':'mean'})
        for customer in df.index.levels[0]:
            for device in df.index.levels[1]:
                data={
                    "device_id":device,
                    "customer_id":customer,
                    "from":start_date,
                    "to":end_date,
                    "aggregation_size_minutes":aggregation_size,
                    "aggregated_values":[]
                }
                for timestamp,row in df.loc[(customer,device)].iterrows():
                    data["aggregated_values"].append({"from":timestamp.isoformat(),"value":round(row['reading'],2) })
                result.append(data)

        return Response(result)
    except Exception as exc:
        logger.error(exc.args[0])
        return Response(data={'error':'Something went wrong. Please check your parameter values and try again.'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

