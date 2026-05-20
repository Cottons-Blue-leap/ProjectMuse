# Project Muse — Assets

시리즈 공통 자산 자리. 음악·영상 workflow 양쪽에서 reference.

## 하위 자리

### `fonts/`
시리즈 typography 자리.

```text
fonts/
  gfs_didot/   # GFS Didot SIL OFL (Google Fonts 다운로드)
    GFSDidot-Regular.otf  # 또는 .ttf
    OFL.txt
```

다운로드 출처: https://fonts.google.com/specimen/GFS+Didot

### `series_signature_reference/`
시리즈 시그너처 5축 reference 자료. 예시 layout 박힘 이미지, 다른 시리즈 reference (4AD album covers 등) 보관 자리.

### `paintings_master_reference/`
명화 원본 reference 누적 자리 (시리즈 차원 — 곡 결정 전 후보 명화 자료).

곡 결단 후에는 작품별 `works/<piece>/video/art_sources/` 자리로 이동·복사.

## 자료 누적 원칙

- 무게 큰 파일 (4K painting scans 등)은 본 자리에 박되 `.gitignore` 검토 의제.
- 라이선스 자료 (SIL OFL · public domain notice)는 자료와 동일 폴더에 보관.
- 폰트는 `*.otf`/`*.ttf` + OFL.txt 한 쌍이 lock 양식.
