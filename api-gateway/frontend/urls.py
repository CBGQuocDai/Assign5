from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home, name='home'),
    path('search/', views.book_search, name='book_search'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    # Customer auth
    path('login/', views.customer_login, name='customer_login'),
    path('register/', views.customer_register, name='customer_register'),
    path('logout/', views.customer_logout, name='customer_logout'),

    # Customer pages
    path('customer/', views.customer_home, name='customer_home'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('review/<int:book_id>/', views.submit_review, name='submit_review'),

    # Staff auth
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/logout/', views.staff_logout, name='staff_logout'),

    # Staff pages
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/books/', views.staff_books, name='staff_books'),
    path('staff/books/add/', views.staff_book_add, name='staff_book_add'),
    path('staff/books/<int:book_id>/edit/', views.staff_book_edit, name='staff_book_edit'),
    path('staff/books/<int:book_id>/delete/', views.staff_book_delete, name='staff_book_delete'),
    path('staff/orders/', views.staff_orders, name='staff_orders'),
    path('staff/orders/<int:order_id>/update/', views.staff_order_update, name='staff_order_update'),
    path('staff/coupons/', views.staff_coupons, name='staff_coupons'),
    path('staff/coupons/add/', views.staff_coupon_add, name='staff_coupon_add'),
]
