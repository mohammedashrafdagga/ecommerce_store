from django.shortcuts import render

# Create your views here.

def baskt_summary(request):
    return render(request, 'basket/summary.html')