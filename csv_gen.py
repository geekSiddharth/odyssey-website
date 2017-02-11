import psycopg2
import json
from data import config, event_data, event_form

def connect():
	return psycopg2.connect("dbname=%s user=%s password=%s host=%s port=%s" % (config["db-name"], config["db-user"], config["db-password"], config["db-host"], config["db-port"]))

conn = connect()

def prepare_csv(event_id):
	result = {}
	cur = conn.cursor()
	cur.execute("""
		SELECT r.id, registration_time, team_name, team_size, data, captain = participant_id AS isCaptain, name, institute, email, phone_number FROM participant p
		LEFT JOIN registration_participant rp
		ON rp.participant_id = p.id
		LEFT JOIN registration r
		ON rp.registration_id = r.id
		WHERE event_id = 'can-you-duet'
		ORDER BY r.id, isCaptain DESC;
		""")

	for row in cur:
		if row[0] not in result:
			result[row[0]] = {
				"registration_time": row[1],
				"team_name": row[2],
				"team_size": row[3],
				"data": row[4],
				"_pcount": 0
			}
		reg = result[row[0]]
		# add participant
		reg["_pcount"] += 1
		prefix = "participant #%s - " % reg["_pcount"]

		reg[prefix + "name"] = row[6]
		reg[prefix + "institute"] = row[7]
		reg[prefix + "email"] = row[8]
		reg[prefix + "phone_number"] = row[9]

	print(result)

