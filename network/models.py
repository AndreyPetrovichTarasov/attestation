from django.db import models


class NetworkNode(models.Model):
    name = models.CharField(max_length=255)

    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=20)

    supplier = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='clients')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def level(self):
        """Вычисляет уровень иерархии"""
        level = 0
        supplier = self.supplier
        while supplier:
            level += 1
            supplier = supplier.supplier
        return level


class Product(models.Model):
    node = models.ForeignKey(NetworkNode, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.model})'
