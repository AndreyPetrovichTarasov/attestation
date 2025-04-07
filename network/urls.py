from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet
from django.urls import path
from . import views

app_name = "network"

router = DefaultRouter()
router.register(
    r"api/nodes", NetworkNodeViewSet, basename="api-nodes"
)  # добавим префикс для API

urlpatterns = [
    # HTML-вьюхи
    path("", views.NetworkNodeListView.as_view(), name="list"),
    path("<int:pk>/", views.NetworkNodeDetailView.as_view(), name="detail"),
    path("create/", views.NetworkNodeCreateView.as_view(), name="create"),
    path(
        "<int:pk>/add-product/",
        views.ProductCreateView.as_view(),
        name="product_create",
    ),
]

# добавляем DRF-маршруты
urlpatterns += router.urls

# добавляем media только в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
