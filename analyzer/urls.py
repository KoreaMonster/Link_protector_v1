from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'analyzer'

#DRF Router 설정
router = DefaultRouter()
router.register('analysis', views.URLAnalysisViewSet, basename='analysis')


urlpatterns = [
    # 메인 페이지 (URL 입력)
    path('', views.IndexView.as_view(), name='index'),
    # 결과 페이지 (Template)
    path('result/<int:pk>/', views.AnalysisDetailView.as_view(), name='result'),

    #api 앤드포인트
    path('api/analyze/', views.AnalyzeAPIView.as_view(), name='api_analyze'),
    path('api/recent/', views.RecentAnalysisAPIView.as_view(), name='api_recent'),

    # ViewSet 라우팅 (자동으로 여러 URL 생성)
    # GET /api/analysis/ - 목록
    # GET /api/analysis/{id}/ - 상세
    # GET /api/analysis/recent/ - 최근 10개
    path('api/', include(router.urls)),
]