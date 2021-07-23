from bookstore.models import *
import datetime
user = User.objects.filter(email="kushajreal@gmail.com")[0]
book = Book.objects.filter(title="Invisible Man")[0]
book.stock = 2
book.save()

promo = Promotion(code="TEST1", percentage=10, start_date=datetime.date.today(), end_date=datetime.date.today())
promo.save()
promo = Promotion(code="TEST2", percentage=12, start_date=datetime.date.today(), end_date=datetime.date.today())
promo.save()
promo = Promotion(code="TEST3", percentage=10, start_date=datetime.date.today()+datetime.timedelta(days=2), end_date=datetime.date.today())
promo.save()
promo = Promotion(code="TEST4", percentage=10, start_date=datetime.date.today()-datetime.timedelta(days=3), end_date=datetime.date.today()-datetime.timedelta(days=1))
promo = Promotion(code="GEN42069", percentage=10, start_date=datetime.date.today()-datetime.timedelta(days=3), end_date=datetime.date.today()+datetime.timedelta(days=10))
promo.save()

for o in Order.objects.all(): o.delete()
order = Order.objects.create_order(
    status="Confirmed",
    user=user,
    total=100,
    promotion=Promotion.objects.get(code="TEST1"),
    date=datetime.date.today(),
    time=datetime.datetime.now().strftime("%H:%M:%S"),
    first_name="Kushajveer",
    last_name="Singh",
    phone="7064619944",
    street="Your mom's house",
    city="hub",
    state="XX",
    zip_code="42069",
    county="Cry",
    country="Pleasure",
    card_name="Kushajveer Singh",
    card_num="1234567890123456",
    card_exp="10/12",
    card_cvv="123",
    card_four="3456"
)
order.save()
order = Order.objects.create_order(
    status="Confirmed",
    user=user,
    total=100,
    promotion=Promotion.objects.get(code="TEST2"),
    date=datetime.date.today(),
    time=datetime.datetime.now().strftime("%H:%M:%S"),
    first_name="Kushajveer",
    last_name="Singh",
    phone="7064619944",
    street="Your mom's house",
    city="hub",
    state="XX",
    zip_code="42069",
    county="Cry",
    country="Pleasure",
    card_name="Kushajveer Singh",
    card_num="1234567890123456",
    card_exp="10/12",
    card_cvv="123",
    card_four="3456"
)
order.save()
for o in OrderItem.objects.all(): o.delete()
orderItem = OrderItem.objects.add_order_item(order=Order.objects.all()[0],
                                             book=book,
                                             quantity=2)
orderItem.save()
orderItem = OrderItem.objects.add_order_item(order=Order.objects.all()[1],
                                             book=book,
                                             quantity=2)