from http import HTTPStatus
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from mysql.connector.errors import Error
from mysql_connection import get_connection
import mysql.connector

import pandas as pd
import numpy as np

class MovieRecomResource(Resource) :
    @jwt_required()
    def get(self) :
        
        # 1. 클라이언트로 부터 데이터를 받아온다.
        user_id = get_jwt_identity()

        # 2. 추천을 위한 상관계수 데이터프레임 읽어온다.
        df = pd.read_csv('data/movie_correlations.csv', index_col= 'title')
        # print(df)
        
        # 3. 이 유저의 별점 정보를, 디비에서 가져온다.

         # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            query = '''select r.userId, r.movieId, r.rating, m.title
                    from rating r
                    join movie m
                    on r.movieId = m.id and r.userId = %s;'''
            
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

        # 디비로 부터 가져온, 내 별점 정보를, 데이터프레임으로 만들어준다
        df_my_rating = pd.DataFrame(data= result_list)

        # 추천 영화를 저장할, 빈 데이터 프레임 만든다.
        similar_movie_list = pd.DataFrame()

        for i in range( len(df_my_rating) ) :
            similar_movie = df[df_my_rating['title'][i]].dropna().sort_values(ascending= False).to_frame()
            similar_movie.columns = ['Correlation']
            similar_movie['Weight'] = df_my_rating['rating'][i] * similar_movie['Correlation']
            similar_movie_list = similar_movie_list.append(similar_movie)

        # 영화 제목이 중복된 영화가 있을 수 있다.
        # 중복된 영화는, Weight 가 가장 큰(max)값으로 해준다.
        similar_movie_list.reset_index(inplace= True)

        similar_movie_list = similar_movie_list.groupby('title')['Weight'].max().sort_values(ascending= False)

        # 내가 이미 봐서, 별점을 남긴 영화는 여기서 제외해야 한다.

        #print(similar_movie_list)
        
        similar_movie_list = similar_movie_list.reset_index()

        # 내가 이미 본 영화 제목만 가져온다.
        title_list = df_my_rating['title'].tolist()

        # similar_movie_list 에 내가 본 영화인 title_list 를
        # 제외하고 가져온다

        print(similar_movie_list)
        print(title_list)

        recomn_movie_list = similar_movie_list.loc[ ~similar_movie_list['title'].isin(title_list) , ]
                            # ~ 은 반대되는걸 가져와라 => 이번건 Flase
        print(recomn_movie_list.iloc[ 0 : 19+1 , ])

        return { "result" : "success" ,
            'movie_list' : recomn_movie_list.iloc[ 0 : 19+1 , ].to_dict('records')
                                                                    # records 는 문법, 쓰면 json 형식으로 만들어주겠다
             }, 200

# 실시간 영화 추천
class MovieRecomRealTimeResource(Resource) :
    @jwt_required()
    def get(self) :

        # 1. 클라이언트로부터 데이터를 받아온다.
        user_id = get_jwt_identity()

        # 2. 추천을 위한 상관계수를 위해, 데이터베이스에서 데이터를 먼저 가져온다.

            
        # 3. 이 유저의 별점 정보를, 디비에서 가져온다.

         # 디비로부터 데이터를 받아서 ,클라이언트에 보내준다.
        try :
            # 데이터 업데이트
            connection = get_connection()

            # 실시간으로 가져와서 데이터프레임 만드는 쿼리
            ###
            query = '''select m.title, r.movieId, r.rating, r.userId
                    from movie m
                    join rating r
                    on m.id = r.movieId;'''
            
            # record = (user_id, )

            # select 문은, dictionary = True 를 해준다.
            cursor = connection.cursor(dictionary = True)

            # 실행
            cursor.execute(query)

            # select 문은, 아래 함수를 이용해서, 데이터를 가져온다.
            result_list = cursor.fetchall()

            df = pd.DataFrame(data= result_list)
            # 피봇  테이블한후, 상관계수를 뽑는다
            matrix = df.pivot_table(values= 'rating',index= 'userId', columns= 'title')
            # 영화별로 50개 이상의 리뷰있는 영화만 상관계수 계산
            df = matrix.corr(min_periods= 50)

            ###

            query = '''select r.userId, r.movieId, r.rating, m.title
                    from rating r
                    join movie m
                    on r.movieId = m.id and r.userId = %s;'''
            
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

        # 디비로 부터 가져온, 내 별점 정보를, 데이터프레임으로 만들어준다
        df_my_rating = pd.DataFrame(data= result_list)

        # 추천 영화를 저장할, 빈 데이터 프레임 만든다.
        similar_movie_list = pd.DataFrame()

        for i in range( len(df_my_rating) ) :
            similar_movie = df[df_my_rating['title'][i]].dropna().sort_values(ascending= False).to_frame()
            similar_movie.columns = ['Correlation']
            similar_movie['Weight'] = df_my_rating['rating'][i] * similar_movie['Correlation']
            similar_movie_list = similar_movie_list.append(similar_movie)

        # 영화 제목이 중복된 영화가 있을 수 있다.
        # 중복된 영화는, Weight 가 가장 큰(max)값으로 해준다.
        similar_movie_list.reset_index(inplace= True)

        similar_movie_list = similar_movie_list.groupby('title')['Weight'].max().sort_values(ascending= False)

        # 내가 이미 봐서, 별점을 남긴 영화는 여기서 제외해야 한다.

        #print(similar_movie_list)
        
        similar_movie_list = similar_movie_list.reset_index()

        # 내가 이미 본 영화 제목만 가져온다.
        title_list = df_my_rating['title'].tolist()

        # similar_movie_list 에 내가 본 영화인 title_list 를
        # 제외하고 가져온다

        print(similar_movie_list)
        print(title_list)

        recomn_movie_list = similar_movie_list.loc[ ~similar_movie_list['title'].isin(title_list) , ]
                            # ~ 은 반대되는걸 가져와라 => 이번건 Flase를 가져와라
        print(recomn_movie_list.iloc[ 0 : 19+1 , ])

        return { "result" : "success" ,
            'movie_list' : recomn_movie_list.iloc[ 0 : 19+1 , ].to_dict('records')
                                                                    # records 는 문법, 쓰면 json 형식으로 만들어주겠다
             }, 200

        