import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey

# import all, though we're gonna be using only half of these 
from sqlalchemy.dialects.postgresql import \
    ARRAY, BIGINT, BIT, BOOLEAN, BYTEA, CHAR, CIDR, DATE, \
    DOUBLE_PRECISION, ENUM, FLOAT, HSTORE, INET, INTEGER, \
    INTERVAL, JSON, JSONB, MACADDR, NUMERIC, OID, REAL, SMALLINT, TEXT, \
    TIME, TIMESTAMP, UUID, VARCHAR, INT4RANGE, INT8RANGE, NUMRANGE, \
    DATERANGE, TSRANGE, TSTZRANGE, TSVECTOR

import json

with open('sensitive_data.json', newline='') as file:
    global config
    config = json.file.read()

def connect():
    return connect_to_db(config["db-user"], config["db-password"], config["db-name"], config["db-host"], config["db-port"])

# from https://suhas.org/sqlalchemy-tutorial
def connect_to_db(user, password, db, host='localhost', port=5432):
    '''Returns a connection and a metadata object'''
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    con = sqlalchemy.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta = sqlalchemy.MetaData(bind=con, reflect=True)

    return con, meta

con, meta = connect()

# 1-to-1 relation with registration. This may have multiple duplicate entries
participant = Table('participant', meta,
    Column('id', INT, primary_key=True),
    Column('email', VARCHAR(50)),
    Column('phone_number', VARCHAR(50)), #phone numbers can have hyphens and spaces too, we'll do a check for this in code. Backend and frontend must be consistent.
    Column('name', VARCHAR(50))
)

event = Table('event', meta,
    Column('id', VARCHAR(50), primary_key=True),
    Column('name', VARCHAR(50)),
    Column('team_size', SMALLINT)
)

# one to many mapping
registration_participant = Table('registration_participant', meta,
    Column('registration_id', INT,  ForeignKey("registration.id")),
    Column('participant_id', INT,  ForeignKey("participant.id"))
)

registration = Table('registration', meta,
    Column('id', INT, primary_key=True),
    Column('captain', INT, ForeignKey("participant.id")),
    Column('team_name', VARCHAR(50))
    Column('data', JSON)
)

meta.create_all()

"""
Todo
 - schema
 - forms and insert queries
 - form generation
"""