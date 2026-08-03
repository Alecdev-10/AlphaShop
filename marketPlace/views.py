from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem
)

from django.contrib import messages

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .forms import (
    RegisterForm,
    ProfileForm,
    ContactForm,
    NewsletterForm
)

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction


PRODUCTS_PER_PAGE = 8


def productList(request):

    products = Product.objects.all()

    query = request.GET.get("q", "").strip()

    if query:

        products = products.filter(

            Q(name__icontains=query) |
            Q(description__icontains=query)

        )

    sort = request.GET.get("sort", "newest")

    sort_map = {
        "newest": "-createdAt",
        "price_asc": "price",
        "price_desc": "-price",
        "name": "name",
    }

    products = products.order_by(sort_map.get(sort, "-createdAt"))

    paginator = Paginator(products, PRODUCTS_PER_PAGE)

    page = paginator.get_page(request.GET.get("page"))

    context = {

        "products": page,

        "page_obj": page,

        "query": query,

        "sort": sort,

        "total_count": paginator.count,

    }

    return render(

        request,

        "marketPlace/product_list.html",

        context

    )



def productDetail(request, slug):

    product = get_object_or_404(

        Product,

        slug=slug

    )

    relatedProducts = (

        Product.objects

        .exclude(id=product.id)

        .order_by("-createdAt")[:4]

    )

    context = {

        "product": product,

        "relatedProducts": relatedProducts

    }

    return render(

        request,

        "marketPlace/product_detail.html",

        context

    )


def register(request):

    if request.user.is_authenticated:

        return redirect("product_list")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(

                request,

                "Account created successfully."

            )

            return redirect("product_list")

    else:

        form = RegisterForm()

    return render(

        request,

        "marketPlace/register.html",

        {

            "form": form

        }

    )




def loginUser(request):

    if request.user.is_authenticated:

        return redirect("product_list")

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user:

            login(request, user)

            messages.success(

                request,

                "Welcome back."

            )

            return redirect("product_list")

        messages.error(

            request,

            "Invalid username or password."

        )

    return render(

        request,

        "marketPlace/login.html"

    )



@login_required
def logoutUser(request):

    logout(request)

    messages.success(

        request,

        "Logged out successfully."

    )

    return redirect("login")


@login_required
def showCart(request):

    cart = Cart.objects.filter(

        user=request.user,

        status=Cart.Status.ACTIVE

    ).first()

    recommended = (
        Product.objects
        .filter(stock__gt=0)
        .order_by("-createdAt")[:4]
    )

    return render(

        request,

        "marketPlace/cart.html",

        {

            "cart": cart,

            "recommended": recommended

        }

    )



@login_required
def addToCart(request, productId):

    product = get_object_or_404(

        Product,

        id=productId

    )

    try:
        requestedQuantity = int(request.POST.get("quantity") or request.GET.get("quantity") or 1)
    except ValueError:
        requestedQuantity = 1

    requestedQuantity = max(1, requestedQuantity)

    if product.stock <= 0:

        messages.error(

            request,

            "This product is out of stock."

        )

        return redirect(

            "product_detail",

            slug=product.slug

        )

    cart, _ = Cart.objects.get_or_create(

        user=request.user,

        status=Cart.Status.ACTIVE

    )

    item = CartItem.objects.filter(

        cart=cart,

        product=product

    ).first()

    if item:

        newQuantity = item.quantity + requestedQuantity

        if newQuantity <= product.stock:

            item.quantity = newQuantity

            item.save()

            messages.success(
                request,
                "Product quantity updated."
            )

        else:

            messages.warning(
                request,
                "You have reached the maximum available stock."
            )

    else:

        CartItem.objects.create(

            cart=cart,

            product=product,

            quantity=min(requestedQuantity, product.stock)

        )

        messages.success(
            request,
            "Product added to cart."
        )

    return redirect("show_cart")



@login_required
def removeFromCart(request, itemId):

    item = get_object_or_404(

        CartItem,

        id=itemId,

        cart__user=request.user

    )

    item.delete()

    messages.success(

        request,

        "Product removed from cart."

    )

    return redirect(

        "show_cart"

    )



@login_required
def increaseQuantity(request, itemId):

    item = get_object_or_404(

        CartItem,

        id=itemId,

        cart__user=request.user

    )

    if item.quantity < item.product.stock:

        item.quantity += 1

        item.save()

    else:

        messages.warning(

            request,

            "No more stock available."

        )

    return redirect(

        "show_cart"

    )



@login_required
def decreaseQuantity(request, itemId):

    item = get_object_or_404(

        CartItem,

        id=itemId,

        cart__user=request.user

    )

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    else:

        item.delete()

    return redirect(

        "show_cart"

    )


@login_required
def checkout(request):

    cart = Cart.objects.filter(
        user=request.user,
        status=Cart.Status.ACTIVE
    ).first()

    if not cart or not cart.items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect("show_cart")

    if request.method == "POST":

        for item in cart.items.all():

            if item.quantity > item.product.stock:

                messages.error(
                    request,
                    f"Not enough stock for {item.product.name}."
                )

                return redirect("show_cart")

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                total=cart.total
            )

            for item in cart.items.all():

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                item.product.stock -= item.quantity
                item.product.save()

            cart.status = Cart.Status.CHECKED_OUT
            cart.save()

        messages.success(
            request,
            "Order placed successfully."
        )

        return redirect("orders")

    return render(
        request,
        "marketPlace/checkout.html",
        {
            "cart": cart
        }
    )


@login_required
def orderList(request):

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
    )

    return render(

        request,

        "marketPlace/orders.html",

        {

            "orders": orders

        }

    )


def _stylePasswordForm(form):

    for field in form.fields.values():
        field.widget.attrs.update({"class": "form-control"})

    return form


@login_required
def profile(request):

    if request.method == "POST":

        if "update_profile" in request.POST:

            profileForm = ProfileForm(request.POST, instance=request.user)
            passwordForm = _stylePasswordForm(PasswordChangeForm(request.user))

            if profileForm.is_valid():

                profileForm.save()

                messages.success(request, "Profile updated successfully.")

                return redirect("profile")

        else:

            profileForm = ProfileForm(instance=request.user)
            passwordForm = _stylePasswordForm(PasswordChangeForm(request.user, request.POST))

            if passwordForm.is_valid():

                user = passwordForm.save()

                update_session_auth_hash(request, user)

                messages.success(request, "Password changed successfully.")

                return redirect("profile")

    else:

        profileForm = ProfileForm(instance=request.user)
        passwordForm = _stylePasswordForm(PasswordChangeForm(request.user))

    ordersCount = Order.objects.filter(user=request.user).count()

    return render(

        request,

        "marketPlace/profile.html",

        {
            "profileForm": profileForm,
            "passwordForm": passwordForm,
            "ordersCount": ordersCount,
        }

    )


def about(request):

    return render(request, "marketPlace/about.html")


def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            messages.success(
                request,
                "Thanks for reaching out! We'll get back to you soon."
            )

            return redirect("contact")

    else:

        form = ContactForm()

    return render(request, "marketPlace/contact.html", {"form": form})


def newsletterSignup(request):

    if request.method == "POST":

        form = NewsletterForm(request.POST)

        if form.is_valid():

            messages.success(request, "You're subscribed to our newsletter.")

        else:

            messages.error(request, "Please enter a valid email address.")

    return redirect(request.META.get("HTTP_REFERER", "product_list"))