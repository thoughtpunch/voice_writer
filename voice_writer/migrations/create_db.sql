CREATE DATABASE voice_writer;
CREATE USER voice_writer WITH PASSWORD 'spyglass_home_HOMEMADE_chinch';
psycopg.errors.InsufficientPrivilege: permission denied to create database
ALTER ROLE voice_writer SET client_encoding TO 'utf8';
ALTER ROLE voice_writer SET default_transaction_isolation TO 'read committed';
ALTER ROLE voice_writer SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE voice_writer TO voice_writer;
GRANT ALL PRIVILEGES ON SCHEMA public TO voice_writer;
GRANT ALL PRIVILEGES ON TABLE django_migrations TO voice_writer;
GRANT USAGE ON SCHEMA public TO voice_writer;
GRANT CREATE ON SCHEMA public TO voice_writer;
GRANT CREATE ON DATABASE voice_writer TO voice_writer;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO voice_writer;