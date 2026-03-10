from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author_id = models.IntegerField()        # ref catalog-service
    category_id = models.IntegerField()      # ref catalog-service
    staff_id = models.IntegerField()         # ref staff-service
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    isbn = models.CharField(max_length=20, unique=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'book'
