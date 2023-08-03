import psycopg2

# is to manage the database connection
def manage_connection(query, type) :
    connection = None
    try : 
        connection = psycopg2.connect(
            database="railway", #your database name
            user='postgres',
            password='zRC4WwSp8qqgzlrXc3dm',
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
    query = f"""
            INSERT INTO favorite_jokes (joke_text)
            VALUES ('{joke}')
            """
    manage_connection(query, "insert")

def delete_from_favorites_method(joke):
    query = f'''
            DELETE FROM menu_items 
            where item_name = "{joke}"
            '''
    manage_connection(query, "delete")


if __name__ == '__main__':
    add_to_favorites_method("test joke 2")