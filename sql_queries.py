create_tables = """
    CREATE TABLE event (
        id character varying(50) NOT NULL PRIMARY KEY
    );

    CREATE TABLE participant (
        id SERIAL PRIMARY KEY NOT NULL,
        name character varying(100) NOT NULL,
        institute VARCHAR(100),
        email character varying(100) NOT NULL,
        phone_number character varying(50)
    );

    CREATE TABLE registration (
        id SERIAL PRIMARY KEY NOT NULL,
        event_id character varying(50) NOT NULL references event(id),
        captain integer references participant(id) NOT NULL,
        team_name character varying(50),
        team_size SMALLINT,
        data JSON
    );

    CREATE TABLE registration_participant (
        registration_id integer NOT NULL  references registration(id),
        participant_id integer NOT NULL PRIMARY KEY references participant(id)
    );
"""

# this is just a comment
"""
CREATE DATABASE odyssey
  ENCODING 'UTF8'
  LC_COLLATE = 'en_US.UTF-8'
  LC_CTYPE = 'en_US.UTF-8';
CREATE USER odyssey WITH PASSWORD '%s';
GRANT ALL PRIVILEGES ON DATABASE odyssey TO odyssey;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO odyssey;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public to odyssey;
"""
