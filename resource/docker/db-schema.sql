--DROP SCHEMA IF EXISTS hydra;
--CREATE SCHEMA hydra;

DROP SCHEMA IF EXISTS erp4btc;
CREATE SCHEMA erp4btc;

--DROP ROLE IF EXISTS hydra;
--CREATE ROLE hydra WITH SUPERUSER LOGIN PASSWORD 'password';
--ALTER USER hydra SET search_path to 'hydra';

DROP ROLE IF EXISTS erp4btc;
CREATE ROLE erp4btc WITH SUPERUSER LOGIN PASSWORD 'password';
ALTER USER erp4btc SET search_path to 'erp4btc';


DROP TABLE IF EXISTS erp4btc.role;
CREATE TABLE erp4smb.role (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50),
  acl JSONB,
  parentid BIGINT
);

DROP TABLE IF EXISTS erp4btc.customers;
CREATE TABLE erp4btc.customers (
  id BIGSERIAL PRIMARY KEY,
  "firstName" VARCHAR(20),
  "lastName" VARCHAR(20),
--  roles VARCHAR[],
  "tg_id" VARCHAR(20)
--  "ismember" BOOLEAN
);
