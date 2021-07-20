from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

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
        first_name = request.POST['userFirst_name']
        last_name = request.POST['userLast_name']
        phone = request.POST['userPhone']
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
                    receive_promotions=receive_promotions, phone=phone)
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
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            email = request.POST['userEmail']
            password = request.POST['userPassword']

            flags = {
                'email_flag': False,
                'active_flag': False,
                'password_flag': False,
                'suspended_flag': False,
            }

            users = User.objects.filter(email=email)
            if len(users) == 0:
                flags['email_flag'] = True
                return render(request, 'bookstore/login.html', flags)

            if not users[0].is_active:
                flags['active_flag'] = True
                return render(request, 'bookstore/login.html', flags)

            user = authenticate(request, username=email, password=password)
            if user is None:
                flags['password_flag'] = True
                return render(request, 'bookstore/login.html', flags)

            if user.is_suspended:
                flags['suspended_flag'] = True
                return render(request, 'bookstore/login.html', flags)

            auth_login(request, user)
            return redirect('index')
        else:
            return render(request, 'bookstore/login.html')


def signout(request):
    logout(request)
    return redirect('login')


def book_detail(request, title):
    book = Book.objects.get(title=title)
    context = {
        'title': book.title,
        'book': book,
        #'other_books': Book.objects.filter(genre=book.genre).order_by('?'),
        'books': Book.objects.all(),
        # 'cartCount': getCartCount(request),
    }
    return render(request, 'bookstore/productDetails.html', context)


@login_required
def password_change_complete(request):
    # send_mail(
    #     "Your account password has changed",
    #     [request.user.email],
    #     fail_silently=False,
    # )
    return redirect('edit_profile')


def password_reset_complete(request):
    return redirect('login')


def getCartCount(request):
    if request.user.is_authenticated:
        return 10
    else:
        return ""


@login_required
def edit_profile(request):
    context = {
        'cartCount': getCartCount(request)
    }
    if request.method == "POST":
        pass
    return render(request, 'bookstore/editprofile.html', context)


def search(request):
    return render(request, 'bookstore/search.html')
