from time import sleep

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
dttm_raw_mini = read_last_time(engine, RawMini)
dttm_raw_tsi = read_last_time(engine, RawTsi)


if __name__ == '__main__':
	while True:
		try:
			data = fetch_raw_mini(dttm_raw_mini)
			insert_data(engine, RawMini, data)
			dttm_raw_mini = read_last_time(engine, RawMini)
			print(f"Raw mini data update to {dttm_raw_mini}")

			data = fetch_raw_tsi(dttm_raw_tsi)
			insert_data(engine, RawTsi, data)
			dttm_raw_tsi = read_last_time(engine, RawTsi)
			print(f"Raw TSI data update to {dttm_raw_tsi}")

			for i in range(60):
				sleep(1)
				if i % 10 == 0:
					print(f'fetch raw data again in {60-i} sec')
		except:
			print("failed in fetching data")
			sleep(300)
