from django.db import models
from account.models import User

from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'."
)


class ShopSector(models.Model):
    name = models.CharField(max_length=100, unique=True)  
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200) 
    owner = models.CharField(max_length=100)  
    sector = models.ForeignKey(ShopSector, on_delete=models.CASCADE)  
    address = models.TextField() 
    contact_number = models.CharField(
    max_length=10,
    validators=[phone_validator],
    blank=True,
    null=True
) 
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Bill(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE) 
    customer_name = models.CharField(max_length=200)  
    customer_number = models.CharField(max_length=15, blank=True, null=True) 
    description = models.TextField(blank=True, null=True) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    def update_total(self):
       
        self.total_amount = sum(item.total_price for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Bill #{self.id} - {self.shop.name}"

class BillItem(models.Model):
    UNIT_CHOICES = [
        ("kg", "Kilogram"),
        ("gm", "Gram"),
        ("piece", "Piece"),
        ("packet", "Packet"),
        ("set", "set"),
    ]

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name="items")  
    product_name = models.CharField(max_length=200) 
    quantity = models.PositiveIntegerField() 
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, blank=True, default='') 
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
  
    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product_name} - {self.quantity} {self.unit if self.unit else ''}"



