import os
from flask import Flask, g
from .config import *
from .db import get_db

def create_app():

   app = Flask(__name__)
   app.config.from_object(__name__)


   @app.route('/')
   def mojee():
      return 'Welcome to mojee!'


   @app.before_request
   def before_request():
      g.db = get_db()


   @app.teardown_request
   def teardown_request(err):
      if err:
         app.logger.info(err)
      database = getattr(g, 'db', None)
      if database is not None:
         database.close()


   @app.errorhandler(404)
   def image_not_found(err):
      if err:
         app.logger.info(err)
      return {'status': 404}


   if __name__ == '__main__':
      app.run(debug=True)


   from . import db
   db.init_app(app)

   with app.app_context():
       from . import images
       app.register_blueprint(images.bp)
       app.add_url_rule('/', endpoint='index')

   return app
