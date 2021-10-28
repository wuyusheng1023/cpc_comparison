from time import sleep
from datetime import datetime

from sqlalchemy.orm import session

from models import RawMini, RawTsi
from utils import (
	get_postgres_engine,
	init_postgress,
	fetch_raw_mini,
	fetch_raw_tsi,
	insert_data,
	read_last_time,
)


engine = get_postgres_engine()
init_postgress(engine)


if __name__ == '__main__':
	dttm_raw_mini = read_last_time(engine, RawMini)
	result = fetch_raw_mini(dttm_raw_mini)
	insert_data(engine, RawMini, result)
	print(f"Raw mini data update to {dttm_raw_mini}")

	dttm_raw_tsi = read_last_time(engine, RawTsi)
