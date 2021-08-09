import os
from flask import Flask, request,jsonify
from flask_restful import Resource,Api
from secure_check import authenticate,identify
from flask_jwt import JWT,jwt_required

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)


app.config['SECRET_KEY']='mysecretkey'


basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
Migrate(app,db)
jwt=JWT(app,authenticate,identify)
api=Api(app)
class Pupppy(db.Model):
	name=db.Column(db.String(80),primary_key=True)
	def __init__(self,name):
		self.name=name

	def json(self):
		return {'name':self.name}



class Puppy(Resource):
	def get(self,name):
		pup=Pupppy.query.filter_by(name=name).first()

		if pup:
			return pup.json()
		else:
			return {'name':None},404
	def post(self,name):
		pup=Pupppy(name)
		db.session.add(pup)
		db.session.commit()
		return pup.json()
	def delete(self,name):
		pup=Pupppy.query.filter_by(name=name).first()
		db.session.delete(pup)
		db.session.commit()
		return {"Note": 'delete success'}

class All(Resource):
#	@jwt_required()
	def get(self):
		puppies=Pupppy.query.all()	
		return [pup.json() for pup in puppies]
api.add_resource(Puppy,'/puppy/<string:name>')
api.add_resource(All,'/puppies')

if(__name__=='__main__'):
	app.run(debug=True)
