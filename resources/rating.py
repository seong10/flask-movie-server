from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

class RatingListResource(Resource) :
    @jwt_required()
    def post(self) :

        # 1. 클라이언트로부터 데이터를 받아온다.
        # {
        #     "movieId": "32",
        #     "rating": 4
        # }

        data = request.get_json()
        user_id = get_jwt_identity()

        # 2. 디비에 insert

        try :
            # 1. DB에 연결
            connection = get_connection()
         
            # 2. 쿼리문 만들기
            query ='''insert into rating
                    (userId, movieId, rating)
                    values
                    ( %s, %s, %s);'''

            record = (user_id, data['movieId'], data['rating'])

            # 3. 커서를 가져온다.
            cursor = connection.cursor()

            # 4. 쿼리문을 커서를 이용해서 실행한다
            # 실행
            cursor.execute(query, record)

            # 5. 커넥션을 커밋해줘야한다 => 디비에 영구적으로 반영하는것
            connection.commit()

            # 6. 자원 해제
            cursor.close()
            connection.close()

        except mysql.connector.Error as e :
            print(e)
            cursor.close()
            connection.close()
            return {"error" : str(e), 'error_no' : 3}, 503

        return {'result' : 'success'}, 200

    @jwt_required()
    def get(self) :

        # 1. 클라이언트로부터 데이터를 가져온다
        # ?offset=0&limit=25

        offset = request.args['offset']
        limit = request.args['limit']
        user_id = get_jwt_identity()

        # 2. 내 리뷰리스트를 디비에서 가져온다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select m.title, r.rating
                    from rating r
                    join movie m
                    on r.movieId = m.id and r.userId = %s
                    limit '''+offset+''', '''+limit+''';'''
            record = (user_id, )

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