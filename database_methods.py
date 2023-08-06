from dotenv import load_dotenv
import psycopg2
import os


# To manage the database connection
def manage_connection(query: str, type: str) :
    load_dotenv()
    db_pass = os.getenv('DB_PASS')
    connection = None
    try : 
        connection = psycopg2.connect(
            database="railway",
            user='postgres',
            password=db_pass,
            host='containers-us-west-180.railway.app', 
            port='5575'
        )

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                if type != "select" :
                    connection.commit()
                else :
                    return cursor.fetchall()
    except Exception as e :
        print(e)
    finally :
        if connection != None:
            connection.close()

            
def add_to_favorites_method(user_id: int, joke_id: int) -> None:
    query = f"""
            INSERT INTO favorite_jokes (user_id, joke_id)
            VALUES ({user_id}, '{joke_id}')
            """
    manage_connection(query, "insert")

def delete_from_favorites_method(user_id: int, joke_id: int) -> None:
    query = f'''
            DELETE FROM favorite_jokes
            WHERE user_id = {user_id} AND joke_id = {joke_id}
            '''
    manage_connection(query, "delete")
    
def get_favorites_method(user_id: int) -> list[int]:
    query = f'''
            SELECT joke_id FROM favorite_jokes
            WHERE user_id = {user_id}
            '''
    fav_jokes_id = [row[0] for row in manage_connection(query, 'select')]
    return fav_jokes_id

def is_not_in_favorites(joke_id: int, user_id: int) -> bool:
    query = f'''
        SELECT joke_id FROM favorite_jokes
        WHERE joke_id = {joke_id} AND user_id = {user_id}
        '''
    query_result = manage_connection(query, "select")
    return  query_result == []