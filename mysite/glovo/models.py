from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)], null=True, blank=True)
    CHOICES_STATUS = (
        ('client', 'client'),
        ('owner', 'owner'),
        ('courier', 'courier'))
    status = models.CharField(max_length=32, choices=CHOICES_STATUS, default='client')
    created_account = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=50, unique=True)
    store_description = models.TextField(max_length=750)
    store_image = models.ImageField(upload_to='store_images/', blank=True, null=True)
    address = models.CharField(max_length=200)
    owner_store = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name

class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contacts')
    contact_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
    social_network = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.contact_name}, {self.phone_number}'

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_list')
    product_name = models.CharField(max_length=50)
    product_description = models.TextField()
    product_image = models.ImageField(upload_to='product_images', blank=True, null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name

class Combo(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,  related_name='combo_list')
    combo_name = models.CharField(max_length=50)
    combo_description = models.TextField(max_length=750)
    combo_image = models.ImageField(upload_to='combo_images', blank=True, null=True)
    combo_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.combo_name

class Cart(models.Model):
    cart_owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cart_owner}'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=1)

    # def __str__(self):
    #     return self.

class Order(models.Model):
    client_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_profile')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    CHOICES_ORDER_STATUS = (
    ('Ожидает обработки', 'Ожидает обработки'),
    ('В процессе доставки', 'В процессе доставки'),
    ('Доставлен', 'Доставлен'),
    ('Отменен', 'Отменен'))
    order_status = models.CharField(max_length=50, choices=CHOICES_ORDER_STATUS, default='Ожидает обработки')
    delivery_address = models.CharField(max_length=150)
    courier_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_profile')
    order_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_status

class Courier(models.Model):
    courier_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='courier_order')
    CHOICES_COURIER_STATUS = (
    ('Доступен', 'Доступен'),
    ('Занят', 'Занят'))
    courier_status = models.CharField(max_length=50, choices=CHOICES_COURIER_STATUS)

    def __str__(self):
        return f'{self.courier_profile}, {self.courier_status}'

class StoreReview(models.Model):
    client_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_review')
    review_text_store = models.TextField(max_length=750)
    stars_store = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_profile}, {self.store}'

class CourierRating(models.Model):
    client_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_profile_review')
    courier_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_profile_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.courier_profile}'
