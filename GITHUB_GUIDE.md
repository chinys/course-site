# VSCode(Antigravity)에서 GitHub 연동 및 사용 가이드

이 문서는 로컬 PC 환경(VSCode)에서 Git을 초기화하고, GitHub 원격 저장소와 연동하여 버전 관리를 하는 전체 흐름과 핵심 명령어를 정리한 가이드입니다.

---

## 1. Git과 GitHub의 개념 차이
- **Git**: 내 컴퓨터(로컬) 안에서 파일의 변경 이력을 추적하고 버전을 관리해 주는 사령탑 시스템. (프로그램 그 자체)
- **GitHub**: Git으로 관리하는 내 프로젝트를 클라우드 안전 금고에 올려서, 언제 어디서든 접근하고 다른 개발자와 협업·공유할 수 있게 해주는 **웹 호스팅 플랫폼**. (구글 계정 등을 통해 가입/로그인 가능)

---

## 2. 사전 준비 (로컬 PC)

1. **Git 프로그램 다운로드 및 설치**
   - 개발자용이 아니더라도 기본 설정값 그대로('Next'만 계속 클릭) 로컬 PC에 설치해도 무방합니다.
   - **설치 확인 (VSCode 터미널)**:
     ```bash
     git --version
     # 또는
     git -v
     ```

2. **Git 계정 정보 등록 (식별자)**
   - 내가 남긴 커밋(저장 기록)에 이름표를 붙이기 위해 컴퓨터(터미널)에 정보를 입력합니다.
     ```bash
     git config --global user.name "본인 이름(예: gildong)"
     # (예시) git config --global user.name gildong
     git config --global user.email "가입 이메일(예: gd9999@gmail.com)"
     # (예시) git config --global user.email gd9999@gmail.com  
     ```

3. **설정 정보 확인**
   - 위 1, 2번 과정을 거친 후, 입력한 정보가 제대로 들어갔는지 확인합니다.
     ```bash
     git config --list
     # 또는
     git config -l
     ```

---

## 3. GitHub Repository (원격 저장소) 생성

1. **로컬에서 커밋 완료하기**
     ```bash
    git init
    git add .
    git commit -m "Initial commit"
    ```  
2. **새 저장소 만들기**
   - GitHub 로그인 후 우측 상단의 `+` 버튼 &rarr; **New repository** 클릭.

3. **환경 설정 (Configuration)**
   - **Repository name**: 영문, 숫자, 하이픈(-) 등을 조합해 신규 저장소 이름 입력.
   - **Choose visibility (공개 여부)**: 
     - `Public`: 누구나 볼 수 있음 (포트폴리오나 강의 사이트 등 외부 노출 시 필수).
     - `Private`: 비공개 (본인 및 초대한 사람만 볼 수 있음).
   - **다른 옵션(README, .gitignore 등)은 건드리지 않고 하단의 Create repository 버튼을 클릭**:
     - `Add a README`: 프로젝트 대문 역할을 하는 마크다운(.md) 설명서 파일 생성 (On/Off).
     - `Add .gitignore`: GitHub에 업로드하지 않을 보안 파일(DB 비번, 인증키 등)이나 무거운 캐시 폴더 패턴을 정의하는 파일. (GitHub에서 만들어도 되지만, **VSCode 로컬에서 직접 생성하고 관리하는 것이 더 유연하고 좋음**)
     - `Add license`: 다른 사람이 내 코드를 퍼갈 때의 권한 명시 (초기엔 필수 아님).

4. **로컬 코드를 GitHub로 보내기(Push)**
     ```bash
    git remote add origin https://github.com/본인계정/저장소이름.git
     # (예시) git remote add origin https://github.com/gildong/course-site.git     
    git branch -M main
    git push -u origin main
    ```
---

## 4. VSCode GUI의 초간편 사용 (Source Control)

터미널 명령어의 원리를 이해했다면, VSCode 좌측의 **'소스 제어(Source Control, 나뭇가지 아이콘)'** 탭을 사용해 클릭만으로 훨씬 직관적이고 편하게 버전 관리를 할 수 있습니다.

### 1) Repository 클론 (Clone) 방법
- **(사전작업) 현재 폴더의 기존 git 흔적 제거?** 숨김 폴더인 .git을 제거하면 됨

- **언제 쓰나요?** GitHub에 있는 원격 저장소를 내 PC로 처음 가져올 때 사용합니다.
- **현재 폴더에 git clone 하기(터미널)** : git clone https://github.com/본인계정/저장소이름.git . (예: git clone https://github.com/chinys/course-site .) 맨 마지막에 현재 폴더를 가르키는 . 추가함
- **git clone 다른 방법(참고만)** : 시작 화면이나 '소스 제어' 탭에서 **[리포지토리 복제 (Clone Repository)]**를 클릭합니다. 
 복사해 둔 GitHub 저장소 URL(`https://github.com/본인계정/저장소이름.git`)을 상단 검색창에 붙여넣고 Enter를 누릅니다.


