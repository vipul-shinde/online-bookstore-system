from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.db.models import Sum

from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.http import HttpResponseRedirect, HttpResponse

from copy import deepcopy
import datetime
from .models import *
from .tokens import account_activation_token

# Create your views here.
def index(request):
    context = {
        'best_sellers': Book.objects.filter(rating=5).order_by('?'),
        'new_arrivals': Book.objects.all(),
        'cartCount': getCartCount(request),
    }

    if request.method == "POST":
        if request.POST.get("espionage_cat"):
            return search_function(request, "espionage", True)
        if request.POST.get("contemporary_cat"):
            return search_function(request, "contemporary", True)
        if request.POST.get("classics_cat"):
            return search_function(request, "classics", True)
        if request.POST.get("literary_cat"):
            return search_function(request, "literary", True)
        if request.POST.get("horror_cat"):
            return search_function(request, "horror", True)
        if request.POST.get("all_cat"):
            return search_function(request, "all", True)
        
        if request.POST.get("search_button"):
            return search_function(request, request.POST["search"])

        if request.POST.get("add_to_cart"):
            err = add_to_cart(request, request.POST['add_to_cart'], 1)
            if err == "redirect":
                return redirect('login')
            elif err == "out_of_stock":
                context['out_of_stock_flag'] = True
                return render(request, 'bookstore/index.html', context)

        context['cartCount'] = getCartCount(request)
        return render(request, 'bookstore/index.html', context)
    else:
        return render(request, 'bookstore/index.html', context)


def signup(request):
    if request.method == "POST":
        if request.POST['something'] == "not_working":
            return render(request, 'bookstore/sign-up.html', {'email_flag': False})
        first_name = request.POST['userFirst_name']
        last_name = request.POST['userLast_name']
        phone = request.POST['userPhone']
        email = request.POST['userEmail']
        password = request.POST['userPassword']

        if "promotions" in request.POST.getlist("checks[]"):
            receive_promotions = True
        else:
            receive_promotions = False

        if request.POST['userStreet'] != "":
            street = request.POST['userStreet']
            city = request.POST['userCity']
            state = request.POST['userState']
            zip_code = request.POST['userZip_code']
            county = request.POST['userCounty']
            country = request.POST['userCountry']
        else:
            street = ""
            city = ""
            state = ""
            zip_code = ""
            county = ""
            country = ""

        if request.POST['userCard_name'] != "":
            card_count = 1
            card_name = request.POST['userCard_name']
            card_num = request.POST['userCard_num']
            card_exp = f"{request.POST.get('userCard_month')}/{request.POST.get('userCard_year')}"
            card_cvv = request.POST['userCard_cvv']
            card_four = card_num[-4:]
        else:
            card_count = 0
            card_name = ""
            card_num = ""
            card_exp = ""
            card_cvv = ""
            card_four = ""


        objects = User.objects.all()
        for o in objects:
            if o.email == email:
                return render(request, 'bookstore/sign-up.html', {'email_flag': True})

        user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    receive_promotions=receive_promotions,
                    phone=phone,
                    street=street,
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    county=county,
                    country=country,
                    card_count=card_count,
                    card_name1=card_name,
                    card_num1=card_num,
                    card_exp1=card_exp,
                    card_cvv1=card_cvv,
                    card_four1=card_four)
        user.set_password(password)
        user.save()

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
        return render(request, 'bookstore/sign-up.html', {'email_flag': False})


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
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('index')
        else:
            return render(request, 'bookstore/login.html')


def signout(request):
    logout(request)
    return redirect('login')


@login_required
def password_change_complete(request):
    mail_subject = "Genlib account password changed"
    mail_message = "Your account password has been changed."
    EMAIL = EmailMessage(mail_subject, mail_message, to=[request.user.email])
    EMAIL.send()
    return redirect('edit_profile')


def password_reset_complete(request):
    return redirect('login')


def getCartCount(request):
    if request.user.is_authenticated:
        count = 0
        cart_items = CartItem.objects.filter(user=request.user)
        for cart_item in cart_items:
            count += cart_item.quantity
        return count
    else:
        return ""


def book_detail(request, title):
    book = Book.objects.get(title=title)
    context = {
        'title': book.title,
        'book': book,
        #'other_books': Book.objects.filter(genre=book.genre).order_by('?'),
        'books': Book.objects.all(),
        'cartCount': getCartCount(request),
    }
    if request.method == "POST":
        if request.POST.get("search_button"):
            return search_function(request, request.POST["search"])

        if request.POST.get("add_to_cart"):
            err = add_to_cart(request, book.isbn, 1)
            if err == "redirect":
                return redirect('login')
            elif err == "out_of_stock":
                context['out_of_stock_flag'] = True
                return render(request, 'bookstore/productDetails.html', context)

            context['cartCount'] = getCartCount(request)
            return render(request, "bookstore/productDetails.html", context)
    else:
        return render(request, 'bookstore/productDetails.html', context)

