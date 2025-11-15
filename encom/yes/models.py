from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class User(models.Model):
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=120, null=False)
    birth_date = models.DateField()

    def __str__(self):
        return f"{self.name} {self.surname}"
    
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    email = models.EmailField(unique=True, blank=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True, validators=[MinLengthValidator(9)])

    description = models.TextField(blank=True, default="hellow")
   
    def __str__(self):
        return f"{self.user.name}'s Profile"
    
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(max_length=4, null=False, validators=[MaxValueValidator(9999), MinValueValidator(1)])
    description = models.TextField(blank=True, default="$")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price}$"
    
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    item = models.ManyToManyField(Product)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.name}'s Cart"
    
class PaymentSystem(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    cardholders_name = models.CharField(max_length=20, null=False)
    card_number = models.CharField(max_length=21, null=False, validators=[MinLengthValidator(15)])
    card_expire_date = models.DateField(null=False)
    CVC = models.IntegerField(null=False, max_length=3, validators=[MaxValueValidator(999), MinValueValidator(000)])

    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.name}'s card"
    
class Rating(models.Model):
    class StarRating(models.TextChoices):
            ONE = '1', '⭐ (1 Star)'
            TWO = '2', '⭐⭐ (2 Stars)'
            THREE = '3', '⭐⭐⭐ (3 Stars)'
            FOUR = '4', '⭐⭐⭐⭐ (4 Stars)'
            FIVE = '5', '⭐⭐⭐⭐⭐ (5 Stars)'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="rateitem")
    
    stars = models.CharField(max_length=1, choices=StarRating.choices, default=StarRating.FIVE)

    comment = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.name} {self.user.surname} rated product - {self.product.name} [{self.get_stars_display()}]"

    
class ProductHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_additions') 
    
    action = models.CharField(max_length=20, default='added') 
    added_at = models.DateTimeField(auto_now_add=True)  
    
    
    class Meta:
        ordering = ['-added_at'] 
        verbose_name = 'Product History'
        verbose_name_plural = 'Product Histories'
    
    def __str__(self):
        return f"{self.product.name} {self.action} by {self.user.name} {self.user.surname} on {self.added_at.strftime('%Y-%m-%d %H:%M')}"


    
