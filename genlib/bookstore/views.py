from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.http import HttpResponseRedirect, HttpResponse

from .models import *
from .tokens import account_activation_token

# Create your views here.
def index(request):
    context = {
        'best_sellers': Book.objects.filter(rating=5).order_by('?'),
        'new_arrivals': Book.objects.all(),
        # 'cartCount': getCartCount(request),
    }
    return render(request, 'bookstore/index.html', context)


def signup(request):
    if request.method == "POST":
        name = request.POST['userName']
        name = name.split(' ')
        if len(name) == 1:
            first_name, last_name = name[0], ""
        else:
            first_name, last_name = name[0], name[1]

        email = request.POST['userEmail']
        password = request.POST['userPassword']

        if "promotions" in request.POST.getlist("checks[]"):
            receive_promotions = True
        else:
            receive_promotions = False

        objects = User.objects.all()
        for o in objects:
            if o.email == email:
                return render(request, 'bookstore/sign-up.html', {'email_flag': True})

        user = User(first_name=first_name, last_name=last_name, email=email,
                    receive_promotions=receive_promotions)
        user.set_password(password)
        user.save()

        cart = Cart.objects.create_cart(user)

        current_site = get_current_site(request)
        mail_subject = "Activate your genlib account"
        mail_message = render_to_string('bookstore/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        EMAIL = EmailMessage(mail_subject, mail_message, to=[email])
        EMAIL.send()

        return render(request, 'bookstore/signup-confirmation.html')
    else:
        return render(request, 'bookstore/sign-up.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account is active. Sign in your account.")
    else:
        messages.error(request, "Account could not be activated.")
    
    return redirect('login')


def signup_confirmation(request):
    return render(request, 'bookstore/signup-confirmation.html')


def login(request):
    # if request.user.is_authenticated:
    #     # return redirect('index')
    # else:
    if request.method == "POST":
        email = request.POST['userEmail']
        password = request.POST['userPassword']

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if user.is_suspended:
                return render(request, 'bookstore/suspended.html')
            else:
                auth_login(request, user)
                return redirect('index')
        else:
            messages.info(request, "Email/password is incorrect")

    return render(request, 'bookstore/login.html')


# def getCartCount(request):
#     if request.user.is_authenticated:
#         return 10
#     else:
#         return ""