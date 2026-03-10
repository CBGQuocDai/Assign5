from django.shortcuts import render, redirect
from django.contrib import messages
from .services import call_service


# ─── SHARED ────────────────────────────────────────────────────────
def home(request):
    books = call_service('book', '/api/books/') or []
    categories = call_service('catalog', '/api/categories/') or []
    if isinstance(books, dict):
        books = books.get('results', [])
    return render(request, 'customer/home.html', {'books': books, 'categories': categories})


# ─── CUSTOMER AUTH ─────────────────────────────────────────────────
def customer_login(request):
    if request.method == 'POST':
        result = call_service('customer', '/api/customers/login/', method='POST', data={
            'email': request.POST['email'],
            'password': request.POST['password'],
        })
        if result and result.get('status') == 'success':
            customer = result['customer']
            request.session['customer_id'] = customer['id']
            request.session['customer_name'] = customer['name']
            request.session['user_type'] = 'customer'
            return redirect('customer_home')
        messages.error(request, 'Email hoặc mật khẩu không đúng.')
    return render(request, 'customer/login.html')


def customer_register(request):
    if request.method == 'POST':
        result = call_service('customer', '/api/customers/', method='POST', data={
            'name': request.POST['name'],
            'email': request.POST['email'],
            'password': request.POST['password'],
            'phone': request.POST.get('phone', ''),
            'address': request.POST.get('address', ''),
        })
        if result and result.get('id'):
            messages.success(request, 'Đăng ký thành công! Giỏ hàng đã được tạo.')
            return redirect('customer_login')
        messages.error(request, 'Đăng ký thất bại. Email có thể đã tồn tại.')
    return render(request, 'customer/register.html')


def customer_logout(request):
    request.session.flush()
    return redirect('home')


# ─── CUSTOMER HOME & BOOKS ─────────────────────────────────────────
def customer_home(request):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    books = call_service('book', '/api/books/') or []
    categories = call_service('catalog', '/api/categories/') or []
    recommendations = call_service('recommender', f'/api/recommend/customer/{customer_id}/') or {}
    if isinstance(books, dict):
        books = books.get('results', [])
    return render(request, 'customer/home.html', {
        'books': books,
        'categories': categories,
        'recommendations': recommendations.get('recommended_books', []),
    })


def book_detail(request, book_id):
    book = call_service('book', f'/api/books/{book_id}/')
    reviews = call_service('comment_rate', f'/api/reviews/book/{book_id}/') or {}
    if not book:
        messages.error(request, 'Không tìm thấy sách.')
        return redirect('home')
    return render(request, 'customer/book_detail.html', {'book': book, 'reviews': reviews})


def book_search(request):
    q = request.GET.get('q', '')
    books = call_service('book', '/api/books/search/', params={'q': q}) or []
    return render(request, 'customer/book_list.html', {'books': books, 'query': q})


# ─── CART ──────────────────────────────────────────────────────────
def cart_view(request):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    cart = call_service('cart', f'/api/carts/customer/{customer_id}/') or {}
    # Enrich items with book details
    items = cart.get('items', [])
    enriched = []
    total = 0
    for item in items:
        book = call_service('book', f'/api/books/{item["book_id"]}/') or {}
        price = float(book.get('price', 0))
        subtotal = price * item['quantity']
        total += subtotal
        enriched.append({**item, 'book': book, 'subtotal': subtotal})
    return render(request, 'customer/cart.html', {'cart': cart, 'items': enriched, 'total': total})


def cart_add(request, book_id):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    cart = call_service('cart', f'/api/carts/customer/{customer_id}/')
    if cart and cart.get('id'):
        call_service('cart', f'/api/carts/{cart["id"]}/add_item/', method='POST', data={
            'book_id': book_id, 'quantity': int(request.POST.get('quantity', 1)),
        })
        messages.success(request, 'Đã thêm vào giỏ hàng.')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def cart_update(request, item_id):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    qty = request.POST.get('quantity', 1)
    call_service('cart', f'/api/cart-items/{item_id}/', method='PATCH', data={'quantity': int(qty)})
    return redirect('cart')


def cart_remove(request, item_id):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    call_service('cart', f'/api/cart-items/{item_id}/', method='DELETE')
    return redirect('cart')


