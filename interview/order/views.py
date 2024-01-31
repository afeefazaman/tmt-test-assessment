from django.utils.dateparse import parse_date

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class OrdersBetweenDatesView(generics.ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request: Request, *args, **kwargs) -> Response:
        start_date_str = self.request.query_params.get('start_date')
        embargo_date_str = self.request.query_params.get('embargo_date')

        if not start_date_str or not embargo_date_str:
            return Response({"message": 'Both start_date and embargo_date parameters are required.'}, status=400)

        try:
            start_date = parse_date(start_date_str)
            embargo_date = parse_date(embargo_date_str)
        except ValueError:
            return Response({"message":'Invalid date format.'},  status=400)
        
        if not start_date or not embargo_date:
            return Response({"message": 'start_date and/or embargo_date parameter(s) are incorrect.'}, status=400)

        if start_date > embargo_date:
            return Response({"message": 'start_date cannot be later than embargo_date.'}, status=400)

        orders = Order.objects.filter(start_date__gte=start_date, embargo_date__lte=embargo_date)
        serializer = self.serializer_class(orders, many=True)

        return Response(serializer.data, status=200)
