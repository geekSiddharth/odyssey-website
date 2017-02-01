import psycopg2
import json
from data import config, event_data, event_form

def connect():
    return psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (config["db-name"], config["db-user"], config["db-password"], config["db-host"], config["db-port"]))

conn = connect()

def process_post_request(form, event_id):
    # captain
    data = {
        "captain": {
            "name": form["captain_name"],
            "email": form["captain_email"],
            "phone_number": form["captain_phone"],
            "institute": "lel"
        },
        "event_id": event_id
    }
    # team

    if(event_data[event_id]["teamSizeMax"] > 1):
        data["team_name"] = form["team_name"]
        data["team_size"] = form["team_size"]
        data["other_participants"] = []

        for i in range(event_data[event_id]["teamSizeMax"] - 1):
            data["other_participants"].append({
                "name": form["participant_name_" + str(i)],
                "email": form["participant_email_" + str(i)],
                "phone_number": form["participant_phone_" + str(i)],
                "institute": form["participant_institute_" + str(i)]
            })
    else:
        data["team_name"] = None
        data["team_size"] = None

    # json
    data["data"] = {}
    d = event_form[event_id]["data"]
    for k in d:
        value = form["data_" + k] if d[k].type == "string" else d[k].options[form["data_" + k]]
        data["data"][k] = value

    return data

def insert_record(data, event_id):
    cur = conn.cursor()
    cur.execute("SAVEPOINT insert_record")
    try:
        cur.execute("INSERT INTO participant (name, institute, email, phone_number) VALUES (%s, %s, %s, %s) RETURNING id", (data["captain"]["name"], data["captain"]["institute"], data["captain"]["email"], data["captain"]["phone_number"]))
        captain_pk = cur.fetchone()
        cur.execute("INSERT INTO registration (event_id, captain, team_size, team_name, data) VALUES (%s, %s, %s, %s, %s::json) RETURNING id", (event_id, captain_pk, data["team_size"], data["team_name"], json.dumps(data["data"])))
        regsitration_pk = cur.fetchone()
        cur.execute("INSERT INTO registration_participant (registration_id, participant_id) VALUES (%s, %s)", (regsitration_pk, captain_pk))

        for p in data["other_participants"]:
            cur.execute("INSERT INTO participant (email, phone_number, name, institute) VALUES (%s, %s, %s, %s) RETURNING id", (p["email"], p["phone_number"], p["name"], p["institute"]))
            pk = cur.fetchone()
            cur.execute("INSERT INTO registration_participant (registration_id, participant_id) VALUES (%s, %s)", (regsitration_pk, pk))
            cur.execute("RELEASE SAVEPOINT insert_record")
        
        conn.commit()
    except:
        cur.execute("ROLLBACK TO insert_record")
        raise

"""
Todo
 - x schema
 - x forms and insert queries
 - x form generation
"""

"""
Setup Commands

"""
