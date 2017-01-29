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
    config = json.loads(file.read())

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

print(meta)

def create_all_tables():
    #meta.drop_all()
    # 1-to-1 relation with registration. This may have multiple duplicate entries
    participant = Table('participant', meta,
        Column('id', INTEGER, primary_key=True),
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
        Column('registration_id', INTEGER,  ForeignKey("registration.id")),
        Column('participant_id', INTEGER,  ForeignKey("participant.id"), primary_key=True)
    )

    registration = Table('registration', meta,
        Column('id', INTEGER, primary_key=True),
        Column('event_id', VARCHAR(50), ForeignKey("event.id")),
        Column('captain', INTEGER, ForeignKey("participant.id")),
        Column('team_name', VARCHAR(50)), #nullable, because team size can be 1
        Column('data', JSON)
    )
    #meta.create_all()

participant = Table('participant', meta, autoload=True)
event = Table('event', meta, autoload=True)
registration_participant = Table('registration_participant', meta, autoload=True)
registration = Table('registration', meta, autoload=True)

data = {
    "captain": {
        "name": "Participant A",
        "email": "pa",
        "phone_number": "pam"
    },
    "other_participants": [
        {
            "name": "Participant B",
            "email": "pb",
            "phone_number": "pbm"
        },
    ],
    "team_name": None,
    "event_id": "a-capella",
    "data": {
        "some": "json"
    }
}


def insert_record(data):
    transaction = con.begin().transaction
    try:
        q = participant.insert().values(data["captain"])
        captain_pk = con.execute(q).inserted_primary_key[0]

        q = registration.insert().values(event_id=data["event_id"], team_name=data["team_name"], data=data["data"], captain=captain_pk)
        regsitration_pk = con.execute(q).inserted_primary_key[0]

        q = participant.registration_participant.insert().values(registration_id=regsitration_pk, participant_id=captain_pk)
        con.execute(q)

        for p in data.other_participants:
            q = participant.insert().values(p)
            pk = con.execute(q).inserted_primary_key[0]
            q = participant.registration_participant.insert().values(registration_id=regsitration_pk, participant_id=pk)
            con.execute(q)

        transaction.commit()
    except e:
        transaction.rollback()
        raise Exception("Registration Not Successful") from e

"""
Todo
 - schema
 - forms and insert queries
 - form generation
"""

"""
Setup Commands

"""