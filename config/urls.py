# config/urls.py

from django.contrib import admin
from django.urls import path, include # <--- Nhớ import include
from django.conf import settings
from django.conf.urls.static import static

# 1. Import các công cụ cần thiết từ rest_framework và app của bạn
from rest_framework.routers import DefaultRouter
from production.views import FinishedBundleViewSet

# 2. Tạo Router và đăng ký API 'finished-bundles'
router = DefaultRouter()
router.register(r'finished-bundles', FinishedBundleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 3. Đưa tất cả API vào đường dẫn bắt đầu bằng 'api/'
    path('api/', include(router.urls)), 
]

# Cấu hình media cho môi trường debug (giữ nguyên như cũ của bạn)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)