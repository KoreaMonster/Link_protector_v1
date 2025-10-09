from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import render
from urllib.parse import urlparse
from .models import URLAnalysis
from .serializers import (
    URLAnalysisSerializer,
    URLAnalyzeRequestSerializer,
    RecentURLSerializer
)
import subprocess
import uuid
from pathlib import Path
from django.conf import settings
import json
from urllib.parse import urlparse

class IndexView(APIView):
    """
    메인 페이지 (Template 렌더링)
    GET /

    DRF APIView이지만 HTML 템플릿을 반환할 수 있습니다.
    """

    def get(self, request):
        # 최근 분석된 URL 10개 가져오기
        recent_urls = URLAnalysis.objects.all()[:10]

        context = {
            'recent_urls': recent_urls
        }
        return render(request, 'index.html', context)


class AnalyzeAPIView(APIView):
    """
    URL 분석 API
    POST /api/analyze/

    요청 본문:
    {
        "url": "https://example.com"
    }

    응답:
    {
        "id": 1,
        "original_url": "https://example.com",
        "final_url": "https://example.com",
        "domain": "example.com",
        "page_title": "Example Domain",
        "risk_score": 25,
        "risk_level": "low",
        ...
    }
    """

    def post(self, request):
        # 1. 입력 데이터 검증
        serializer = URLAnalyzeRequestSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'error': '입력 데이터가 유효하지 않습니다.',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 검증된 URL 가져오기
        url = serializer.validated_data['url']

        # 3. URL 분석 수행 (현재는 데모 데이터)
        analysis_result = self.analyze_url(url)

        parsed_url = urlparse(analysis_result['final_url'])
        domain = parsed_url.netloc
        # parsed.netloc   # 'www.example.com:8080' (도메인)

        # 4. 데이터베이스에 저장
        url_analysis = URLAnalysis.objects.create(
            # Docker에서 받은 데이터
            original_url=analysis_result['original_url'],
            final_url=analysis_result['final_url'],
            page_title=analysis_result['page_title'],
            screenshot_path=analysis_result.get('screenshot_path', ''),

            # 직접 추출한 데이터
            domain=domain,

            # 임시값 (Phase 6, 7에서 실제 구현 예정)
            ip_address='0.0.0.0',
            network_requests=0,
            redirects=0,
            js_errors=0,
            risk_score=25,
            risk_level='low',
        )

        # 5. 저장된 데이터를 Serializer로 변환하여 응답
        response_serializer = URLAnalysisSerializer(url_analysis)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )


    def analyze_url(self, url):
        """
        URL 분석 로직 - Docker 컨테이너 실행

        왜 Docker를 실행하나?
        - 악성 URL이 서버를 공격할 수 있음
        - Docker는 격리된 환경 = 안전
        """

        # id를 생성 -> 여러 사람이 동시에 분석 진행하는 것 구분하려고 / 8자
        analysis_id = str(uuid.uuid4())[:8]
        #결과를 저장하는 폴더 생성 -> id로 구분되도록
        results_dir = Path(settings.BASE_DIR) / 'results' / analysis_id
        results_dir.mkdir(parents=True, exist_ok=True)

        print(f"📁 결과 폴더 생성: {results_dir}")

        #Docker 실행명령
        docker_command = [
            'docker', 'run',
            '--rm',
            '-v', f'{results_dir}:/output',  # 폴더 공유
            'selenium-analyzer',  # 우리가 만든 이미지
            'python', 'analyze.py', url  # 실행할 명령
        ]
        print(f"🐳 Docker 실행 중...")

        try:
            result = subprocess.run(
                docker_command,
                capture_output=True,  # 출력 내용 받기
                text=True,  # 문자열로 받기
                timeout=120  # 최대 60초 (너무 오래 걸리면 중단)
            )

            # 5단계: 실행 결과 확인
            if result.returncode != 0:  # 0이 아니면 오류
                print(f"❌ Docker 오류: {result.stderr}")
                raise Exception(f"Docker 실행 실패: {result.stderr}")

            print(f"✅ Docker 실행 완료!")

        except subprocess.TimeoutExpired:
            print(f"⏰ 시간 초과 (120초)")
            raise Exception("분석 시간 초과")

        # 6단계: 결과 파일 읽기

        result_file = results_dir / 'result.json'
        screenshot_file = results_dir / 'screenshot.png'

        # JSON 파일 읽기
        with open(result_file, 'r', encoding='utf-8') as f:
            analysis_result = json.load(f)

        # 스크린샷 경로 추가
        if screenshot_file.exists():
            # 상대 경로로 저장 (웹에서 접근 가능하게)
            analysis_result['screenshot_path'] = f'/results/{analysis_id}/screenshot.png'

        print(f"📊 분석 결과: {analysis_result['page_title']}")

        return analysis_result

