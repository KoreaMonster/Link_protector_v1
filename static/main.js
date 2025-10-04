// Link Shield - Main JavaScript

// 페이지 로드시 애니메이션 효과
document.addEventListener('DOMContentLoaded', function() {
    // 카드 호버 효과 강화
    const cards = document.querySelectorAll('.card, .info-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // URL 입력 필드 유효성 검사
    const urlInput = document.getElementById('url');
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            const url = this.value;
            if (url && !url.startsWith('http://') && !url.startsWith('https://')) {
                this.setCustomValidity('URL은 http:// 또는 https://로 시작해야 합니다.');
            } else {
                this.setCustomValidity('');
            }
        });
    }

    // 스크린샷 확대 기능
    const screenshot = document.querySelector('.screenshot-img');
    if (screenshot) {
        screenshot.style.cursor = 'zoom-in';
        screenshot.addEventListener('click', function() {
            const modal = createImageModal(this.src);
            document.body.appendChild(modal);
        });
    }
});

// 이미지 모달 생성 함수
function createImageModal(imageSrc) {
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        cursor: zoom-out;
    `;

    const img = document.createElement('img');
    img.src = imageSrc;
    img.style.cssText = `
        max-width: 90%;
        max-height: 90%;
        border-radius: 10px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
    `;

    modal.appendChild(img);

    // 클릭시 모달 닫기
    modal.addEventListener('click', function() {
        modal.remove();
    });

    return modal;
}

// 부드러운 스크롤
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});