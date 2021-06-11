from django.urls import path

from store.views import *

app_name = 'store'
urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('add-to-cart/<slug:slug>/', AddProductToCartView.as_view(), name='add-to-cart'),
    path('', ProductListView.as_view(), name='list'),
    path('purchase/', PurchaseView.as_view(), name='purchase'),
    path("create/", ProductCreateView.as_view(), name="create"),
    path("update/<slug:slug>/", ProductUpdateView.as_view(), name="update"),
    path("delete/<slug:slug>/", ProductDeleteView.as_view(), name="delete"),

]
