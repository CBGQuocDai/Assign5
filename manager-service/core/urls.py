from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManagerViewSet, CouponViewSet

router = DefaultRouter()
router.register(r'managers', ManagerViewSet)
router.register(r'coupons', CouponViewSet)

urlpatterns = [path('', include(router.urls))]
