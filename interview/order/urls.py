
from django.urls import path
from interview.order.views import OrderListCreateView, OrderTagListCreateView, OrdersBetweenDatesView


urlpatterns = [
    path('tags/', OrderTagListCreateView.as_view(), name='order-detail'),
    path('between-dates/', OrdersBetweenDatesView.as_view(), name='orders-between-dates'),
    path('', OrderListCreateView.as_view(), name='order-list'),

]
