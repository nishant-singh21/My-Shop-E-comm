from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction

from .models import Category, Product, Order, OrderItem
from .cart import Cart


def product_list(request, category_slug=None):
    """
    Category-based product filtering.
    /                     -> all active products
    /category/<slug>/     -> products in one category
    """
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related("category")

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    return render(request, "shop/product_list.html", {
        "category": category,
        "categories": categories,
        "products": products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_detail(request):
    cart = Cart(request)
    return render(request, "shop/cart_detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(product=product, quantity=quantity)
    return redirect("cart_detail")


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required
@transaction.atomic
def checkout(request):
    """
    Converts the session cart into a persisted Order + OrderItems,
    decrements stock, and clears the cart. Wrapped in a transaction
    so a failure mid-checkout can't leave stock/orders inconsistent.
    """
    cart = Cart(request)
    if len(cart) == 0:
        return redirect("cart_detail")

    if request.method == "POST":
        address = request.POST.get("shipping_address", "")
        order = Order.objects.create(user=request.user, shipping_address=address)

        for item in cart:
            product = item["product"]
            if product.stock < item["quantity"]:
                order.delete()
                return render(request, "shop/cart_detail.html", {
                    "cart": cart,
                    "error": f"Not enough stock for {product.name}",
                })

            OrderItem.objects.create(
                order=order,
                product=product,
                price=item["price"],
                quantity=item["quantity"],
            )
            product.stock -= item["quantity"]
            product.save(update_fields=["stock"])

        order.recalculate_total()
        cart.clear()
        return redirect("order_tracking", order_id=order.id)

    return render(request, "shop/checkout.html", {"cart": cart})


@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "shop/order_tracking.html", {"order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "shop/order_history.html", {"orders": orders})
