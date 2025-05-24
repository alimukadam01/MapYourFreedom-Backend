from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Payment(models.Model): 
    user = models.ForeignKey(User, models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=256, null=True, blank=True)
    session_id = models.CharField(max_length=512, null=True, blank=True)
    payment_intent_id = models.CharField(max_length=512, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    payment_status = models.CharField(max_length=256, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    session_created_at = models.DateTimeField(null=True, blank=True)