# ─── ORDER / CHECKOUT ─────────────────────────────────────────────
def checkout(request):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    cart = call_service('cart', f'/api/carts/customer/{customer_id}/') or {}
    items = cart.get('items', [])
    enriched = []
    total = 0
    for item in items:
        book = call_service('book', f'/api/books/{item["book_id"]}/') or {}
        price = float(book.get('price', 0))
        subtotal = price * item['quantity']
        total += subtotal
        enriched.append({**item, 'book': book, 'subtotal': subtotal})
    pay_methods = call_service('pay', '/api/payment-methods/') or []
    ship_methods = call_service('ship', '/api/shipping-methods/') or []
    coupons = call_service('manager', '/api/coupons/') or []
    if isinstance(pay_methods, dict):
        pay_methods = pay_methods.get('results', [])
    if isinstance(ship_methods, dict):
        ship_methods = ship_methods.get('results', [])
    if isinstance(coupons, dict):
        coupons = coupons.get('results', [])
    return render(request, 'customer/checkout.html', {
        'items': enriched, 'total': total,
        'pay_methods': pay_methods, 'ship_methods': ship_methods, 'coupons': coupons,
    })


def place_order(request):
    if request.method != 'POST' or request.session.get('user_type') != 'customer':
        return redirect('checkout')
    customer_id = request.session['customer_id']
    cart = call_service('cart', f'/api/carts/customer/{customer_id}/') or {}
    items = cart.get('items', [])
    order_items = []
    total = 0
    for item in items:
        book = call_service('book', f'/api/books/{item["book_id"]}/') or {}
        price = float(book.get('price', 0))
        qty = item['quantity']
        subtotal = price * qty
        total += subtotal
        order_items.append({
            'book_id': item['book_id'],
            'book_title': book.get('title', ''),
            'quantity': qty,
            'unit_price': price,
            'subtotal': subtotal,
        })

    result = call_service('order', '/api/orders/', method='POST', data={
        'customer_id': customer_id,
        'total_amount': total,
        'payment_method': request.POST.get('payment_method', 'cod'),
        'shipping_method': request.POST.get('shipping_method', 'standard'),
        'shipping_address': request.POST.get('shipping_address', ''),
        'items': order_items,
    })
    if result and result.get('id'):
        # Clear cart
        if cart.get('id'):
            call_service('cart', f'/api/carts/{cart["id"]}/clear/', method='DELETE')
        messages.success(request, f'Đặt hàng thành công! Mã đơn: #{result["id"]}')
        return redirect('order_list')
    messages.error(request, 'Đặt hàng thất bại.')
    return redirect('checkout')


def order_list(request):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    orders = call_service('order', f'/api/orders/customer/{customer_id}/') or []
    return render(request, 'customer/order_list.html', {'orders': orders})


def order_detail(request, order_id):
    if request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    order = call_service('order', f'/api/orders/{order_id}/')
    payment = call_service('pay', f'/api/payments/order/{order_id}/') or {}
    shipment = call_service('ship', f'/api/shipments/order/{order_id}/') or {}
    return render(request, 'customer/order_detail.html', {
        'order': order, 'payment': payment, 'shipment': shipment,
    })


# ─── REVIEWS ──────────────────────────────────────────────────────
def submit_review(request, book_id):
    if request.method != 'POST' or request.session.get('user_type') != 'customer':
        return redirect('customer_login')
    customer_id = request.session['customer_id']
    order_id = request.POST.get('order_id')
    call_service('comment_rate', '/api/reviews/', method='POST', data={
        'customer_id': customer_id,
        'book_id': book_id,
        'order_id': order_id,
        'rating': int(request.POST.get('rating', 5)),
        'comment': request.POST.get('comment', ''),
    })
    messages.success(request, 'Đánh giá đã được gửi.')
    return redirect('book_detail', book_id=book_id)


# ─── STAFF AUTH ────────────────────────────────────────────────────
def staff_login(request):
    if request.method == 'POST':
        result = call_service('staff', '/api/staff/login/', method='POST', data={
            'email': request.POST['email'],
            'password': request.POST['password'],
        })
        if result and result.get('status') == 'success':
            staff = result['staff']
            request.session['staff_id'] = staff['id']
            request.session['staff_name'] = staff['name']
            request.session['staff_role'] = staff['role']
            request.session['user_type'] = 'staff'
            return redirect('staff_dashboard')
        messages.error(request, 'Email hoặc mật khẩu không đúng.')
    return render(request, 'staff/login.html')


def staff_logout(request):
    request.session.flush()
    return redirect('staff_login')


