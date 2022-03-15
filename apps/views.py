from datetime import datetime, timedelta
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import (
    AppSerializer, PlanSerializer,
    SubscriptionSerializer, AppCreateSerializer
)
from .models import (
    App, Plan, Subscription
)

@api_view()
@permission_classes([AllowAny,])
def api_endpoints(request):
    links = {
        'register': reverse('register'),
        'token': reverse('token_obtain_pair'),
        'token_refresh': reverse('token_refresh'),
        'app_list': reverse('app_list'),
        'app_create': reverse('app_create'),
        'password_reset': '/api/password_reset',

    }
    return Response(links)


class AppListView(ListAPIView):
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return App.objects.filter(user=self.request.user)


class AppCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = AppCreateSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            name = data['name']
            description = data['description']
            plan = Plan.objects.get(name='free')
            subscription = Subscription(plan=plan, active=True)
            subscription.save()
            app = App(
                name=name, description=description,
                user=request.user, subscription=subscription
            )

            app.save()
            return Response({ 'msg': 'app is created' }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppRetrieveDeleteView(RetrieveUpdateDestroyAPIView):

    serializer_class = AppSerializer
    queryset = App.objects.all()
    permission_classes = [IsAuthenticated]


@api_view()
@permission_classes([IsAuthenticated, ])
def subscription_view(request, pk):
    app = App.objects.get(pk=pk, user=request.user)
    serializer = SubscriptionSerializer(app.subscription)
    return Response(serializer.data)


@api_view()
@permission_classes([IsAuthenticated, ])
def subscription_cancel_view(request, pk):
    try:
        app = App.objects.get(pk=pk, user=request.user, subscription__active=True)
        if app:
            sub = app.subscription
            sub.active = False
            sub.save()
        return Response(SubscriptionSerializer(sub).data)
    except:
        return Response({'msg': 'No active subscriptions'}, status=status.HTTP_204_NO_CONTENT)


@api_view()
@permission_classes([IsAuthenticated, ])
def subscription_update_view(request, pk, plan_pk):
    try:
        app = App.objects.get(pk=pk, user=request.user )
        try:
            plan = Plan.objects.get(pk=plan_pk)
            if app and plan:
                sub = app.subscription
                month_later = sub.last_update_date + timedelta(30)

                if sub.plan.id==plan_pk and sub.last_update_date <= month_later:
                    return Response({'msg': 'subscription is not expire'})
                sub.active = True
                sub.plan = plan
                sub.last_update_date = datetime.today().date()
                sub.save()
                return Response(SubscriptionSerializer(sub).data)
        except:
            return Response({'msg': 'No such plan exists'}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({'msg': 'No such app exists'}, status=status.HTTP_204_NO_CONTENT)