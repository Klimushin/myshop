from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, RedirectView, CreateView, UpdateView, DeleteView

from store.mixins import StaffRequiredMixin
from store.models import Product, Cart, CartItem


# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"


class AddProductToCartView(RedirectView):
    def get(self, *args, **kwargs):
        cart = self.request.session.get('cart', {})
        product_slug = self.kwargs.get('slug')
        if product_slug in cart:
            cart[product_slug] += 1
        else:
            cart[product_slug] = 1
        self.request.session['cart'] = cart
        redirect_url = self.request.headers.get('referer') or reverse_lazy('store:list')
        return HttpResponseRedirect(redirect_url)


class PurchaseView(View):
    def get(self, request, *args, **kwargs):
        session_cart = request.session.get('cart')
        if session_cart is None:
            redirect_url = self.request.headers.get('referer') or reverse_lazy('store:list')
            return HttpResponseRedirect(redirect_url)

        user = self.request.user
        cart = Cart.objects.get_or_create(user=user, is_active=True)

        for product_slug in session_cart:
            product = Product.objects.get(slug=product_slug)
            quantity = session_cart[product_slug]
            cart_item = CartItem(product=product, quantity=quantity, cart=cart)
            cart_item.save()
        self.request.session['cart'] = {}
        redirect_url = self.request.headers.get('referer') or reverse_lazy('store:list')
        return HttpResponseRedirect(redirect_url)


class ProductCreateView(StaffRequiredMixin, CreateView):
    """Product create view implementation"""

    # http_method_names = ["get", "post", "head", "options", "trace"]
    model = Product
    fields = [
        "brand",
        # "image",
        "product",
        "description",
        "price",
        "quantity",
    ]


class ProductUpdateView(StaffRequiredMixin, UpdateView):
    """Product update view implementation"""

    # http_method_names = ["get", "post", "head", "options", "trace"]
    model = Product
    fields = [
        "brand",
        # "image",
        "product",
        "description",
        "price",
        "quantity",
    ]


class ProductDeleteView(StaffRequiredMixin, DeleteView):
    """Product delete view implementation"""

    http_method_names = ["get", "post", "head", "options", "trace"]
    model = Product
    success_url = reverse_lazy("store:list")
