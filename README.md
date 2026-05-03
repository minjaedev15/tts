# AI TTS Desktop App

🎙️ 현대적인 데스크톱용 텍스트-투-스피치 (TTS) 애플리케이션

## 특징

- **AI 기반 음성 합성**: Microsoft Edge TTS 엔진 사용
- **다국어 지원**: 자동 언어 감지 및 최적 음성 선택
- **크로스 플랫폼**: macOS, Windows, Linux 지원
- **데스크톱 앱**: PyWebView로 네이티브 UI 제공
- **빠른 빌드**: Nuitka로 standalone 실행 파일 생성

## 설치 및 실행

### 요구사항
- Python 3.8+
- pip

### 설치
```bash
# 저장소 클론
git clone <repository-url>
cd tts

# 가상환경 생성 (선택사항)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 실행
```bash
python3 src/app.py
```

## 빌드

### 로컬 빌드
```bash
./build.sh
```
결과물: `./build/build_output.zip` (및 macOS의 경우 `.dmg`)

### 옵션
- `--clean`: 빌드 폴더 정리
- `--version`: 버전 정보

### CI/CD 빌드
- GitHub Actions로 자동화된 크로스 플랫폼 빌드
- Docker 컨테이너 사용 (CI)

## 프로젝트 구조

```
tts/
├── src/                    # 소스 코드
│   ├── app.py             # 메인 UI 애플리케이션
│   ├── core.py            # TTS 핵심 로직
│   ├── language.py        # 언어 감지
│   ├── voice.py           # 음성 관리
│   └── audio.py           # 오디오 재생
├── tests/                 # 테스트
│   └── test_core.py
├── docker/                # Docker 설정
│   └── Dockerfile.ci
├── .github/workflows/     # CI/CD 워크플로우
│   ├── ci.yml
│   ├── build.yml
│   └── cd.yml
├── build.sh               # 빌드 스크립트
├── requirements.txt       # Python 의존성
├── docker-compose.yml     # Docker Compose (개발용)
├── .gitignore
└── README.md
```

## 사용법

1. 앱 실행
2. 텍스트 입력
3. "재생" 버튼 클릭
4. 음성이 자동으로 생성 및 재생

### 환경 변수
- `TTS_DISABLE_TTS=1`: TTS 비활성화 (테스트용)
- `TTS_DISABLE_AUDIO=1`: 오디오 재생 비활성화
- `TTS_DISABLE_CLEANUP=1`: 임시 파일 자동 삭제 비활성화

## 개발

### 테스트 실행
```bash
source venv/bin/activate
python3 -m unittest tests.test_core
```

### 코드 구조
- **app.py**: PyWebView 기반 UI, JavaScript 연동
- **core.py**: 비동기 TTS 생성, 임시 파일 관리
- **language.py**: langid로 언어 감지 (캐싱)
- **voice.py**: Edge TTS 음성 목록 로드 및 선택 (LRU 캐싱)
- **audio.py**: 플랫폼별 오디오 재생

## 라이선스

MIT License

## 기여

PR 환영! 이슈 제출 또는 개선 제안 부탁드립니다.