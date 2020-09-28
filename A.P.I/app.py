from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from user import userRegister
from item import ItemList,Item

app=Flask(__name__)
app.secret_key="secret key"   
api=Api(app)

jwt=JWT(app,authenticate,identity)

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(userRegister,"/register")


if __name__=='__main__':
    app.run(debug=True)