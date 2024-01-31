from rest_framework import generics
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def patch(self, request:Request, *args, **kwargs) -> Response:
        order = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
        order.is_active = False
        order.save()

        return Response({"message": "Order set to inactive"}, status=200)