@login_required
def edit_profile(request):
    payment_cards = []
    if request.user.card_four1 != "":
        payment_cards.append(request.user.card_four1)
    if request.user.card_four2 != "":
        payment_cards.append(request.user.card_four2)
    if request.user.card_four3 != "":
        payment_cards.append(request.user.card_four3)
    context = {
        'cartCount': getCartCount(request),
        'payment_cards': payment_cards,
        'delete_flag': False,
        'three_cards': False,
    }

    if request.method == "POST":
        if request.POST.get("search_button"):
            return search_function(request, request.POST['search'])

        if request.POST['something'] == "not_working":
            return render(request, 'bookstore/editprofile.html', context)
        changes_made = []
        orig_user = deepcopy(request.user)
        user = request.user
        checks = request.POST.getlist("checks[]")
        
        if "delete_address" in checks:
            changes_made.append("delete_address")
            user.street = ""
            user.city = ""
            user.state = ""
            user.zip_code = ""
            user.county = ""
            user.country = ""
        else:
            user.street = request.POST['userStreet']
            user.city = request.POST['userCity']
            user.state = request.POST['userState']
            user.zip_code = request.POST['userZip']
            user.county = request.POST['userCounty']
            user.country = request.POST['userCountry']

        if request.POST['receive_promotion'] == "Yes":
            user.receive_promotions = True
        else:
            user.receive_promotions = False

        if user.receive_promotions != orig_user.receive_promotions:
            if user.receive_promotions == True:
                changes_made.append("add_promotion")
            else:
                changes_made.append("remove_promotion")

        user.first_name = request.POST['userFirst_name']
        user.last_name = request.POST['userLast_name']
        user.phone = request.POST['userPhone']
        
        if user.first_name != orig_user.first_name:
            changes_made.append("first_name")
        if user.last_name != orig_user.last_name:
            changes_made.append("last_name")
        if user.phone != orig_user.phone:
            changes_made.append("phone")
        if user.street != orig_user.street:
            changes_made.append("street")
        if user.city != orig_user.city:
            changes_made.append("city")
        if user.state != orig_user.state:
            changes_made.append("state")
        if user.zip_code != orig_user.zip_code:
            changes_made.append("zip_code")
        if user.county != orig_user.county:
            changes_made.append("county")
        elif user.country != orig_user.country:
            changes_made.append("country")

        if request.POST.get("card_option", "Select") != "Select":
            if request.POST.get("card_option") == "Delete":
                if user.card_count == 0:
                    context['delete_flag'] = True
                    return render(request, 'bookstore/editprofile.html', context)

                user.card_count -= 1
                if user.card_four1 == request.POST["cards"]:
                    changes_made.append("card_delete_1")
                    user.card_name1 = ""
                    user.card_num1 = ""
                    user.card_exp1 = ""
                    user.card_cvv1 = ""
                    user.card_four1 = ""
                elif user.card_four2 == request.POST["cards"]:
                    changes_made.append("card_delete_2")
                    user.card_name2 = ""
                    user.card_num2 = ""
                    user.card_exp2 = ""
                    user.card_cvv2 = ""
                    user.card_four2 = ""
                elif user.card_four3 == request.POST["cards"]:
                    changes_made.append("card_delete_3")
                    user.card_name3 = ""
                    user.card_num3 = ""
                    user.card_exp3 = ""
                    user.card_cvv3 = ""
                    user.card_four3 = ""

                payment_cards = []
                if user.card_four1 != "":
                    payment_cards.append(user.card_four1)
                if user.card_four2 != "":
                    payment_cards.append(user.card_four2)
                if user.card_four3 != "":
                    payment_cards.append(user.card_four3)
                context['payment_cards'] = payment_cards

            else:
                if user.card_count == 3:
                    context['three_cards'] = True
                    return render(request, 'bookstore/editprofile.html', context)
                
                user.card_count += 1
                if user.card_four1 == "":
                    changes_made.append("card_save_1")
                    user.card_name1 = request.POST["card_name"]
                    user.card_num1 = request.POST["card_num"]
                    user.card_exp1 = f'{request.POST.get("card_month")}/{request.POST.get("card_year")}'
                    user.card_cvv1 = request.POST["card_cvv"]
                    user.card_four1 = request.POST["card_num"][-4:]
                elif user.card_four2 == "":
                    changes_made.append("card_save_2")
                    user.card_name2 = request.POST["card_name"]
                    user.card_num2 = request.POST["card_num"]
                    user.card_exp2 = f'{request.POST.get("card_month")}/{request.POST.get("card_year")}'
                    user.card_cvv2 = request.POST["card_cvv"]
                    user.card_four2 = request.POST["card_num"][-4:]
                elif user.card_four3 == "":
                    changes_made.append("card_save_3")
                    user.card_name3 = request.POST["card_name"]
                    user.card_num3 = request.POST["card_num"]
                    user.card_exp3 = f'{request.POST.get("card_month")}/{request.POST.get("card_year")}'
                    user.card_cvv3 = request.POST["card_cvv"]
                    user.card_four3 = request.POST["card_num"][-4:]

                payment_cards = []
                if user.card_four1 != "":
                    payment_cards.append(user.card_four1)
                if user.card_four2 != "":
                    payment_cards.append(user.card_four2)
                if user.card_four3 != "":
                    payment_cards.append(user.card_four3)
                context['payment_cards'] = payment_cards

        user.save()

        message = ""
        if "delete_address" in changes_made:
            message += "* Your address has been deleted\n"
        if "add_promotion" in changes_made:
            message += "* You have opted in to receive promotions\n"
        if "remove_promotion" in changes_made:
            message += "* You will no longer receive promotions\n"
        for x in ["first_name", "last_name", "phone"]:
            if x in changes_made:
                message += f"* Your {x} has been updated\n"
        if "delete_address" not in changes_made:
            for x in ["street", "city", "state", "zip_code", "county", "country"]:
                if x in changes_made:
                    message += f"* Your {x} has been updated\n"
        if "card_delete_1" in changes_made:
            message += f"* Your card ending in {orig_user.card_four1} has been removed\n"
        if "card_delete_2" in changes_made:
            message += f"* Your card ending in {orig_user.card_four2} has been removed\n"
        if "card_delete_3" in changes_made:
            message += f"* Your card ending in {orig_user.card_four3} has been removed\n"
        if "card_save_1" in changes_made:
            message += f"* Card ending in {user.card_four1} has been added to your account\n"
        if "card_save_2" in changes_made:
            message += f"* Card ending in {user.card_four2} has been added to your account\n"
        if "card_save_3" in changes_made:
            message += f"* Card ending in {user.card_four3} has been added to your account\n"

        mail_subject = "Changes made to your genlib account"
        mail_message = message

        if mail_message != "":
            EMAIL = EmailMessage(mail_subject, mail_message, to=[user.email])
            EMAIL.send()

        return render(request, 'bookstore/editprofile.html', context)
    else:
        return render(request, 'bookstore/editprofile.html', context)


