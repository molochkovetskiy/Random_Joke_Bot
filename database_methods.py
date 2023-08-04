import psycopg2
from dotenv import load_dotenv
import os



# is to manage the database connection
def manage_connection(query, type) :
    load_dotenv()
    db_pass = os.getenv('DB_PASS')
    connection = None
    try : 
        connection = psycopg2.connect(
            database="railway", #your database name
            user='postgres',
            password=db_pass,
            host='containers-us-west-180.railway.app', 
            port='5575'
        )

        with connection:
            with connection.cursor() as cursor: #it closes the transaction
                cursor.execute(query)
                if type != "select" :
                    connection.commit()
                else :
                    return cursor.fetchall()
    except Exception as e :
        print(e)
    finally :
        if connection != None:
            connection.close() #need to specificaly closed the connection
            
            
def add_to_favorites_method(joke):
    joke = joke.replace("'", "''")
    query = f"""
            INSERT INTO favorite_jokes (joke_text)
            VALUES ('{joke}')
            """
    manage_connection(query, "insert")

def delete_from_favorites_method(joke):
    query = f'''
            DELETE FROM favorite_jokes 
            where joke_text = "{joke}"
            '''
    manage_connection(query, "delete")
    
def get_favorites_method():
    query = f'''
            SELECT joke_text FROM favorite_jokes
            '''
    # row_fav_jokes = manage_connection(query, 'select')
    fav_jokes = [row[0] for row in manage_connection(query, 'select')]
    return fav_jokes
    # return fav_jokes
    # yield somehow each element and messege it???


if __name__ == '__main__':
    add_to_favorites_method("test joke 2")