from rest_framework import serializers
from .models import URLAnalysis

class URLAnalysisSerializer(serializers.ModelSerializer):
    # URL 분석 결과 Serialiazer

    #읽기 전용 필드(자동으로 생성)
    risk_label = serializers.CharField(source="get_risk_label", read_only=True)
    risk_message = serializers.CharField(source="get_risk_message", read_only=True)
    analyzed_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = URLAnalysis
        fields = [
            'id',
            'original_url',
            'final_url',
            'domain',
            'page_title',
            'screenshot',
            'analyzed_at',
            'analyzed_at_formatted',
            'network_requests',
            'redirects',
            'js_errors',
            'ip_address',
            'risk_score',
            'risk_level',
            'risk_label',
            'risk_message',
            'detail_data',
        ]
        read_only_fields = ['id', 'analyzed_at']

    def get_analyzed_at_formatted(self, obj):
        """분석 시간을 포맷팅"""
        return obj.analyzed_at.strftime('%Y년 %m월 %d일 %H:%M:%S')

class URLAnalyzeRequestSerializer(serializers.Serializer):
    #URL 분석 요청 Serializer

    url = serializers.URLField(
        max_length= 500,
        help_text= "분석할 URL(https:// 또는 http://"
    )

    def validate_url(self, value):
        #URL 유효성 검증
        if not (value.startwith('http://') or value.startwith("https://")):
            raise serializers.ValidationError(
                "URL은 http:// 또는 https://로 시작해야합니다."
            )
        return value

class RecentURLSerializer(serializers.ModelSerializer):
    #최근 분석 URL 간단 정보

    class Meta:
        model = URLAnalysis
        fields = [
            'id',
            'original_url',
            'domain',
            'analyzed_at',
            'risk_score',
            'risk_level',
        ]