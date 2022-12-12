from flask_restful import Resource, Api
from flask_restful import fields, marshal
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError
#from application.models import ArticleLikes
from application.database import db
from flask import current_app as app
import werkzeug
from flask import abort, request, jsonify
from datetime import date, datetime
from flask_security import auth_required, login_required, roles_accepted, roles_required, auth_token_required
from application.models import Cards, Listss, User

'''article_likes_resource_fields = {
    'user_id':   fields.Integer,
    'article_id':    fields.String,
}

create_article_likes_parser = reqparse.RequestParser()
create_article_likes_parser.add_argument('user_id')
create_article_likes_parser.add_argument('article_id')

class ArticleLikesAPI(Resource):
    @auth_required("token")
    def post(self):
        args = create_article_likes_parser.parse_args()
        article_id = args.get("article_id", None)
        user_id = 1 # current user
        # Do all the validation
        new_like = ArticleLikes(user_id=user_id, article_id=article_id)
        db.session.add(new_like)
        db.session.commit()
        return marshal(new_like, article_likes_resource_fields)'''


test_api_resource_fields = {
    'msg':    fields.String,
}

class TestAPI(Resource):
    @auth_required("token")
    def get(self):
        return marshal({"msg":"Hello World"}, test_api_resource_fields)

class Lists(Resource):
    def get(self):
        data = Listss.query.all()
        j_data = [each.toDict() for each in data]
        return jsonify(j_data)
    def post(self):
        data = request.get_json()
        #print(data)
        title = data['newList']
        user_id = data['current_user_id']
        newList = Listss(title=title, user_id=user_id)
        db.session.add(newList)
        db.session.commit()
        return str(data), 201

class Tasks(Resource):
    def get(self):
        data = Cards.query.all()
        j_data = [each.toDict() for each in data]
        return jsonify(j_data)
    def post(self):
        data = request.get_json()
        #print(data)
        content = data['content']
        deadline = data['deadline']
        parent = data['taskParent']
        user_id = data['current_user_id']
        print(type(deadline))
        createdOn = str(datetime.now())[:10]
        newCard = Cards(content=content, deadline=deadline, createdOn=createdOn, parentList=parent, user_id=user_id)
        db.session.add(newCard)
        db.session.commit()
        return str(data), 201

class Registrations(Resource):
    def post(self):
        data = request.get_json()
        if (data['name'] and data['email'] and data['password']):
            already_exists = User.query.filter_by(email=data['email']).first()
            if ( not already_exists):
                newUser = User(name=data['name'], email=data['email'], password=data['password'])
                db.session.add(newUser)
                db.session.commit()
                return jsonify({"msg":"Registration successful"})
            else:
                return jsonify({"msg":"email already exists"})
        else:
            return jsonify({"msg":"Registration not successful"})

class Logins(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        if (email and password):
            aUser = User.query.filter_by(email=email, password=password).first()
            if aUser:
                return
                #return jsonify(msg="login success", access_token=access_token)
            else:
                return jsonify({"msg":"wrong email/password"})
        else:
            return jsonify({"msg":"login failed"})

class RemoveCard(Resource):
    def get(self, id):
        card = Cards.query.filter_by(id=id).first()
        db.session.delete(card)
        db.session.commit()

class EditCard(Resource):
    def post(self, id):
        card = Cards.query.filter_by(id=id).first()
        data = request.get_json()
        newContent = data['newContent']
        card.content = newContent
        db.session.commit()

class RemoveList(Resource):
    def get(self, title):
        aList = Listss.query.filter_by(title=title).first()
        allCards = Cards.query.filter_by(parentList=title).all()
        db.session.delete(aList)
        for each_card in allCards:
            db.session.delete(each_card)
        db.session.commit()

class EditList(Resource):
    def post(self, title):
        aList = Listss.query.filter_by(title=title).first()
        data = request.get_json()
        newListName = data['newListName']
        aList.title = newListName
        allCards = Cards.query.filter_by(parentList=title).all()
        for each_card in allCards:
            each_card.parentList=newListName
        db.session.commit()

class allData(Resource):
    def get(self, user_id):
        allLists = Listss.query.filter_by(user_id=user_id)
        res = []
        for each in allLists:
            tname = each.title
            allCards = Cards.query.filter_by(parentList=tname, user_id=user_id).all()
            allCardsjson = [each.toDict() for each in allCards]
            #print(allCardsjson)
            res.append({"name":tname, "value":allCardsjson})
        return res

class movingACard(Resource):
    def post(self, id, to):
        theCard = Cards.query.filter_by(id=id).first()
        theCard.parentList = to.strip()
        db.session.commit()
        return