class URLAnalysisViewSet(viewsets.ReadOnlyModelViewSet):
    """
    URL 분석 결과 ViewSet (읽기 전용)

    자동 생성되는 엔드포인트:
    - GET /api/analysis/ : 전체 목록 (페이지네이션)
    - GET /api/analysis/{id}/ : 특정 분석 결과 상세 조회

    커스텀 액션:
    - GET /api/analysis/recent/ : 최근 10개 분석 결과

    ViewSet은 CRUD 기능을 자동으로 제공합니다.
    ReadOnlyModelViewSet은 읽기(list, retrieve)만 가능합니다.
    """

    queryset = URLAnalysis.objects.all()
    serializer_class = URLAnalysisSerializer

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        최근 10개 분석 결과
        GET /api/analysis/recent/

        응답:
        [
            {
                "id": 1,
                "original_url": "https://example.com",
                "domain": "example.com",
                ...
            },
            ...
        ]
        """
        recent = self.queryset[:10]
        serializer = RecentURLSerializer(recent, many=True)
        return Response(serializer.data)


class RecentAnalysisAPIView(APIView):
    """
    최근 분석 목록 API
    GET /api/recent/

    응답:
    {
        "count": 10,
        "results": [
            {
                "id": 1,
                "original_url": "https://example.com",
                "domain": "example.com",
                "analyzed_at": "2025-10-05T13:30:00",
                "risk_score": 25,
                "risk_level": "low"
            },
            ...
        ]
    }
    """

    def get(self, request):
        # 최근 10개 가져오기
        recent = URLAnalysis.objects.all()[:10]

        # Serializer로 변환
        serializer = RecentURLSerializer(recent, many=True)

        return Response({
            'count': recent.count(),
            'results': serializer.data
        })


class AnalysisDetailView(APIView):
    """
    특정 분석 결과 상세 조회 (Template 렌더링)
    GET /result/{id}/

    result.html 페이지를 렌더링합니다.
    """

    def get(self, request, pk):
        try:
            url_analysis = URLAnalysis.objects.get(pk=pk)
        except URLAnalysis.DoesNotExist:
            return Response(
                {'error': '분석 결과를 찾을 수 없습니다.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Template에 전달할 데이터
        result = {
            'id': url_analysis.id,
            'original_url': url_analysis.original_url,
            'final_url': url_analysis.final_url,
            'page_title': url_analysis.page_title,
            'domain': url_analysis.domain,
            'ip_address': url_analysis.ip_address,
            'analyzed_at': url_analysis.analyzed_at.strftime('%Y년 %m월 %d일 %H:%M:%S'),
            'screenshot': url_analysis.screenshot.url if url_analysis.screenshot else None,
            'network_requests': url_analysis.network_requests,
            'redirects': url_analysis.redirects,
            'js_errors': url_analysis.js_errors,
            'risk_score': url_analysis.risk_score,
            'risk_level': url_analysis.risk_level,
            'risk_label': url_analysis.get_risk_label(),
            'risk_message': url_analysis.get_risk_message(),
        }

        return render(request, 'result.html', {'result': result})