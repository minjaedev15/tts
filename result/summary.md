# CI/CD Setup Summary

## What I changed
### Code fixes / CI hardening
- **`core.py`**
  - Temp file을 전역 경로 대신 **요청마다 `tempfile.mkstemp()`**로 생성(레이스/잔여 파일 위험 감소).
  - CI/테스트용 토글:
    - `TTS_DISABLE_TTS=1` → `edge_tts` 네트워크 호출 없이 placeholder `.mp3`(`ID3` 바이트) 생성
    - `TTS_DISABLE_AUDIO=1` → 오디오 재생 스킵
    - `TTS_DISABLE_CLEANUP=1` → 임시파일 정리 스케줄링 비활성화

  - 성능 최적화:
    - `detect_language()`는 `lru_cache`로 캐싱
    - **언어별 보이스 선택을 `OrderedDict` 기반 true LRU**로 캐싱(동기/스레드 안전하게 동작)

- **`requirements.txt`**
  - **PyObjC**는 **macOS(Darwin)**에서만 설치되도록 조건부 가드
    - `pyobjc-core`, `pyobjc-framework-*` guarded with `platform_system=="Darwin"`

### Docker/로컬 CI 실행
- **`docker/Dockerfile.ci`**
  - Ubuntu에서 단위 테스트를 동일 환경으로 재현하기 위한 CI용 Python 이미지
- **`docker-compose.yml`**
  - `docker compose run --rm tts-ci` 로 `py_compile` + `unittest` 실행

### CI (GitHub Actions) - Docker-based (Ubuntu only)
- **`.github/workflows/ci.yml`**
  - Ubuntu에서 Docker로만 unit tests 실행
  - Matrix: Python `3.10/3.11/3.12`
  - `docker compose ... build`
  - `docker compose ... run --rm tts-ci`
  - (컨테이너 내부 기본 설정: `TTS_DISABLE_TTS=1`, `TTS_DISABLE_AUDIO=1`)

### CD (safe placeholder) - Docker-based zip step
- **`.github/workflows/cd.yml`**
  - Docker 컨테이너 내부에서 `tts-source.zip` 생성 후 업로드

### Executable builds (.dmg/.exe/Linux executable) - Nuitka
- **`.github/workflows/build.yml`**
  - OS matrix:
    - Ubuntu: **docker-compose에서** Linux 실행파일/zip 생성
    - Windows: host에서 Nuitka standalone 빌드/패키징
    - macOS: host에서 Nuitka standalone 빌드(`--mode=app`)/DMG
  - Ubuntu 산출물:
    - `result/build_output.zip`
  - macOS 산출물:
    - `result/build_output.dmg` (zip 포함)
  - 업로드 artifact:
    - `build-ubuntu-latest-zip`
    - `build-windows-latest-zip`
    - `build-macos-latest-zip`, `build-macos-latest-dmg`

### Tests
- **`tests/test_core.py`**
  - `TTS_DISABLE_TTS=1`에서 `core.speak()`가 placeholder `.mp3` 파일을 실제로 생성하는지 검증

## 로컬에서 Docker CI-equivalent 실행
```bash
docker compose build
docker compose run --rm tts-ci
```

## Files added/updated
- Updated: `core.py`, `requirements.txt`
- Added: `.github/workflows/ci.yml`, `.github/workflows/cd.yml`, `.github/workflows/build.yml`
- Added: `docker/Dockerfile.ci`, `docker-compose.yml`
- Added: `tests/test_core.py`
- Added: `.gitignore`, `result/summary.md`
