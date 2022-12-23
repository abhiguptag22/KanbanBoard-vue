import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_security import Security, SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from application.models import User, Role
from flask_login import LoginManager
from flask_security import utils
from flask_cors import CORS
from flask_mail import Mail, Message

app = None
api = None

def create_app():
    app = Flask(__name__, template_folder="templates")
  
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    app.config['MAIL_SERVER']='smtp.mail.yahoo.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'abhigupta.g2@yahoo.com'
    app.config['MAIL_PASSWORD']  ''
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    db.init_app(app)
    mail = Mail(app)
    app.app_context().push()
    # Setup Flask-Security
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    # user_datastore.create_user(username="thejeshgn",email='i@thejeshgn.com', password=utils.hash_password('password'), active=1)
    # db.session.commit()    
    api = Api(app)
    CORS(app)
    db.create_all()
    app.app_context().push()      
    return app, api, mail

app,api, mail = create_app()


@app.route("/")
def index():
   msg = Message(
                'Hello',
                sender ='abhigupta.g2@yahoo.com',
                recipients = ['abhigupta.g22@gmail.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Sent'



# Import all the controllers so they are loaded
from application.controllers import *

# Add all restful controllers
#from application.api import ArticleLikesAPI
#api.add_resource(ArticleLikesAPI, "/api/article_likes", "/api/article_likes/<int:article_id>")


from application.api import TestAPI

api.add_resource(TestAPI, "/api/test")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(401)
def not_authorized(e):
    # note that we set the 403 status explicitly
    return jsonify(msg='unauthorised')



from application.api import Tasks, Lists, RemoveCard, RemoveList, EditCard
from application.api import EditList, allData, movingACard, Registrations, Logins
api.add_resource(Tasks, '/tasks')
api.add_resource(Lists, '/lists')
api.add_resource(RemoveCard, '/removecard/<int:id>')
api.add_resource(RemoveList, '/removelist/<title>')
api.add_resource(EditCard, '/editcard/<int:id>')
api.add_resource(EditList, '/editlist/<title>')
api.add_resource(allData, '/allData/<int:user_id>')
api.add_resource(movingACard, '/movecard/<int:id>/<to>')
api.add_resource(Registrations, '/signup')
api.add_resource(Logins, '/logins')





if __name__ == '__main__':
  # Run the Flask app
  app.run(
    debug=True
  )
