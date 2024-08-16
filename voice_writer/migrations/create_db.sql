CREATE DATABASE voice_writer;
CREATE USER vwadmin WITH PASSWORD 'spyglass_home_HOMEMADE_chinch';
ALTER ROLE vwadmin SET client_encoding TO 'utf8';
ALTER ROLE vwadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE vwadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE voice_writer TO vwadmin;
