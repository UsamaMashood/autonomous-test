from django.urls import path
from .views import (
    AppListView, AppCreateView, AppRetrieveDeleteView,
    subscription_view, subscription_cancel_view,
    subscription_update_view
)

urlpatterns = [
    path('', AppListView.as_view(), name='app_list'),
    path('create', AppCreateView.as_view(), name='app_create'),
    path('<int:pk>', AppRetrieveDeleteView.as_view(), name='app-detail'),
    path('<int:pk>/subscription', subscription_view, name='subscription'),
    path('<int:pk>/subscription/cancel', subscription_cancel_view, name='subscription_cancel'),
    path('<int:pk>/subscription/update/<int:plan_pk>', subscription_update_view, name='subscription_update')

]
