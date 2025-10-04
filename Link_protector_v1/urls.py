from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django 관리자 페이지
    path('admin/', admin.site.urls),
    
    # analyzer 앱 연결 (메인 페이지로 설정)
    path('', include('analyzer.urls')),
]

# 개발 환경에서 static 파일 서빙
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)