# @login_required
def add_to_cart(request, isbn, quantity):
    if request.user.is_authenticated:
        user = request.user
        book = Book.objects.filter(isbn=isbn)[0]
        if book.stock - quantity < 0:
                return "out_of_stock"

        if CartItem.objects.filter(user=user, book=book):            
            new_quantity = CartItem.objects.get(user=user, book=book).quantity + quantity
            book.stock -= quantity
            book.save()
            CartItem.objects.filter(user=user, book=book).update(quantity=new_quantity)
        else:
            book.stock -= quantity
            book.save()
            cart_item = CartItem.objects.add_cart_item(user, book, quantity)
        return "success"
    else:
        return "redirect"


def browse_books(request):
    def get_context():
        context = {
            'cartCount': getCartCount(request),
            'books': Book.objects.all()
        }
        return context
    context = get_context()

    if request.method == "POST":
        if request.POST.get("search_button"):
            return search_function(request, request.POST["search"])

        if request.POST.get("add_to_cart"):
            err = add_to_cart(request, request.POST['add_to_cart'], 1)
            if err == "redirect":
                return redirect('login')
            elif err == "out_of_stock":
                context['out_of_stock_flag'] = True
                return render(request, 'bookstore/browse-books.html', context)
        context = get_context()
        return render(request, 'bookstore/browse-books.html', context)
    else:
        return render(request, 'bookstore/browse-books.html', context)

