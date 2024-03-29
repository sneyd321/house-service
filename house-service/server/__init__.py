from flask import Flask, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pymysql
pymysql.install_as_MySQLdb()

db = SQLAlchemy()
app = Flask(__name__)

from kazoo.client import KazooClient, KazooState

zk = KazooClient()



@app.route("/Health")
def health_check():
    return Response(status=200)


def create_app(env):
    #Create app
    global app
    config = Config(app)
    if env == "prod":
        app = config.productionConfig()
        
    elif env == "dev":
        app = config.developmentConfig()
    elif env == "test":
        app = config.testConfig()
    else:
        return 
    
    migrate = Migrate(app, db)
    db.init_app(app)
    zk.set_hosts(app.config["ZOOKEEPER"])
    zk.start()
    
    #Intialize modules
    from server.api.routes import house
    app.register_blueprint(house, url_prefix="/house/v1")
    return app