from django.db import models
from django.contrib.auth import get_user_model


USER = get_user_model()


class Plan(models.Model):
    price = models.FloatField()
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name.title()} (${self.price})'


class Subscription(models.Model):
    active = models.BooleanField()
    plan = models.ForeignKey(Plan, related_name='subscriptions', on_delete=models.CASCADE)
    active_date = models.DateField(auto_now_add=True)
    last_update_date = models.DateField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return f'{self.apps.all()[0].name} -subscription {self.plan}'


class App(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    subscription = models.ForeignKey(Subscription, related_name='apps', on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='apps')

    def __str__(self):
        return self.name

