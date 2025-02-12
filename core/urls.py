from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include("account.urls", namespace='account')),
    path('api/mergintransactions/', include("mergintransactions.urls", namespace='mergintransactions'))
]
