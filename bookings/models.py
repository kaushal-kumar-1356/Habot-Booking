from django.db import models

# Create your models here.

class Parent(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class LSA_Profile(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    skills = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Booking_Request(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    lsa = models.ForeignKey(LSA_Profile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, default="PENDING")

    def __str__(self):
        return f"{self.parent} - {self.lsa}"


class Payment(models.Model):
    booking = models.OneToOneField(Booking_Request, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Pyment - Booking {self.booking.id}"