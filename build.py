"""poems/*.txt 를 읽어 _site/ 에 정적 HTML 사이트를 만든다.

- 파일명(확장자 제외) = 시 제목
- 파일 내용 = 시 본문
- 날짜 = 그 파일이 저장소에 처음 추가된 커밋 시각 (한국 시간)
파이썬 기본 라이브러리만 사용한다.
"""
import html
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POEMS = ROOT / "poems"
ASSETS = ROOT / "site"
OUT = ROOT / "_site"
KST = timezone(timedelta(hours=9))


def first_added(path: Path) -> datetime:
    """파일이 처음 추가된 커밋 시각. 이름을 바꿔도 원래 시각을 따라간다."""
    rel = path.relative_to(ROOT).as_posix()
    try:
        out = subprocess.run(
            ["git", "log", "--follow", "--diff-filter=A", "--format=%cI", "--", rel],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.split()
    except (subprocess.CalledProcessError, FileNotFoundError):
        out = []
    if out:
        return datetime.fromisoformat(out[-1]).astimezone(KST)
    # 아직 커밋하지 않은 파일(로컬 미리보기용)
    return datetime.fromtimestamp(path.stat().st_mtime, KST)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "cp949"):  # 옛 메모장(ANSI) 저장 파일도 읽는다
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("utf-8", errors="replace")
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    return "\n".join(lines).strip("\n")


def page(title: str, body: str, css: str) -> str:
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def main() -> None:
    poems = []
    for path in POEMS.glob("*.txt"):
        poems.append({"title": path.stem, "text": read_text(path), "when": first_added(path)})

    # 최신순. 같은 시각에 올라온 것끼리는 제목 가나다순.
    poems.sort(key=lambda p: p["title"])
    poems.sort(key=lambda p: p["when"], reverse=True)

    # 주소는 제목이 아니라 올린 시각으로 만든다 (제목을 바꿔도 링크 유지)
    used = set()
    for p in poems:
        slug = p["when"].strftime("%Y%m%d-%H%M%S")
        n = 2
        base = slug
        while slug in used:
            slug = f"{base}-{n}"
            n += 1
        used.add(slug)
        p["slug"] = slug

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ASSETS, OUT)
    (OUT / "poems").mkdir()

    for p in poems:
        t = html.escape(p["title"])
        body = (
            '<a href="../">홈</a>\n'
            f'<p class="date">{p["when"]:%Y.%m.%d}</p>\n'
            f"<h1>{t}</h1>\n"
            f'<div class="poem">{html.escape(p["text"])}</div>'
        )
        (OUT / "poems" / f'{p["slug"]}.html').write_text(page(t, body, "../style.css"), encoding="utf-8")

    parts = []
    year = None
    for p in poems:
        if p["when"].year != year:
            if year is not None:
                parts.append("</ul>\n")
            year = p["when"].year
            parts.append(f'<p class="year">{year}</p>\n<ul class="list">')
        parts.append(
            f'  <li><span class="date">{p["when"]:%m.%d}</span>'
            f'<a href="poems/{p["slug"]}.html">{html.escape(p["title"])}</a></li>'
        )
    if year is not None:
        parts.append("</ul>")
    (OUT / "index.html").write_text(page("시", "\n".join(parts), "style.css"), encoding="utf-8")

    print(f"{len(poems)}편 생성 → {OUT}")


if __name__ == "__main__":
    main()
