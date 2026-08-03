from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):

    name = models.CharField(max_length=150)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    stock = models.PositiveIntegerField(default=0)

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    createdAt = models.DateTimeField(auto_now_add=True)

    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-createdAt"]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    @property
    def isNew(self):
        return self.createdAt >= timezone.now() - timedelta(days=7)

    def __str__(self):
        return self.name

class Cart(models.Model):

    class Status(models.TextChoices):

        ACTIVE = "ACTIVE", "Active"

        CHECKED_OUT = "CHECKED_OUT", "Checked Out"

        ABANDONED = "ABANDONED", "Abandoned"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    createdAt = models.DateTimeField(auto_now_add=True)

    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-createdAt"]

    @property
    def itemCount(self):

        return sum(

            item.quantity

            for item in self.items.all()

        )

    @property
    def total(self):

        return sum(

            item.subtotal

            for item in self.items.all()

        )

    def __str__(self):

        return f"{self.user.username} ({self.status})"


class CartItem(models.Model):

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:

        constraints = [

            models.UniqueConstraint(

                fields=["cart", "product"],

                name="unique_product_per_cart"

            )

        ]

    @property
    def subtotal(self):

        return self.product.price * self.quantity

    def __str__(self):

        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):

    class Status(models.TextChoices):

        PENDING = "PENDING", "Pending"

        PAID = "PAID", "Paid"

        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    createdAt = models.DateTimeField(auto_now_add=True)

    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-createdAt"]

    def __str__(self):

        return f"Order #{self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    createdAt = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):

        return self.price * self.quantity

    def __str__(self):

        if self.product:

            return self.product.name

        return "Deleted Product"