import psycopg2
import json

with open('sensitive_data.json', newline='') as file:
    global config
    config = json.loads(file.read())


def connect():
    return psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (config["db-name"], config["db-user"], config["db-password"], config["db-host"], config["db-port"]))

conn = connect()

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
    "event_id": "a-cappella",
    "data": {
        "some": "json"
    }
}


def insert_record(data):
    cur = conn.cursor()
    cur.execute("SAVEPOINT insert_record")
    try:
        cur.execute("INSERT INTO participant (email, phone_number, name) VALUES (%s, %s, %s) RETURNING id", (data["captain"]["email"], data["captain"]["phone_number"], data["captain"]["name"]))
        captain_pk = cur.fetchone()
        cur.execute("INSERT INTO registration (event_id, captain, team_name, data) VALUES (%s, %s, %s, %s::json) RETURNING id", (data["event_id"], captain_pk, data["team_name"], json.dumps(data["data"])))
        regsitration_pk = cur.fetchone()
        cur.execute("INSERT INTO registration_participant (registration_id, participant_id) VALUES (%s, %s)", (regsitration_pk, captain_pk))

        for p in data["other_participants"]:
            cur.execute("INSERT INTO participant (email, phone_number, name) VALUES (%s, %s, %s) RETURNING id", (p["email"], p["phone_number"], p["name"]))
            pk = cur.fetchone()
            cur.execute("INSERT INTO registration_participant (registration_id, participant_id) VALUES (%s, %s)", (regsitration_pk, pk))
            cur.execute("RELEASE SAVEPOINT insert_record")
        
        conn.commit()
    except:
        cur.execute("ROLLBACK TO insert_record")
        raise Exception("Registration Not Successful")

"""
Todo
 - schema
 - forms and insert queries
 - form generation
"""

"""
Setup Commands

"""
