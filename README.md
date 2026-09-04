# 수산물 회수정보 검색

제공된 JSON 60건을 검색하는 정적 웹페이지와 키워드 검색 결과를 CSV로 내보내는 Python 도구입니다.

## 웹페이지 실행 및 GitHub Pages 배포

저장소의 루트 디렉터리를 그대로 GitHub에 올린 뒤 저장소 **Settings → Pages**에서 배포 브랜치와 루트(`/`)를 선택하면 됩니다. 배포 후 `index.html`이 `수산물_회수정보.json`을 불러옵니다.

로컬에서는 브라우저의 파일 보안 정책 때문에 JSON 로딩이 차단될 수 있으므로 간단한 웹 서버를 사용하세요.

```bash
python -m http.server 8000
```

그런 다음 <http://localhost:8000>을 엽니다.

## CSV 추출 도구

Python 3 표준 라이브러리만 사용하며 별도 설치가 필요하지 않습니다. 키워드는 원본 8개 필드 전체에서 대소문자와 공백을 무시한 부분일치로 검색됩니다.

```bash
python export_recall_csv.py 연어
python export_recall_csv.py 회수중 -o 회수중.csv
python export_recall_csv.py 인천 -i 수산물_회수정보.json -o output/인천.csv
```

출력 CSV는 Excel에서 한글이 깨지지 않도록 UTF-8 BOM 형식으로 저장됩니다.
