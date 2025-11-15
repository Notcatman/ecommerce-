from django.contrib import admin
from .models import User, Profile, Product, Cart, PaymentSystem, ProductHistory, Rating

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(PaymentSystem)
admin.site.register(ProductHistory)
admin.site.register(Rating)
