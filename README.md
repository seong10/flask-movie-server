# movie_project_api

# 순서
1. DB생성
> - 1. mySQL workbench 에서 서버를 생성한다
> - 2. 서버의 테이블을 설계한다
> - 3. 테이블안에 데이터를 insert 한다

2. API 설계
> - 1. app.py 메인파일 기본 구조 설계
> - 2. config, utils, connection 파일 가져오고
> - 3. DB에서 mySQL 접속위한 유저 만들기 !!!중요!!!
> - 4. 만들고자 하는 기능의 구조설계
> - 5. 메인파일에서 경로설정
> - 6. 기능 개발

3. 기능 개발 순서
> - 1. 개발했었던 구조 가져오기
> - 2. 쿼리문 DB에서 테스트 코드하기

# 추가
테이블의 컬럼이름을 헝가리안 표기법으로 하겠습니다

created_at => createdAt

이렇게 하는이유??
안드로이드 개발할때, 개발 편의성 때문
어떤건 _ 이고 어떤건 헝가리안 이라면 혼선이 온다

### rating 컬럼에 index 추가
index 추가하면 데이터베이스 성능이 빨라진다
