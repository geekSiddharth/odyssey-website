create_tables = """
    CREATE TABLE event (
        id character varying(50) NOT NULL PRIMARY KEY,
        name character varying(50) NOT NULL,
        team_size smallint NOT NULL
    );

    CREATE TABLE participant (
        id SERIAL PRIMARY KEY NOT NULL,
        email character varying(50) NOT NULL,
        phone_number character varying(50),
        name character varying(50) NOT NULL
    );

    CREATE TABLE registration (
        id SERIAL PRIMARY KEY NOT NULL,
        event_id character varying(50) NOT NULL references event(id),
        captain integer references participant(id),
        team_name character varying(50),
        data JSON
    );

    CREATE TABLE registration_participant (
        registration_id integer NOT NULL  references registration(id),
        participant_id integer NOT NULL PRIMARY KEY references participant(id)
    );
"""

# this is just a comment
"""
CREATE DATABASE 
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';
CREATE USER odyssey WITH PASSWORD '%s';
RANT ALL PRIVILEGES ON DATABASE odyssey TO odyssey;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO odyssey;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to odyssey;
"""
