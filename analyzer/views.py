from django.shortcuts import render, redirect
from django.views import View
from datetime import datetime
from urllib.parse import urlparse


class IndexView(View):
    """URL 입력 페이지"""

    def get(self, request):
        return render(request, 'index.html')


class AnalyzeView(View):
    """URL 분석 처리 및 결과 페이지"""

    def post(self, request):
        # 사용자가 입력한 URL 가져오기
        url = request.POST.get('url', '')

        if not url:
            return redirect('analyzer:index')

        # 데모 데이터 생성 (실제로는 Docker + Selenium으로 분석)
        result = self.create_demo_result(url)

        return render(request, 'result.html', {'result': result})

    def create_demo_result(self, url):
        """
        데모용 분석 결과 생성
        나중에 실제 Docker + Selenium 분석으로 교체할 부분
        """
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        # 데모 데이터
        result = {
            'original_url': url,
            'final_url': url,  # 리다이렉션이 없다고 가정
            'page_title': f'{domain} 웹사이트',
            'domain': domain,
            'ip_address': '123.456.78.90',  # 데모 IP
            'analyzed_at': datetime.now().strftime('%Y년 %m월 %d일 %H:%M:%S'),
            'screenshot': None,  # 아직 스크린샷 기능 없음
            'network_requests': '12',
            'redirects': '0',
            'js_errors': '0',
            'risk_score': '25',
            'risk_level': 'low',
            'risk_label': '낮은 위험도',
            'risk_message': '현재까지 발견된 명백한 위협 요소는 없습니다. 하지만 항상 주의가 필요합니다.'
        }

        return result