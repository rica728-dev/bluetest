import sys
import json
import csv
import os

# 원본 8개 헤더 정의
HEADERS = [
    "회수ID",
    "등록일",
    "품목",
    "제조사",
    "회수사유",
    "조치상태",
    "판매지역",
    "담당기관"
]

# 파일명 금지 문자 목록 (Windows/Linux/Mac 표준 공통)
INVALID_FILENAME_CHARS = {'\\', '/', ':', '*', '?', '"', '<', '>', '|'}

def main():
    # 1. 명령행 인자 개수 검증 (스크립트명 제외 정확히 1개여야 함)
    if len(sys.argv) != 2:
        print("[error] 명령행 키워드는 정확히 1개만 입력해야 합니다.")
        return

    # 앞뒤 공백 제거
    keyword = sys.argv[1].strip()

    # 인자가 빈 문자열인 경우 예외 처리
    if not keyword:
        print("[error] 키워드가 공백이거나 비어 있습니다.")
        return

    # 2. 파일명 금지 문자 포함 여부 확인
    if any(char in INVALID_FILENAME_CHARS for char in keyword):
        print("[error] 키워드에 파일명으로 사용할 수 없는 금지 문자(\\ / : * ? \" < > |)가 포함되어 있습니다.")
        return

    # 스크립트 위치 기준으로 입력/출력 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "첨부", "수산물_회수정보.json")
    output_filename = f"결과_{keyword}.csv"
    csv_path = os.path.join(base_dir, output_filename)

    # 3. 입력 JSON 파일 존재 여부 확인 및 로드
    if not os.path.exists(json_path):
        print(f"[error] 입력 파일이 존재하지 않습니다: {json_path}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[error] JSON 파일 처리 중 오류 발생: {e}")
        return

    # 4. 8개 필드 대상 부분일치 검색 (순서 유지)
    matched_rows = []
    for item in data:
        # 원본 8개 필드 값 중 하나라도 키워드를 부분 포함하는지 검사
        is_matched = any(keyword in str(item.get(header, '')) for header in HEADERS)
        if is_matched:
            matched_rows.append(item)

    # 5. CSV 파일 생성 및 저장 (utf-8-sig)
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()
            if matched_rows:
                writer.writerows(matched_rows)

        print(f"[ok] {len(matched_rows)}건 저장 -> {output_filename}")

    except Exception as e:
        print(f"[error] CSV 파일 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
