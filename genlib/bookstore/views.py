from django.shortcuts import render
from django.http import HttpResponseRedirect


# Create your views here.
def index(request):
    context = {
        'title': 'index'
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
        return ""
    else:
        return ""