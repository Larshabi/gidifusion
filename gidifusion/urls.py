from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from team.views import Ticket, PayCallback, PaymentVerify, Paid_Teams, Paid_ticket

schema_view = get_schema_view(
    openapi.Info(
        title="GIDIFUSION API",
        default_version='v1',
        description='Rest API for Gidifusion',
        contact=openapi.Contact(email="admin@gmail.com"), 
    ),
    public=True,
    permission_classes=[AllowAny]
    )

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('team/', include('team.urls')),
    path('ticket/', Ticket.as_view()),
    path('ticket/paid/',Paid_ticket.as_view()),
    path('team/paid/', Paid_Teams.as_view()),
    path('paystack/callback/', PayCallback.as_view()), 
    path('paystack/verify/<str:tref>/', PaymentVerify.as_view()),
]
