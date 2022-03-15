from django.contrib import admin
from .models import (
    App, Subscription, Plan
)

admin.site.register(App)
admin.site.register(Subscription)
admin.site.register(Plan)
