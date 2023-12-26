from django.urls import path, include

urlpatterns = [
    path("shipments/", include("api.v1.shipments.urls")),
]
