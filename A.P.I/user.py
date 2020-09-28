import sqlite3
from flask_restful import Resource,reqparse

class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password

    @classmethod
    def find_by_username(cls,username):
        connection=sqlite3.connect('data.db')
        curosr=connection.cursor()

        insert_query="SELECT * FROM users WHERE username=?"
        res=curosr.execute(insert_query,(username,))  #dont forget to put comma to make it a tupple
        row=res.fetchone() 
        if row:
            ans=cls(*row)   
        else:
            ans= "result dosn't found in  the database"
        connection.close()
        return ans

    @classmethod
    def find_by_id(cls,_id):
        connection=sqlite3.connect('data.db')
        curosr=connection.cursor()

        insert_query="SELECT * FROM users WHERE id=?"
        res=curosr.execute(insert_query,(_id,))  #dont forget to put comma to make it a tupple
        row=res.fetchone() 
        if row:
            ans=cls(*row)
        else:
            ans= "result dosn't found in  the database"
        connection.close()
        return ans


class userRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument("username",
    type=str,
    required=True,
    help="please enter the valid name",
    )
    parser.add_argument("password",
    type=str,
    required=True,
    help="please enter the valid password",
    )
    def post(self):
        data=userRegister.parser.parse_args()

        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="INSERT INTO users VALUES (NULL,?,?) "

        cursor.execute(query,(data['username'],data['password']))
        connection.commit()
        connection.close()

        return {"message":"User created Successfully"}