def cart(request):
    def get_context():
        books = CartItem.objects.filter(user=request.user)
        prices = []
        for book in books:
            price = int(book.quantity)*float(book.book.cost)
            price = f"{price:.2f}"
            prices.append(price)
        total_cost = 0
        for book in books:
            total_cost += int(book.quantity)*float(book.book.cost)
        total_cost = f"{total_cost:.2f}"
        context = {
            'cartCount': getCartCount(request),
            'books_in_cart': zip(CartItem.objects.filter(user=request.user), prices),
            'total_cost': total_cost,
        }
        return context
    context = get_context()

    if request.method == "POST":
        if request.POST.get("search_button", "None") == "search_button":
            return search_function(request, request.POST["search"])

        if request.POST.get("cross_button"):
            cart_item = CartItem.objects.filter(user=request.user, book=Book.objects.get(isbn=request.POST.get("cross_button")))[0]
            book = Book.objects.get(isbn=request.POST.get("cross_button"))
            
            book.stock += cart_item.quantity
            book.save()
            cart_item.delete()
            context = get_context()
            return render(request, 'bookstore/cart.html', context)

        if request.POST.get("minus_button"):
            cart_item = CartItem.objects.filter(user=request.user, book=Book.objects.get(isbn=request.POST.get("minus_button")))[0]
            if cart_item.quantity == 0:
                return render(request, 'bookstore/cart.html', context)
            else:
                book = Book.objects.get(isbn=request.POST.get("minus_button"))
                # if book.stock == 0:
                #     context["minus_flag"] = True
                #     return render(request, 'bookstore/cart.html', context)

                book.stock += 1
                book.save()
                cart_item.quantity -= 1
                if cart_item.quantity == 0:
                    cart_item.delete()
                else:
                    cart_item.save()

            context = get_context()

        if request.POST.get("plus_button"):
            book = Book.objects.get(isbn=request.POST.get("plus_button"))
            cart_item = CartItem.objects.filter(user=request.user, book=Book.objects.get(isbn=request.POST.get("plus_button")))[0]

            if book.stock == 0:
                context["minus_flag"] = True
                return render(request, 'bookstore/cart.html', context)

            book.stock -= 1
            book.save()
            cart_item.quantity += 1
            cart_item.save()

            context = get_context()

        if request.POST.get("continue_checkout"):
            cartCount = getCartCount(request)
            if cartCount == 0:
                context['checkout_flag'] = True
                return render(request, 'bookstore/cart.html', context)
            else:
                return redirect('shipping')
        return render(request, 'bookstore/cart.html', context)
    else:
        return render(request, 'bookstore/cart.html', context)


def search_function(request, s, advanced=False):
    def get_context():
        context = {
            'cartCount': getCartCount(request),
            'books': Book.objects.all(),
        }
        return context
    context = get_context()

    if request.method == "POST":
        # if request.POST.get("search_button"):
        #     return search_function(request, request.POST["search"])

        if request.POST.get("add_to_cart"):
            err = add_to_cart(request, request.POST['add_to_cart'], 1)
            if err == "redirect":
                return redirect('login')
            elif err == "out_of_stock":
                context['out_of_stock_flag'] = True
                return render(request, 'bookstore/search.html', context)
        context = get_context()
        return render(request, 'bookstore/search.html', context)
    else:
        return render(request, 'bookstore/search.html', context)

def search(request):
    context = {
        'cartCount': getCartCount(request),
    }
    return render(request, 'bookstore/search.html', context)

def admin_home(request):
    return render(request, 'bookstore/admin-home.html')

def order_history(request):
    return render(request, 'bookstore/orderHistory.html')

