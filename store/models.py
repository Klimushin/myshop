from django.db import models
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator


# Create your models here.


class ProductBrand(models.Model):
    brand = models.CharField(max_length=20)

    def __repr__(self):
        return f"<ProductBrand [{self.pk}] ('{self}')>"

    def __str__(self):
        return self.brand

    @property
    def name(self):
        return self.brand


class Product(models.Model):
    slug = models.SlugField(
        max_length=128,
        help_text=_('128 characters or fewer.'
                    'Letters, numbers, hyphens and underscores.'),
    )
    product = models.CharField(
        max_length=128,
        verbose_name=_('a product title'),
        help_text=_('128 character or fewer'),
    )
    image = models.ImageField(
        upload_to="static/images",
        default="default/product.png",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('a single product price'),
        help_text=_('a positive number or zero'),
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text=_('a positive integer'),
        default=1,
    )
    description = models.TextField(
        verbose_name=_('product details')
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.PROTECT,
        verbose_name=_('product brand')
    )

    def __repr__(self):
        return f"<Product [{self.pk}] ('{self}')>"

    def __str__(self):
        return self.product

    @property
    def name(self):
        """An alias to a product field"""

        return self.product

    def get_absolute_url(self):
        """Return an absolute URL to a product instance"""

        return reverse_lazy("store:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """Override save method"""

        if not self.slug:
            self.slug = slugify(self.product)

        super(Product, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def get_total(self):
        total = 0.0
        for cart_item in self.cart_items.all():
            total = total + cart_item.get.total()
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')

    def get_total(self):
        return self.product.price * self.quantity


class Purchase(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
