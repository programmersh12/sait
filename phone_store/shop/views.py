from django.shortcuts import render
from .models import Phone
# Create your views here.
def home(request):
    phones = Phone.objects.all()
    return render(request, 'shop/home.html', {'phones': phones})