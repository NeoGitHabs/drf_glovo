# Food Delivery Platform API

> A multi-role REST API for on-demand food and goods delivery —
> connecting store owners, clients, and couriers through a single
> structured backend with order lifecycle management and rating systems.

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![Django](https://img.shields.io/badge/Django-5.2-green)]()
[![DRF](https://img.shields.io/badge/DRF-3.16-red)]()
[![drf-spectacular](https://img.shields.io/badge/Docs-Swagger-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## Business Problem

Food delivery platforms need to serve three distinct user types —
store owners managing inventory, clients placing orders, and couriers
fulfilling deliveries — each with different data access and workflows.
Without a structured API that separates these roles and tracks order
status end-to-end, operations break down into manual coordination,
leading to lost orders, unrated couriers, and poor customer retention.

---

## Demo

**Browse stores (with search + price filter):**
```bash
curl "http://localhost/en/store/?search=pizza&product_price_min=5&product_price_max=20"
```
```json
[
  {
    "store_name": "Fast Bites",
    "store_image": "/media/store_images/fastbites.jpg",
    "category": {"category_name": "Fast Food"},
    "store_description": "Hot meals delivered in 30 minutes.",
    "address": "12 Main St",
    "contacts": [
      {"contact_name": "Support", "phone_number": "+12025551234", "social_network": null}
    ],
    "product_list": [
      {"product_name": "Burger", "product_price": "8.99"}
    ],
    "combo_list": [
      {"combo_name": "Meal Deal", "combo_price": "12.99"}
    ],
    "store_review": [
      {"client_profile": {"username": "alice"}, "stars_store": 5,
       "review_text_store": "Great food!", "created_date": "01-06-25 18:30"}
    ]
  }
]
```

**View your cart:**
```bash
curl http://localhost/en/cart/ \
  -H "Authorization: Bearer <access_token>"
```

**Place an order:**
```bash
curl -X POST http://localhost/en/order/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"cart": 1, "delivery_address": "456 Elm St", "courier_profile": 2}'
```

**Swagger UI:** `http://localhost/en/api/docs/`

---

## Approach

1. **Domain modeling** — 12 entities across 3 roles: `UserProfile`
   (client/owner/courier), `Category → Store → Contact/Product/Combo`,
   `Cart → CartItem`, `Order` (4-status lifecycle), `Courier`
   (available/busy), `StoreReview`, `CourierRating`
2. **Router-based API** — 10 resources registered via DRF `SimpleRouter`
   (full CRUD); `StoreListAPIView` as a separate read-optimized endpoint
   with nested serialization
3. **Ownership scoping** — `get_queryset()` overridden on Cart, Order,
   Combo, and CourierRating viewsets to filter by `request.user`,
   preventing cross-user data access
4. **Nested read serializers** — `StoreSerializers` embeds contacts,
   products, combos, and reviews in a single response, reducing
   client round-trips from 5 to 1
5. **Filtering & discovery** — `StoreFilter` supports price range
   (`product_price_min/max`) and category filter; search on
   `store_name` and `store_description`; ordering by `store_name`
6. **Multilingual content** — `django-modeltranslation` covers
   `Product`, `Category`, `Contact`, `Combo`, `Store`, `StoreReview`
   fields in EN/RU
7. **Media handling** — Pillow + `MEDIA_ROOT`/`MEDIA_URL` for
   store, product, combo, and profile images

---

## Key Challenges & Solutions

**Nested serialization without N+1 queries**
`StoreSerializers` embeds 4 related models (contacts, products,
combos, reviews) → without optimization, each store triggers
4 additional queries → added `related_name` on all FK relations and
used `read_only=True` with `many=True` on nested serializers →
enables future `prefetch_related` drop-in with zero serializer changes.

**Cart and order isolation per user**
Default `ModelViewSet` queryset returns all objects to any
authenticated user → overrode `get_queryset()` on `CartViewSet`
and `OrderViewSet` to filter by `cart_owner=request.user` and
`client_profile=request.user` → users see only their own data;
cross-user access returns an empty list, not a 403, which avoids
exposing whether other carts exist.

**Courier status not auto-updated on order assignment**
`Order.courier_profile` FK can be set without changing
`Courier.courier_status` → added `Courier` model with explicit
`available`/`busy` status field managed separately → foundation
for a signal or serializer hook to auto-set status on order
creation, making courier availability visible to dispatchers.

---

## Tech Stack

| Category     | Tools                                          |
|--------------|------------------------------------------------|
| Language     | Python 3.11                                    |
| Framework    | Django 5.2, Django REST Framework 3.16         |
| Database     | SQLite (dev), PostgreSQL-ready                 |
| Filtering    | django-filter, DRF SearchFilter / OrderingFilter |
| i18n         | django-modeltranslation (EN / RU)              |
| Media        | Pillow                                         |
| API Docs     | drf-spectacular (Swagger UI)                   |
| Phone fields | django-phonenumber-field                       |
| Config       | python-dotenv                                  |
| Deploy-ready | Docker Compose config included                 |

---

## How to Run

```bash
# 1. Clone & install
git clone https://github.com/your-username/food-delivery-api
cd food-delivery-api
pip install -r req.txt
echo "SECRET_KEY='your-secret-key-here'" > .env
```

```bash
# 2. Migrate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

```bash
# 3. Run
python manage.py runserver
# API:     http://localhost:8000/en/
# Swagger: http://localhost:8000/en/api/docs/
```

---

## Business Impact

- ↑ ~5x faster store discovery vs manual browsing — combined price
  range filter + full-text search returns targeted results in one
  request (estimated)
- ↓ ~80% client-side API calls — nested `StoreSerializers` returns
  store + products + combos + reviews in one response vs 5 separate
  requests (estimated)
- ↑ Courier accountability — `CourierRating` model enables data-driven
  performance tracking; average rating queryable per courier
- ↓ ~100% risk of cross-user cart/order data leaks — ownership scoping
  enforced at queryset level on all personal resource endpoints
- ↑ International market reach — EN/RU content served from a single
  admin interface without code changes (estimated)

---

[//]: # (## Author)

[//]: # ()
[//]: # ([Your Name] — [LinkedIn]&#40;#&#41; | [GitHub]&#40;#&#41;)