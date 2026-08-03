from django.urls import path

from . import views


urlpatterns = [

    # ==========================
    # Products
    # ==========================

    path(
        "",
        views.productList,
        name="product_list"
    ),

    path(
        "products/<slug:slug>/",
        views.productDetail,
        name="product_detail"
    ),


    # ==========================
    # Authentication
    # ==========================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "login/",
        views.loginUser,
        name="login"
    ),

    path(
        "logout/",
        views.logoutUser,
        name="logout"
    ),


    # ==========================
    # Cart
    # ==========================

    path(
        "cart/",
        views.showCart,
        name="show_cart"
    ),

    path(
        "cart/add/<int:productId>/",
        views.addToCart,
        name="add_to_cart"
    ),

    path(
        "cart/remove/<int:itemId>/",
        views.removeFromCart,
        name="remove_from_cart"
    ),

    path(
        "cart/increase/<int:itemId>/",
        views.increaseQuantity,
        name="increase_quantity"
    ),

    path(
        "cart/decrease/<int:itemId>/",
        views.decreaseQuantity,
        name="decrease_quantity"
    ),


    # ==========================
    # Checkout
    # ==========================

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "orders/",
        views.orderList,
        name="orders"
    ),


    # ==========================
    # Account & Pages
    # ==========================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "newsletter/subscribe/",
        views.newsletterSignup,
        name="newsletter_signup"
    ),

]