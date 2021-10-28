from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pymongo import MongoClient

from models import Base


def get_postgres_engine():

	username = 'mini_cpc'
	password = 'mini_cpc'
	host = 'localhost'
	port = 5432
	database = 'mini_cpc'
	DATABASE_URI = f'postgresql://{username}:{password}@{host}:{port}/{database}'
	engine = create_engine(DATABASE_URI)
	return engine


def init_postgress(engine):

	if not sqlalchemy.inspect(engine).has_table('raw_mini'):
		Base.metadata.tables["raw_mini"].create(bind=engine)

	if not sqlalchemy.inspect(engine).has_table('raw_tsi'):
		Base.metadata.tables["raw_tsi"].create(bind=engine)


def get_mongo_col():

	host = 'atm-dev.site'
	port = 11015
	database = 'mini_CPC'
	collection = 'data'
	client = MongoClient(host=host, port=port)
	db = client[database]
	col = db[collection]
	return col

col = get_mongo_col()


def fetch_raw_mini(dttm):

	result = col.find({"dttm": {"$gt": dttm}})
	data = []
	for x in result:
		x.pop('_id', None)
		data.append(x)
	return data


def fetch_raw_tsi(dttm):
	pass


def insert_data(engine, model, data):
	
	Session = sessionmaker(bind=engine)
	s = Session()
	for x in data:
		s.add(model(**x))
	s.commit()
	s.close()


def read_all(engine, model):

	Session = sessionmaker(bind=engine)
	s = Session()
	obj = s.query(model).all()
	s.close()
	return obj


def read_last_time(engine, model):

	Session = sessionmaker(bind=engine)
	s = Session()
	obj = s.query(model).order_by(model.id.desc()).first()
	s.close()
	return obj.dttm if obj else datetime(2021, 1, 1)
