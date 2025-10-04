from django.urls import path
from . import views

app_name = 'analyzer'

urlpatterns = [
    # 메인 페이지 (URL 입력)
    path('', views.IndexView.as_view(), name='index'),

    # URL 분석 처리
    path('analyze/', views.AnalyzeView.as_view(), name='analyze'),
]