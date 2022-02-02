## **`프로젝트 이름 : CodeWithUs(코드위드어스)`** 🖥️

## **`프로젝트 주제`**
알고리즘스터디의 참여도를 어찌하면 높일까?<br>
서로의 코드를 공유만 하지말고 댓글을달면서 피드백을 하면 좋지 않을까? <br>

알고리즘 스터디를 하면서 프로그래머스, 백준 등의 문제를 풀고 깃헙에 올리는 식만의 스터디를 진행했음.
자신의 코드를 올리고 서로다른 답안에 대해 커멘트를 남기고 문제 푼 인원 수를 파악하면서 참여율도 높이고  문제 난이도를 예상할 수 있다.<br>

### Stack
https://vanilla-nephew-d7a.notion.site/CodeWithUs-c728ee3dcf1e48a2a59ab7dc89ed8aa0

## **`엔드유저에게 보이는 웹서비스 타이틀 및 한 줄 소개`**
타이틀 : codewithus <br>
한 줄 소개 : 당신의 알고리즘 실력을 뽐내보세요!


## **`스토리보드 & 시나리오`**
- 피그마 활용

**User Flow Chart**<br>
<img width="1426" alt="figma" src="https://user-images.githubusercontent.com/63540952/151492372-e25d346e-c01e-4b8c-ab14-4d9a644e29f4.png">


- ERDCloud 활용
**ERD 구성**<br>
<img width="1218" alt="erd" src="https://user-images.githubusercontent.com/63540952/151492765-6ea74573-1167-4524-86d6-b975552d7c2c.png">

## 프로젝트 구성 - **`Front`**
### 화면구성
1. 메인화면 - main
2. 로그인창 - login
3. 회원가입 - signup
4. 파일리스트 - file_list
5. 문제 업로드 - problem_upload
6. 문제 리스트 - problem_list
7. 오늘의 문제 - todaty_exam
8. 풀이 리스트 - solutions


## 프로젝트 구성 - **`Database`**
DB Table 구성
1. algoritm
2. algoritm_image
3. cpmment
4. file
5. file_list
6. likes
7. member
8. solution
9. tag

## 프로젝트 구성 - **`BackEnd`**
1. 메인에서 각 화면 넘김(세션로그인시)
2. 회원가입 시 비밀번호 정해진 양식으로 만들어야하고 일치여부
3. 파일리스트에 업로드 시 파일 업로드
4. 파일리스트에서 파일 클릭시 다운로드
5. 문제업로드시 (캡쳐본)오늘의 문제에 출력
6. 문제 리스트(각 알고리즘 태그 부여)
7. 오늘의 문제에 대한 풀이를 구현시 텍스트형식이 아닌 코드형식으로 출력
8. 댓글기능 + 좋아요기능 비동기


### 1. 필요 기술 스택
**ver 1.0**
- 백엔드 기술스택 : Django, MariaDB, MySql, Uwsgi, 
- 고려가능 기술스택 : Docker, AWS
- 프론트엔드 기술스택 : Bootstrap, Jinja_template, HTML, CSS, ajax
- 버전관리 : git


### 2. 메인(MTB) 기능
   1. 
   2. 
   3. 

### 3. 서브 기능(구현 예정 목표)
   1. 배포
   2. 스터디모집 및 그룹 생성
   3. 비밀번호 찾기
   4. 문제정보 미리 저장소에 넣기
   

## **`프로젝트 팀원 역할 분담`**

| 이름   | 담당 업무                       |
| ------ | ------------------------------ |
| 서승우 |백엔드 & 프론트    |
| 이종혁 | 백엔드 & DB          |
| 안정우 | 백엔드 & 프론트   |
| 이반석 | 백엔드 & DB                 |
| 정희창 | 백엔드 & 프론트                 |






## 버전

- Codewith ver 1.0
## FAQ

- 자주 받는 질문 정리

