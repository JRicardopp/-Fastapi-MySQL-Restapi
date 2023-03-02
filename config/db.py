from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymytsql://root:12020191@localhost:3306/crudb")

conn = engine.connect()