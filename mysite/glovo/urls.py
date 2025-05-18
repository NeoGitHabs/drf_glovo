from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileViewSet, CategoryViewSet, StoreListAPIView, ContactViewSet, ProductViewSet, ComboViewSet, CartViewSet,
                    OrderViewSet, CourierViewSet, StoreReviewViewSet, CourierRatingViewSet)


router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet, basename = 'users'),
router.register(r'category', CategoryViewSet, basename = 'categories'),
router.register(r'contact', ContactViewSet, basename = 'contacts'),
router.register(r'product', ProductViewSet, basename = 'products'),
router.register(r'combo', ComboViewSet, basename = 'combo'),
router.register(r'cart', CartViewSet, basename = 'carts'),
router.register(r'order', OrderViewSet, basename = 'orders'),
router.register(r'couriers', CourierViewSet, basename = 'couriers'),
router.register(r'store_review', StoreReviewViewSet, basename = 'store_reviews'),
router.register(r'courier_rating', CourierRatingViewSet, basename = 'couriers_ratings'),

urlpatterns = [
    path('', include(router.urls)),
    path('store/', StoreListAPIView.as_view(), name = 'stores'),
    # path('<int:pk>/', StoreDetailAPIView.as_view(), name = 'store_details'),
]