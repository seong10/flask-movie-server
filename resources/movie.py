from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class MovieListResource(Resource) :
    def get(self) :
        # 1. 클라이언트로 부터 데이터 받아온다.
        # ?offset:0&limit:25
        offset = request.args['offset']
        limit = request.args['limit']
        order = request.args['order']

        # ## 유저토큰으로 부터 user_id 반환
        # user_id = get_jwt_identity()

        # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select m.id, m.title,
                    count(r.movieId) as cnt, ifnull(avg(r.rating), 0) as avg
                    from movie m
                    left join rating r
                    on m.id = r.movieId
                    group by m.id
                    order by '''+order+''' desc
                    limit '''+offset+''', '''+limit+''';'''
            # record = (user_id, )

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            # 실행
            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요! 디비에서 가져온 timestamp 난
            # 파이썬의 datetime 으로 자동 변경된다.
            # json은 datetime 같은게 없다 그냥 문자열이다
            # 문제는! 이 데이터를 json 으로 바로 보낼 수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            i = 0
            for record in result_list :
                result_list[i]['avg'] = float(record['avg'])
                i = i + 1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return { "result" : "success" ,
            'count' : len(result_list),
            "items" : result_list }, 200

class MovieResource(Resource) :
    def get(self, movie_id) :

        # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select m.*, 
                    count(r.movieId) as cnt, ifnull(avg(r.rating), 0) as avg
                    from movie m
                    left join rating r
                    on m.id = r.movieId
                    where m.id = %s
                    group by m.id ;'''
            record = (movie_id, )

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            # 실행
            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요! 디비에서 가져온 timestamp 난
            # 파이썬의 datetime 으로 자동 변경된다.
            # json은 datetime 같은게 없다 그냥 문자열이다
            # 문제는! 이 데이터를 json 으로 바로 보낼 수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            i = 0
            for record in result_list :
                result_list[i]['avg'] = float(record['avg'])
                result_list[i]['year'] = record['year'].isoformat()
                result_list[i]['createdAt'] = record['createdAt'].isoformat()
                i = i + 1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return { "result" : "success" ,
            'count' : len(result_list),
            "items" : result_list }, 200

class MovieRatingResource(Resource) :
    def get(self, movie_id) :
        
        # 1. 클라이언트로부터 데이터를 가져온다
        # ?offset=0&limit=25

        offset = request.args['offset']
        limit = request.args['limit']

        # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select u.name, u.gender, r.rating
                    from rating r
                    join movie m
                    on r.movieId = m.id and m.id = %s
                    join user u
                    on r.userId = u.id
                    limit '''+offset+''', '''+limit+''';'''
            record = (movie_id, )

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            # 실행
            cursor.execute(query, record)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요! 디비에서 가져온 timestamp 난
            # 파이썬의 datetime 으로 자동 변경된다.
            # json은 datetime 같은게 없다 그냥 문자열이다
            # 문제는! 이 데이터를 json 으로 바로 보낼 수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            # i = 0
            # for record in result_list :
            #     result_list[i]['avg'] = float(record['avg'])
            #     result_list[i]['year'] = record['year'].isoformat()
            #     result_list[i]['createdAt'] = record['createdAt'].isoformat()
            #     i = i + 1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return { "result" : "success" ,
            'count' : len(result_list),
            "items" : result_list }, 200

class MoiveSearchResource(Resource) :
    def get(self) :
        # 1. 클라이언트로부터 데이터를 가져온다
        # ?keyword=hello&offset=0&limit=25

        keyword = request.args['keyword']
        offset = request.args['offset']
        limit = request.args['limit']

        # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select m.title, count(r.movieId) as cnt, ifnull(avg(r.rating), 0) as avg
                    from movie m
                    join rating r
                    on m.id = r.movieId
                    where m.title like '%'''+keyword+'''%'
                    group by m.id
                    limit '''+offset+''', '''+limit+''';'''
            # record = (movie_id, )

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            # 실행
            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            print(result_list)

            # 중요! 디비에서 가져온 timestamp 난
            # 파이썬의 datetime 으로 자동 변경된다.
            # json은 datetime 같은게 없다 그냥 문자열이다
            # 문제는! 이 데이터를 json 으로 바로 보낼 수 없으므로,
            # 문자열로 바꿔서 다시 저장해서 보낸다.
            i = 0
            for record in result_list :
                result_list[i]['avg'] = float(record['avg'])
                i = i + 1

            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()

            return {"error" : str(e), 'error_no' : 20}, 503

        return { "result" : "success" ,
            'count' : len(result_list),
            "items" : result_list }, 200

