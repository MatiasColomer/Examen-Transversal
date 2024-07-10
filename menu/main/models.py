from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='product_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    direccion = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    purchase_data = models.JSONField()

    def __str__(self):
        return f'Compra de {self.nombre}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_price = sum(item.product.price * item.quantity for item in self.items.all())
        self.total_price = total_price
        super().save(*args, **kwargs)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} de {self.product.name}'
