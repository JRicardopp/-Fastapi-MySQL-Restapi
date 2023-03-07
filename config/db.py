from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:12020191@localhost:3306/crudb")

meta = MetaData()

conn = engine.connect()


