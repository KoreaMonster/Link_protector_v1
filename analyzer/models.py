from django.db import models
from django.utils import timezone
# Create your models here.

class URLAnalysis(models.Model):

    #기본 URL 정보 - admin에 어떻게 보일지를 지정하는 중
    original_url = models.URLField(
        max_length= 500,
        verbose_name= "원본 URL",
        help_text= "사용자가 입력한 URL"
    )

    final_url = models.URLField(
        max_length= 500,
        verbose_name= "최종 URL",
        help_text= "Redirection 이후 최종 도착 URL"
    )

    domain = models.CharField(
        max_length= 255,
        verbose_name= "도메인",
        help_text= "URL의 도메인 부분"
    )

    #페이지 메타데이터.
    page_title = models.CharField(
        max_length= 255,
        blank= True,
        null= True,
        verbose_name= "페이지 제목"
    )

    # 스크린샷 경로 (이것만 사용)
    screenshot_path = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="스크린샷 경로"
    )

    #분석 시간
    analyzed_at = models.DateTimeField(
        auto_now_add=True,  # 생성 시 자동으로 현재 시간
        verbose_name="분석 시간"
    )

    #네트워크 분석 데이터
    network_requests = models.IntegerField(
        default= 0,
        verbose_name= "네트워크 요청 수"
    )

    redirects = models.IntegerField(
        default=0,
        verbose_name="리다이렉션 수"
    )

    js_errors = models.IntegerField(
        default= 0,
        verbose_name= "JavaScript 오류 수"
    )

    # 호스트 정보
    ip_address = models.GenericIPAddressField(
        blank= True,
        null= True,
        verbose_name= "IP 주소"
    )

    risk_score = models.IntegerField(
        default= 0,
        verbose_name= "위험도 점수",
        help_text= "0-100사이 값, 높을 수록 위험"
    )
    risk_level = models.CharField(
        max_length=20,
        choices=[
            ('low', '낮음'),
            ('medium', '중간'),
            ('high', '높음'),
        ],
        default='low',
        verbose_name="위험 수준"
    )
    #상세분석 데이터 JSON
    detail_data = models.JSONField(
        blank= True,
        null= True,
        verbose_name= "상세 분석 데이터",
        help_text= "네트워크 트래픽, 포트 스탠 결과 등. ."
    )

    class Meta:
        verbose_name = "URL 분석"
        verbose_name_plural = "URL 분석 목록"

        ordering = ["-analyzed_at"]      #최신순으로 정렬하기

    def __str__(self):
        return f"{self.domain} - {self.analyzed_at.strftime('%Y-%m-%d %H:%M')}"

    def get_risk_label(self):
        #위험도 레이블 반환
        if self.risk_score < 30:
            return "낮은 위험도"
        elif self.risk_score < 70:
            return "중간 위험도"
        else:
            return "높은 위험도"

    def get_risk_message(self):
        """위험도 메시지 반환"""
        if self.risk_score < 30:
            return "현재까지 발견된 명백한 위협 요소는 없습니다. 하지만 항상 주의가 필요합니다."
        elif self.risk_score < 70:
            return "일부 의심스러운 요소가 발견되었습니다. 신중하게 접근하세요."
        else:
            return "위험한 요소가 다수 발견되었습니다. 접근을 권장하지 않습니다."















