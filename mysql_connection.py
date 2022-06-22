import mysql.connector

def get_connection() :
    connection = mysql.connector.connect(
        host = 'yh-db.clmt07jbjcoe.ap-northeast-2.rds.amazonaws.com',
        database = 'movie_project_db',
        user = 'm_p_user',
        # 어드민 유저로 하면 안됨
        password = '1234'
    )
    return connection