### 2) Git 초기화 (Initialize) 방법
- **언제 쓰나요?** 내 PC에 있는 일반 프로젝트 폴더를 새롭게 Git으로 관리 시작하고 싶을 때 사용합니다. (`git init`과 동일)
- 해당 폴더를 VSCode로 연 뒤, 좌측 '소스 제어' 탭으로 이동합니다.
- 파란색 **[리포지토리 초기화 (Initialize Repository)]** 버튼을 클릭합니다.
- 이후에는 GitHub에 빈 저장소를 생성하고, 설정 메뉴의 **[리포지토리 게시 (Publish Repository)]** 기능을 사용하거나 터미널에서 `git remote add origin`으로 원격 저장소와 연동할 수 있습니다.

### 3) 커밋 & 푸쉬 (Commit & Push) 방법
- **언제 쓰나요?** 코드를 수정/저장한 뒤 변경 내역을 기록하고 원격 저장소에 업데이트할 때 사용합니다.
- **① 스테이징 (`+`)**: 수정된 파일 목록 옆의 **`+` (변경 사항 스테이징)** 버튼을 눌러 올릴 준비를 합니다. (`git add`)
- **② 커밋 (Commit)**: 상단 메시지 입력창에 작업 내용(예: "로그인 기능 추가")을 적고 **[커밋 (Commit)]** 버튼을 클릭해 기록을 남깁니다. (`git commit`)
- **③ 푸쉬 (Push)**: 파란색 **[변경 사항 동기화 (Sync Changes)]** 버튼을 클릭하여 커밋 기록을 클라우드에 전송합니다. (`git push`)
- 💡 **주의점**: 코드를 파일에서 고치고 저장(`Ctrl+S`) ⇨ `+` 버튼(스테이징) ⇨ Commit ⇨ Sync(Push) 까지 순서대로 완전히 끝내야만 GitHub 웹사이트에 최신본이 반영됩니다.

---

## 5. 필수 핵심 Git 명령어 백과사전

모든 명령어는 맨 앞에 `git` 키워드를 붙여서 사용합니다. (예: `git init`)

| 명령어 | 설명 |
|---|---|
| **`init`** | 현재 머물고 있는 로컬 폴더를 새로운 Git 저장소로 **초기화**합니다. (숨김 폴더 `.git` 생성) |
| **`clone`** | 남이 만든(또는 내 다른) 원격 저장소 프로젝트를 내 로컬 PC로 폴더째 **복사**해 가져옵니다. |
| **`add`** | 수정했거나 새로 만든 파일을 커밋하기 전에 대기열(스테이징 영역)에 **추가**합니다. |
| **`commit`** | 대기열에 있는 파일들의 상태를 묶어 찰칵! 영구적인 사진(버전 이력)으로 **저장(커밋)**합니다. |
| **`status`** | 현재 파일들이 어느 상태인지(빨간색: 안 담김, 초록색: 담김) **상태를 확인**합니다. |
| **`log`** | 지금까지 커밋한 이력표와 메시지들을 시간순으로 **조회**합니다. |
| **`branch`** | 원본 코드에 영향을 주지 않는 평행 우주(브랜치)를 **생성**하거나 **목록을 확인**합니다. |
| **`checkout`<br/>(또는 `switch`)** | 작업 중인 평행 우주(브랜치)를 **이동**하거나, 특정 과거의 커밋 시점으로 훌쩍 건너갑니다. |
| **`merge`** | 따로 작업하던 다른 브랜치의 변경 사항을 현재 내가 서 있는 브랜치로 흡수하여 **병합**합니다. |
| **`push`** | 로컬 PC에 커밋해둔(Commit) 소중한 변경점들을 GitHub 원격 저장소 공간으로 쏘아 **업로드**합니다. |
| **`pull`** | 원격 저장소에서 바뀐 내용(남이 올린 내용 등)을 끌어와서 내 PC 브랜치 기록에 확 **병합**시킵니다. |
| **`fetch`** | 원격 저장소에 뭐가 변했나 가져오기만 하고, 내 PC에 당장 합치거나(Merge) 덮어쓰지는 **않고 눈치만** 봅니다. |
| **`remote`** | 연결할 원격(GitHub) 저장소의 주소를 추가하거나 삭제하고 목록을 **관리**합니다. |
| **`reset`** | 타임머신 역할. 지정한 커밋 시점으로 강제 이동하며, 그 이후에 작업했던 이력을 **삭제(되돌림)**해버립니다. |
| **`revert`** | 이미 엎질러진 물(`push`까지 해버린 커밋)을 되돌리기 위해, 그 시점만 거스르는 **'취소용 반대 커밋'을 새로 생성**합니다. |
| **`help`** | 잘 모르는 명령어가 있을 때 세부 옵션과 사용 설명서를 **확인**합니다. (예: `git help commit`) |

### 🔗 유용한 참고 사이트
> - 초보자를 위한 Git과 GitHub 요약: [모두의연구소 블로그](https://modulabs.co.kr/blog/git-and-github-for-beginners)
> - Git 명령어 정리 및 치트시트: [개인 기술 블로그 모음(Tistory)](https://daengsik.tistory.com/58)
