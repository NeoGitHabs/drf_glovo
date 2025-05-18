from rest_framework import serializers
from .models import (UserProfile, Category, Store, Contact, Product, Combo,
                     Cart, Order, Courier, StoreReview, CourierRating)


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'status')

class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)

class ContactSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('contact_name', 'phone_number', 'social_network')

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_name', 'product_image', 'product_description', 'product_price')

class ComboSerializers(serializers.ModelSerializer):
    class Meta:
        model = Combo
        fields = ('combo_name', 'combo_image', 'combo_description', 'combo_price')

class UserNickMameForReview(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username',)

class StoreReviewSerializers(serializers.ModelSerializer):
    client_profile = UserNickMameForReview()
    created_date = serializers.DateTimeField(format('%d-%m-%y %H-%M'))
    class Meta:
        model = StoreReview
        fields = ('client_profile', 'review_text_store', 'stars_store', 'created_date')

class StoreSerializers(serializers.ModelSerializer):
    owner_store = UserProfileSerializers()
    category = CategorySerializers()
    contacts = ContactSerializers(many=True, read_only=True)
    product_list = ProductSerializers(many=True, read_only=True)
    combo_list = ComboSerializers(many=True, read_only=True)
    store_review = StoreReviewSerializers(many=True, read_only=True)
    class Meta:
        model = Store
        fields = ('store_name', 'store_image', 'category', 'store_description', 'address',
                  'contacts', 'owner_store', 'product_list', 'combo_list', 'store_review')

class CartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('cart_owner',)

class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_status', 'delivery_address', 'courier_profile', 'order_time')

class CourierSerializers(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = ('courier_status',)

class CourierRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourierRating
        fields = ('rating', 'created_date')
