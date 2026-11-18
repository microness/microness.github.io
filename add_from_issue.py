"""휴대폰에서 연 깃허브 이슈를 poems/<제목>.txt 로 바꾼다.

이슈 제목 = 시 제목, 이슈 본문 = 시 본문.
값은 환경변수로만 받는다 (워크플로에서 직접 끼워 넣지 않음).
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
title = os.environ["ISSUE_TITLE"].strip().replace("/", "／").replace("\\", "＼")
body = (os.environ.get("ISSUE_BODY") or "").replace("\r\n", "\n").strip("\n")

if not title or not body.strip():
    raise SystemExit("제목이나 본문이 비어 있습니다.")

target = ROOT / "poems" / f"{title}.txt"
n = 2
while target.exists():  # 같은 제목이 이미 있으면 "제목 (2)"
    target = ROOT / "poems" / f"{title} ({n}).txt"
    n += 1

target.write_text(body + "\n", encoding="utf-8")

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as f:
    f.write(f"file={target.relative_to(ROOT).as_posix()}\n")
print(f"추가: {target.name}")
