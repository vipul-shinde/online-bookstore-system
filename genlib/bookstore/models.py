from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django_cryptography.fields import encrypt


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True, primary_key=True)
    category = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_path = models.CharField(max_length=30)
    edition = models.IntegerField()
    publisher = models.CharField(max_length=30)
    publication_year = models.CharField(max_length=4)
    author = models.CharField(max_length=30)
    stock = models.IntegerField()
    cost = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.IntegerField(default=2)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password, 
                    receive_promotions, phone="", street="",
                    city="", state="", zip_code="", card_name="",
                    card_num="", card_exp="", card_cvv="",
                    **kwargs):
        email = self.normalize_email(email)
        user = self.model(first_name=first_name,
                          last_name=last_name,
                          email=email,
                          password=password,
                          receive_promotions=receive_promotions,
                          phone=phone,
                          street=street,
                          city=city,
                          state=state,
                          zip_code=zip_code,
                          card_name=card_name,
                          card_num=card_num,
                          card_exp=card_exp,
                          card_cvv=card_cvv,
                          **kwargs)
        user.set_password(password)
        user.save()

    def create_superuser(self, first_name, last_name, email, password, 
                         receive_promotions, phone="", street="",
                         city="", state="", zip_code="", card_name="",
                         card_num="", card_exp="", card_cvv="",
                         **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_suspended', False)

        return self.create_user(first_name=first_name, last_name=last_name, email=email, password=password, 
                                receive_promotions=receive_promotions, phone=phone, street=street,
                                city=city, state=state, zip_code=zip_code, card_name=card_name,
                                card_num=card_num, card_exp=card_exp, card_cvv=card_cvv,
                                **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, unique=True, primary_key=True)
    receive_promotions = models.BooleanField(default=False)

    phone = models.CharField(max_length=10, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)

    card_name = encrypt(models.CharField(max_length=100, null=True, blank=True))
    card_num = encrypt(models.CharField(max_length=16, null=True, blank=True))
    card_exp = encrypt(models.CharField(max_length=5, null=True, blank=True))
    card_cvv = encrypt(models.CharField(max_length=3, null=True, blank=True))

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'receive_promotions']

    def __str__(self):
        return self.email


class CartManager(models.Manager):
    def create_cart(self, user):
        cart = self.create(user=user)
        return cart


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = CartManager()

    def __str__(self):
        return str(self.id)
