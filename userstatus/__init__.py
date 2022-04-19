from flask import Flask
import peewee as pw

app = Flask(__name__)

if app.config['ENV'] == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


pg_db = pw.PostgresqlDatabase(app.config['GRES_DATABASE'], user=app.config['GRES_USER'],
                              password=app.config['GRES_PASSWORD'],host=app.config['GRES_HOST'],
                              port=app.config['GRES_PORT'])

from userstatus import views