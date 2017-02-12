import psycopg2
import json
from data import config, event_data, event_form
import csv

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
		WHERE event_id = '%s'
		ORDER BY r.id, isCaptain DESC;
		""" % event_id)

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
		prefix = "team mate #%s - " % reg["_pcount"]

		reg[prefix + "name"] = row[6]
		reg[prefix + "institute"] = row[7]
		reg[prefix + "email"] = row[8]
		reg[prefix + "phone_number"] = row[9]
	
	# begin csv column order logic
	if event_data[event_id]["onlyBatmanAndRobin"]:
		teamSize = 1 # number of all participants
	else:
		teamSize = event_data[event_id]["teamSizeMax"]

	isTeamEvent = event_data[event_id]["onlyBatmanAndRobin"] or event_data[event_id]["teamSizeMax"] > 1

	csv_column_order = ['registration_time']
	if(isTeamEvent):
		csv_column_order += ['team_name', 'team_size']

	for k in event_form[event_id]["data"]:
		csv_column_order.append(k)

	for i in range(1, teamSize + 1):
		prefix = "team mate #%s - " % i
		csv_column_order += [prefix + "name", prefix + "institute", prefix + "email", prefix + "phone_number"]

	# end csv column order logic
	rows = []
	for rid in result:
		row = []
		for col in csv_column_order:
			if col in result[rid]:
				row.append(result[rid][col])
			elif col in result[rid]["data"]:
				row.append(result[rid]["data"][col])
			else:
				row.append("")
		rows.append(row)

	with open("reg_csv_dump/%s.csv" % event_id, "w") as file:
		writer = csv.writer(file, quoting=csv.QUOTE_ALL)
		writer.writerows([csv_column_order] + rows)

for event_id in event_data:
	prepare_csv(event_id)