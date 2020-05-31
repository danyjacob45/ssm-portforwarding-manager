from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy import create_engine

db = SQLAlchemy()


def init_app(app):
    db.app = app
    db.init_app(app)
    return db

def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.drop_all()
    db.metadata.create_all(engine)
    return engine



# Database Models
class SSMAgentList(db.Model):
    __tablename__ = 'ssmlist'
    profile = Column(String(30))
    instance_id = Column(String(30), primary_key=True)
    platform = Column(String(30))
    tag_name = Column(String(20))
    connect_port = Column(String(10))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def to_json(self):
        return {
            'profile' : self.profile,
            'instance_id': self.instance_id,
            'platform': self.platform,
            'tag_name':self.tag_name,
            'connect_port': self.connect_port,
            'updated_time': self.updated_time
        }
