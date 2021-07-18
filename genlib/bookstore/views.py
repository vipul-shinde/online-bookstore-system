from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import *

# Create your views here.
def index(request):
    context = {
        'title': 'index',
        'best_sellers': Book.objects.filter(rating=5).order_by('?'),
        'new_arrivals': Book.objects.all(),
        'cartCount': getCartCount(request),
    }
    return render(request, 'bookstore/index.html', context)


def signup(request):
    if request.method == "POST":
        return HttpResponseRedirect('bookstore/signup-confirmation.html')
    else:
        return render(request, 'bookstore/sign-up.html')
    # if request.method == "POST":

def signup_confirmation(request):
    return render(request, 'bookstore/signup-confirmation.html')



def getCartCount(request):
    if request.user.is_authenticated:
        return 10
    else:
        return ""