def shipping(request):
    orig_user = deepcopy(request.user)

    order = Order.objects.filter(user=request.user, status="Incomplete")
    if len(order) == 0:
        books = CartItem.objects.filter(user=request.user)
        total_cost = 0
        for book in books:
            total_cost += int(book.quantity)*float(book.book.cost)  

        promotion = Promotion(code="SYSTEM",
                              percentage=0,
                              start_date=datetime.date.today(),
                              end_date=datetime.date.today(),)
        promotion.save()

        order = Order.objects.create_order(
            user=request.user,
            total=total_cost,
            promotion=promotion,
            date=datetime.date.today(),
            time=datetime.datetime.now().strftime("%H:%M:%S"),
            first_name="",
            last_name="",
            phone="",
            street="",
            city="",
            state="",
            zip_code="",
            county="",
            country="",
            card_name="",
            card_num="",
            card_exp="",
            card_cvv="",
            card_four="",
        )
        order.save()

    def get_context():
        order = Order.objects.filter(user=request.user, status="Incomplete")[0]
        books = CartItem.objects.filter(user=request.user)
        prices = []
        for book in books:
            price = int(book.quantity)*float(book.book.cost)
            price = f"{price:.2f}"
            prices.append(price)
        
        total_cost = f"{order.total:.2f}"
        discount = int(order.promotion.percentage)*int(order.total)
        discount = f"{discount:.2f}"

        context = {
            'cartCount': getCartCount(request),
            'books_in_cart': zip(books, prices),
            'total_cost': total_cost,
            'promo_code_name': order.promotion.code,
            'promo_code_discount': discount,
        }
        return context
    context = get_context()

    if request.method == "POST":
        if request.POST.get("search_button"):
            return search_function(request, request.POST["search"])

        if request.POST.get("promo_button"):
            if request.POST["promo_code"] == "":
                context['promo_none_flag'] = True
                return render(request, 'bookstore/shipping.html', context)

            promo = Promotion.objects.filter(code=request.POST['promo_code'])
            if len(promo) == 0:
                context['promo_invalid_flag'] = True
                return render(request, 'bookstore/shipping.html', context)

            completed_orders = Order.objects.filter(user=request.user, status="Confirmed")
            orderItems = []
            for c_orders in completed_orders:
                orderItems.append(OrderItem.objects.filter(order=c_orders)[0])
            for orderItem in orderItems:
                used_promo = orderItem.order.promotion.code
                if used_promo == request.POST['promo_code']:
                    context['promo_flag'] = True
                    return render(request, 'bookstore/shipping.html', context)

            if promo.start_date > datetime.date.today():
                context['promo_start_flag'] = True
                return render(request, 'bookstore/shipping.html', context)
            if promo.end_date < datetime.date.today():
                context['promo_end_flag'] = True
                return render(request, 'bookstore/shipping.html', context)
            

        # if can_apply_promo:
        #     try:
        #         order = Order.objects.get(user=request.user)
        #     except:
        #         total = get_context()['total_cost']
        #         total = total * (100 - int(Promotion.objects.get(code=request.POST['promo_code']).percentage))
        #         order = Order.objects.create_order(
        #             user=request.user,
        #             total=total,
        #             date=datetime.date.today(),
        #             time=datetime.datetime.now().strftime("%H:%M:%S"),
        #             first_name="",
        #             last_name="",
        #             phone="",
        #             street="",
        #             city="",
        #             state="",
        #             zip_code="",
        #             county="",
        #             country="",
        #             card_name="",
        #             card_num="",
        #             card_exp="",
        #             card_cvv="",
        #             card_four="",
        #         )
            
        #         order.total = total
        #         order.save()

        #     context = get_context()
        #     return render(request, 'bookstore/shipping.html', context)
        # else:
        #     # try:
        #     #     order = Order.objects.get(user=request.user)
        #     #     order.delete()
        #     # except:
        #     #     pass
            
        #     # first_name = request.POST['userFirst_name']
        #     # last_name = request.POST['userLast_name']
        #     # phone = request.POST['userPhone']
        #     # street = request.POST['userStreet']
        #     # city = request.POST['userCity']
        #     # state = request.POST['userState']
        #     # county = request.POST['userCounty']
        #     # country = request.POST['userCountry']
        #     # zip_code = request.POST['userZip']

        #     # if "save_address" in request.POST.getlist("checks[]"):
        #     #     user = request.user
        #     #     user.first_name = first_name
        #     #     user.last_name = last_name
        #     #     user.phone = phone
        #     #     user.street = street
        #     #     user.city = city
        #     #     user.state = state
        #     #     user.county = county
        #     #     user.country = country
        #     #     user.zip_code = zip_code
        #     #     user.save()

        #     # order = Order.objects.create_order(
        #     #     user=request.user,
        #     #     total=total,
        #     #     date=datetime.date.today(),
        #     #     time=datetime.datetime.now().strftime("%H:%M:%S"),
        #     #     first_name=first_name,
        #     #     last_name=last_name,
        #     #     phone=phone,
        #     #     street=street,
        #     #     city=city,
        #     #     state=state,
        #     #     zip_code=zip_code,
        #     #     county=county,
        #     #     country=country,
        #     #     card_name="",
        #     #     card_num="",
        #     #     card_exp="",
        #     #     card_cvv="",
        #     #     card_four="",
        #     # )
        #     # order.save()

        #     context = get_context()
        #     return render(request, 'bookstore/payment.html', context)
        pass
    else:
        return render(request, 'bookstore/shipping.html', context)

def payment(request):
    return render(request, 'bookstore/payment.html')