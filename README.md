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

1. api 경로 설계
2. 소스코드

# 추가
테이블의 컬럼이름을 헝가리안 표기법으로 하겠습니다

created_at => createdAt

이렇게 하는이유??
안드로이드 개발할때, 개발 편의성 때문
어떤건 _ 이고 어떤건 헝가리안 이라면 혼선이 온다

### rating 컬럼에 index 추가
> - index 추가하면 데이터베이스 성능이 빨라진다

### 목록을 가져오는 API
> - 페이징처리를 해줘야한다

### 영화명 검색하는 API
> - 쿼리에 avg 같은 float 은 제이슨에서 읽도록 변경 시켜줘야 한다(for문 으로)

### 'mySQL 접속위한 유저 만들기'의 코드
> use mysql;
>
> -- mySQL 접속위한 유저 만들기
> create user 'm_p_user'@'%' identified by '1234';
>					-- '%' => 네트워크 통해서 접속가능하게 하겠다
> 
> grant all on movie_project_db.* to 'm_p_user'@'%';
> -- grant all on
> -- 모든 권한을 주겠다
> -- 모든권한을 준다 momo_db의 *(모든것)에 to 'memo_user' 에다가

### mysql 테이블 생성문 만들기
> -- 테이블생성문 만들고싶으면
> -- 테이블 우측마우스 > 카피 투 테이블 > 크리에잇 스테이트먼트
> -- ex)
> -- CREATE TABLE `likes` (
> --   `id` int unsigned NOT NULL AUTO_INCREMENT,
> --   `postingId` int DEFAULT NULL,
> --   `userId` int DEFAULT NULL,
> --   PRIMARY KEY (`id`)
> -- ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

### 좋아요테이블 만들때
두개다 유니크설정하려면
mysql 테이블 설정에 index로 가서 두가지 컬럼다 같이 유니크설정 하는것


# 영화실시간 추천
- 큰 구조가
> 1. df 데이터프레임을 어떻게 만드느냐 => 디비에서 바로 가져오기
>> df를 파일로 가져오는 방법도 있지만 하지말고
>> 디비에서 데이터프레임 만들걸 불러와서 그걸 df로 저장하고
>> 상관계수 뽑는 구조에 대입함
>> 그럼 ! csv파일 만드는거랑 똑같음
> 2. 내 별점정보를 디비에서 바로 가져오기
> 3. 두가지 데이터로 추천(상관계수) 작업
