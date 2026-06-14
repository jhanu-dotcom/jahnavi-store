from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Wishlist
from .models import Review

def home(request):

    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    products = Product.objects.all()

    if query:
        products = products.filter(
            name__icontains=query
        )

    if category:
        products = products.filter(
            category=category
        )

    return render(
        request,
        'home.html',
        {
            'products': products
        }
    )
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if request.user.is_authenticated:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=rating,
                comment=comment
            )

            return redirect('product_detail', id=id)

    reviews = Review.objects.filter(product=product)

    return render(request, 'product.html', {
        'product': product,
        'reviews': reviews
    })
def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    key = str(id)
    cart[key] = cart.get(key, 0) + 1

    request.session['cart'] = cart

    return redirect('cart')

from decimal import Decimal

def cart(request):
    cart = request.session.get('cart', {})

    # Fix old cart data stored as a list
    if isinstance(cart, list):
        new_cart = {}

        for pid in cart:
            pid = str(pid)
            new_cart[pid] = new_cart.get(pid, 0) + 1

        cart = new_cart
        request.session['cart'] = cart

    product_ids = [int(pk) for pk in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    items = []
    total = Decimal('0.00')

    for p in products:
        qty = cart.get(str(p.id), 0)
        subtotal = p.price * qty

        items.append({
            'product': p,
            'quantity': qty,
            'subtotal': subtotal
        })

        total += subtotal

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
def register(request):

    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')

    return render(request, 'register.html', {
        'form': form
    })
def user_logout(request):
    logout(request)
    return redirect('/')
@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    product_ids = [int(pk) for pk in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    total = Decimal('0.00')

    for p in products:
        qty = cart.get(str(p.id), 0)
        total += p.price * qty

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for p in products:
        qty = cart.get(str(p.id), 0)
        if qty <= 0:
            continue
        OrderItem.objects.create(
            order=order,
            product=p,
            quantity=qty,
            price=p.price
        )

    request.session['cart'] = {}

    return render(request, 'success.html', {'order': order})
from django.contrib.auth.decorators import login_required

@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(
        request,
        'orders.html',
        {
            'orders': orders
        }
    )
def increase_quantity(request, id):
    cart = request.session.get('cart', {})

    key = str(id)

    if key in cart:
        cart[key] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})

    key = str(id)

    if key in cart:
        cart[key] -= 1

        if cart[key] <= 0:
            del cart[key]

    request.session['cart'] = cart

    return redirect('cart')

@login_required
def add_to_wishlist(request, id):
     product = Product.objects.get(id=id)
     Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
     return redirect('wishlist')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'items': items
        }
    )
@login_required
def remove_from_wishlist(request, id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=id
    ).delete()

    return redirect('wishlist')