# ─── STAFF DASHBOARD ───────────────────────────────────────────────
def staff_dashboard(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    books = call_service('book', '/api/books/') or []
    orders = call_service('order', '/api/orders/') or []
    if isinstance(books, dict):
        books = books.get('results', [])
    if isinstance(orders, dict):
        orders = orders.get('results', [])
    stats = {
        'total_books': len(books),
        'total_orders': len(orders),
        'pending_orders': len([o for o in orders if o.get('status') == 'pending']),
    }
    return render(request, 'staff/dashboard.html', {'stats': stats, 'recent_orders': orders[:5]})


# ─── STAFF BOOK MANAGEMENT ─────────────────────────────────────────
def staff_books(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    books = call_service('book', '/api/books/') or []
    if isinstance(books, dict):
        books = books.get('results', [])
    return render(request, 'staff/book_list.html', {'books': books})


def staff_book_add(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    categories = call_service('catalog', '/api/categories/') or []
    authors = call_service('catalog', '/api/authors/') or []
    if isinstance(categories, dict):
        categories = categories.get('results', [])
    if isinstance(authors, dict):
        authors = authors.get('results', [])
    if request.method == 'POST':
        result = call_service('book', '/api/books/', method='POST', data={
            'title': request.POST['title'],
            'author_id': request.POST['author_id'],
            'category_id': request.POST['category_id'],
            'staff_id': request.session['staff_id'],
            'price': request.POST['price'],
            'stock': request.POST.get('stock', 0),
            'description': request.POST.get('description', ''),
            'isbn': request.POST.get('isbn', ''),
        })
        if result and result.get('id'):
            messages.success(request, 'Đã thêm sách mới.')
            return redirect('staff_books')
        messages.error(request, 'Thêm sách thất bại.')
    return render(request, 'staff/book_form.html', {'action': 'Thêm', 'categories': categories, 'authors': authors})


def staff_book_edit(request, book_id):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    book = call_service('book', f'/api/books/{book_id}/')
    categories = call_service('catalog', '/api/categories/') or []
    authors = call_service('catalog', '/api/authors/') or []
    if isinstance(categories, dict):
        categories = categories.get('results', [])
    if isinstance(authors, dict):
        authors = authors.get('results', [])
    if request.method == 'POST':
        call_service('book', f'/api/books/{book_id}/', method='PATCH', data={
            'title': request.POST['title'],
            'author_id': request.POST['author_id'],
            'category_id': request.POST['category_id'],
            'price': request.POST['price'],
            'stock': request.POST.get('stock', 0),
            'description': request.POST.get('description', ''),
        })
        messages.success(request, 'Đã cập nhật sách.')
        return redirect('staff_books')
    return render(request, 'staff/book_form.html', {
        'action': 'Sửa', 'book': book, 'categories': categories, 'authors': authors,
    })


def staff_book_delete(request, book_id):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    call_service('book', f'/api/books/{book_id}/', method='DELETE')
    messages.success(request, 'Đã xóa sách.')
    return redirect('staff_books')


# ─── STAFF ORDER MANAGEMENT ────────────────────────────────────────
def staff_orders(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    orders = call_service('order', '/api/orders/') or []
    if isinstance(orders, dict):
        orders = orders.get('results', [])
    return render(request, 'staff/order_list.html', {'orders': orders})


def staff_order_update(request, order_id):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    if request.method == 'POST':
        call_service('order', f'/api/orders/{order_id}/update_status/', method='PATCH', data={
            'status': request.POST.get('status'),
        })
        messages.success(request, 'Đã cập nhật trạng thái đơn hàng.')
    return redirect('staff_orders')


# ─── MANAGER (accessed via staff with supervisor role) ─────────────
def staff_coupons(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    coupons = call_service('manager', '/api/coupons/') or []
    if isinstance(coupons, dict):
        coupons = coupons.get('results', [])
    return render(request, 'staff/coupon_list.html', {'coupons': coupons})


def staff_coupon_add(request):
    if request.session.get('user_type') != 'staff':
        return redirect('staff_login')
    if request.method == 'POST':
        result = call_service('manager', '/api/coupons/', method='POST', data={
            'code': request.POST['code'],
            'discount_type': request.POST['discount_type'],
            'discount_value': request.POST['discount_value'],
            'min_order_amount': request.POST.get('min_order_amount', 0),
            'valid_from': request.POST['valid_from'],
            'valid_to': request.POST['valid_to'],
            'created_by': request.session.get('staff_id', 1),
        })
        if result and result.get('id'):
            messages.success(request, 'Đã thêm phiếu giảm giá.')
            return redirect('staff_coupons')
        messages.error(request, 'Thêm phiếu giảm giá thất bại.')
    return render(request, 'staff/coupon_form.html', {'action': 'Thêm'})
