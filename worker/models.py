from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Float


Base = declarative_base()


class RawMini(Base):
	__tablename__ = 'raw_mini'
	id = Column(Integer, primary_key=True)
	dttm = Column(DateTime)
	conc = Column(Float)
	volt = Column(Float)
	Ts = Column(Float)
	Tc = Column(Float)
	To = Column(Float)
	flow = Column(Float)

	def __repr__(self):
		return f"<RawMini({self.id}, {self.dttm}, {self.conc})>"


class RawTsi(Base):
	__tablename__ = 'raw_tsi'
	id = Column(Integer, primary_key=True)
	dttm = Column(DateTime)
	conc = Column(Float)

	def __repr__(self):
		return f"<RawMini({self.id}, {self.dttm}, {self.conc}>"
