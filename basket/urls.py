from django.urls import path
from . import views


app_name = 'basket'

urlpatterns = [
    path('', views.baskt_summary, name='basket-summary')
]