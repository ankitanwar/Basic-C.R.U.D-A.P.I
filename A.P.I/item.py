import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument(
            'price',
            type=float,                                                                                 
            required=True,                                      
            help="This filled cannot be empty",       
                                                
        )


    @jwt_required()
    def get(self,name): 
        item=Item.find_by_name(name)
        if item:
            return item
        else:
            return {"message":"item not found in the list"}

    @classmethod
    def find_by_name(cls,name):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="SELECT * FROM items WHERE name=?"
        res=cursor.execute(query,(name,))
        row=res.fetchone()
        connection.close()

        if row:
            return {"item":row[0],"price":row[1]}


    def post(self,name):
        if Item.find_by_name(name):
            return {"message":"Item already exist in the database"}
        data=Item.parser.parse_args()
        item_dict={"name":name,"price":data['price']}

        try:
            Item.insert(item_dict)
            return{"message":"Item has been added successfully"}
        except Exception as e:
            return {"message":"Some occur occured while inserting {}".format(e)}


    @classmethod
    def insert(cls,item_dict):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="INSERT INTO items values(?,?)"
        cursor.execute(query,(item_dict['name'],item_dict['price']))

        connection.commit()
        connection.close()


    def delete(self,name):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="DELETE FROM items WHERE name=?"

        cursor.execute(query,(name,))
        connection.commit()
        connection.close()

        return {"Message":"Item has been deleted successfully"}
    
    def put(self,name):
        data=Item.parser.parse_args()
        item_dict={"name":name,"price":data["price"]}
        item=Item.find_by_name(name)
        if item:
            try:
                Item.update_item(item_dict)
                return {"message":"Item has been updates successfully"}
            except Exception as e:
                return {"Message":"Some error has been occured while updating the item"}
        else:
            try:
                Item.insert(item_dict)
                return {"message":"Item has been added successfully"}
            except Exception as e:
                return {"message":"Some error has been occured while passing the data{}".format(e)}
    
    @classmethod
    def update_item(cls,item_dict):
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()

        query="UPDATE items SET price=? WHERE name=?"

        cursor.execute(query,(item_dict['price'],item_dict['name']))
        connection.commit()
        connection.close()

        return {"Message":"Item has been deleted successfully"}


class ItemList(Resource):   
    def get(self):             #this will return all the items in the dictonary
        connection=sqlite3.connect("data.db")
        cursor=connection.cursor()
        query="SELECT * FROM items "
        result=cursor.execute(query)
        items=[]
        for row in result:
            items.append({'name':row[0],"price":row[1]})
        return {"items":items}

        