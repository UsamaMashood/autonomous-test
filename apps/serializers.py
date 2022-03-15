from rest_framework import serializers
from django.urls import reverse

from .models import (
    App, Subscription, Plan
)


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True, many=False)

    class Meta:
        model = Subscription
        fields = '__all__'


class AppSerializer(serializers.HyperlinkedModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    user = serializers.SerializerMethodField('get_user_name')
    subscription_detail = serializers.SerializerMethodField('get_subscription_detail')
    subscription_cancel = serializers.SerializerMethodField('get_subscription_cancel')
    subscription_update = serializers.SerializerMethodField('get_subscription_update')

    class Meta:
        model = App

        fields = ['id', 'name', 'description', 'url',
                  'subscription_detail', 'subscription_cancel',
                  'subscription_update', 'user', 'subscription',

                  ]

    def get_user_name(self, app):
        return app.user.username

    def get_subscription_detail(self, app):
        return reverse('subscription', args=[app.pk])

    def get_subscription_cancel(self, app):
        if app.subscription.active:
            return reverse('subscription_cancel', args=[app.pk])
        else:
            ''

    def get_subscription_update(self, app):
        plans = Plan.objects.all()
        plan_url = {str(plan): reverse('subscription_update', args=[app.pk, plan.pk]) for plan in plans}
        return plan_url


class AppCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = ['name', 'description']
