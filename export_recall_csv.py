#!/usr/bin/env python3
"""키워드가 포함된 수산물 회수정보를 CSV로 추출한다."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELDS = ["회수ID", "등록일", "품목", "제조사", "회수사유", "조치상태", "판매지역", "담당기관"]
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_JSON = SCRIPT_DIR / "수산물_회수정보.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="원본 8개 필드 중 키워드가 부분일치하는 수산물 회수정보만 CSV로 저장합니다."
    )
    parser.add_argument("keyword", help="검색할 키워드(대소문자와 공백 무시)")
    parser.add_argument(
        "-i", "--input", type=Path, default=DEFAULT_JSON, metavar="JSON",
        help="입력 JSON 경로 (기본값: 스크립트와 같은 폴더의 수산물_회수정보.json)",
    )
    parser.add_argument(
        "-o", "--output", type=Path, default=Path("회수정보_검색결과.csv"), metavar="CSV",
        help="출력 CSV 경로 (기본값: 회수정보_검색결과.csv)",
    )
    return parser.parse_args()


def normalize(value: Any) -> str:
    return "".join(str(value if value is not None else "").casefold().split())


def main() -> int:
    args = parse_args()
    try:
        with args.input.open(encoding="utf-8-sig") as source:
            records = json.load(source)
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"오류: JSON을 읽을 수 없습니다: {exc}") from exc

    if not isinstance(records, list):
        raise SystemExit("오류: JSON 최상위 값은 객체 배열이어야 합니다.")

    query = normalize(args.keyword)
    matches = [
        record for record in records
        if isinstance(record, dict) and any(query in normalize(record.get(field)) for field in FIELDS)
    ]

    try:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8-sig", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=FIELDS, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(matches)
    except OSError as exc:
        raise SystemExit(f"오류: CSV를 저장할 수 없습니다: {exc}") from exc

    print(f"검색 결과 {len(matches)}건을 '{args.output}'에 저장했습니다.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
