# 시

`poems/` 폴더에 txt 파일을 넣으면 사이트에 올라갑니다.

- **파일명 = 시 제목** (`온기.txt` → 제목 "온기")
- **파일 내용 = 시 본문** (쓴 그대로. 줄바꿈은 행, 빈 줄은 연)
- **날짜 = 처음 올린 시각** (한국 시간). 본문을 고치거나 파일명을 바꿔도 날짜는 그대로.

올리면 1~2분 뒤 사이트에 반영됩니다.


## 처음 한 번만: 설정

1. 깃허브에서 **`아이디.github.io`** 라는 이름으로 **Public** 저장소를 만든다.
   (무료 계정은 공개 저장소만 Pages를 쓸 수 있음)
2. 이 폴더의 파일을 전부 저장소에 올린다. **`.github` 폴더도 꼭 함께** 올려야 한다.
   - 웹에서 끌어다 놓을 경우: 맥은 Finder에서 `Cmd + Shift + .` 을 눌러야 `.github` 폴더가 보인다.
   - git을 쓸 경우: `git init` → `git add -A` → `git commit` → `git push`
3. 저장소 **Settings → Pages → Build and deployment → Source** 를 **GitHub Actions** 로 바꾼다.
4. **Actions** 탭에서 "사이트 배포"를 한 번 실행한다 (Run workflow).
   끝나면 `https://아이디.github.io` 에서 열린다.


## PC에서 시 올리기

- **웹**: 저장소에서 `poems` 폴더로 들어가 **Add file → Upload files** 로 txt를 끌어다 놓고 Commit.
- **git**: 로컬 `poems/` 에 txt를 저장하고 commit, push.

고치기: txt를 수정해서 다시 올리면 된다. 지우기: txt를 지우면 목록에서도 사라진다.


## 휴대폰에서 시 올리기

깃허브 앱(iOS/Android)에서 **이슈를 열면** 그게 시로 등록됩니다.

1. 깃허브 앱 → 이 저장소 → **Issues** → 새 이슈(**+**)
2. **제목**에 시 제목, **본문**에 시를 쓴다.
3. **Create** (또는 Submit).

1~2분 뒤 `poems/제목.txt` 로 저장되고, 사이트에 반영되고, 이슈는 "등록했습니다" 댓글과 함께 자동으로 닫힙니다.

- 저장소 주인이 연 이슈만 시로 처리합니다. 다른 사람이 이슈를 열어도 올라가지 않습니다.
- 같은 제목의 시가 이미 있으면 `제목 (2).txt` 로 저장됩니다. 나중에 PC에서 파일명을 고치면 됩니다.
- 앱이 없으면 휴대폰 브라우저로 github.com 에 들어가 `poems` 폴더 → **Add file → Create new file** → 파일명에 `제목.txt`, 내용에 시를 써도 됩니다.


## 알아 둘 것

- 메모장에서 저장한 txt는 UTF-8이든 옛 ANSI(EUC-KR)든 둘 다 읽습니다.
- 여러 편을 한 번에 올리면 같은 시각으로 찍히고, 그 안에서는 제목 가나다순입니다.
- 파일명에 `/` 는 쓸 수 없습니다. 휴대폰으로 올린 제목에 `/` 가 있으면 `／`(전각)로 바꿔 저장합니다.
- 오류가 나면 **Actions** 탭에서 빨간 표시가 된 실행을 눌러 보면 이유가 나옵니다.
  "Permission denied" 류라면 Settings → Actions → General → Workflow permissions 를
  **Read and write permissions** 로 바꾼다.


## 구성

```
poems/                   원고(txt). 여기만 건드리면 된다
site/style.css           종이 줄, 글꼴, 링크 색
site/fonts/              나눔고딕코딩, 은 바탕 (+ 라이선스)
build.py                 txt → HTML (파이썬 기본 기능만 사용)
add_from_issue.py        휴대폰 이슈 → txt
.github/workflows/       올라오면 자동으로 만들고 배포
```

미리보기(선택): `python3 build.py` 후 `_site/index.html` 을 브라우저로 연다.
