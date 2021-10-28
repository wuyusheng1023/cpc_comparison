from datetime import datetime, timedelta
import requests


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


class SmearApiData:
    def __init__(self, var, start_dttm, end_dttm, table="KUM_META",
                 quality="ANY", averaging="NONE", typeof="ARITHMETIC"):
        columns = list(var.keys())
        self.columns = columns
        self.table = table
        var = list(var.values())
        tablevariable = [f'{self.table}.{v}' for v in var]
        self.tablevariable = "&".join(tablevariable)
        self.start_dttm = start_dttm
        self.end_dttm = end_dttm
        self.quality = quality
        self.averaging = averaging
        self.typeof = typeof
        self.fetch_data()

    def get_data(self):
        return self._data

    def dt_fmt(self, dt):
        year = dt.year
        month = str(dt.month).rjust(2, '0')
        day = str(dt.day).rjust(2, '0')
        hour = str(dt.month).rjust(2, '0')
        minute = str(dt.month).rjust(2, '0')
        second = str(dt.month).rjust(2, '0')
        microsecond = str(dt.microsecond)[:3]
        text = f'{year}-{month}-{day}T{hour}%3A{minute}%3A{second}.{microsecond}'
        return text

    def create_url(self):
        url = "https://smear-backend.rahtiapp.fi/search/timeseries"
        tablevariable = '='.join(['tablevariable', self.tablevariable])
        start = self.dt_fmt(self.start_dttm)
        start = '='.join(['from', start])
        end = self.dt_fmt(self.end_dttm)
        end = '='.join(['to', end])
        quality = '='.join(['quality', self.quality])
        averaging = '='.join(['averaging', self.averaging])
        typeof = '='.join(['type', self.typeof])
        params = '&'.join(
            [tablevariable, start, end, quality, averaging, typeof])
        return '?'.join([url, params])

    def fetch_data(self):
        url = self.create_url()
        resp = requests.get(url)
        data = resp.json()['data']
        self._data = data


def clean_smear_data(data):
    cleaned_data = []
    for x in data:
        dttm = datetime.strptime(x['samptime'], '%Y-%m-%dT%H:%M:%S.%f')
        cleaned_data.append(
            {
                'dttm': dttm,
                'conc': x['KUM_META.cn']
            }
        )
    return cleaned_data


def fetch_raw_tsi(dttm):

	start_dttm = dttm + timedelta(milliseconds=100000)
	end_dttm = datetime.utcnow() + timedelta(hours=3)
	var = {'Ntot': 'cn'}
	table = 'KUM_META'
	smear = SmearApiData(var=var, start_dttm=start_dttm, end_dttm=end_dttm, table=table)
	data = smear.get_data()
	return clean_smear_data(data)


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
	return obj.dttm if obj else datetime(2021, 10, 24)
