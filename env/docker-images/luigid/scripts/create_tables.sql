-- Extensiones
create extension pgcrypto;
create extension fuzzystrmatch;
create extension hstore;
create extension postgres_fdw;
create extension tablefunc;
create extension cube;
create extension dict_xsyn;
create extension pg_trgm;
create extension "uuid-ossp";

-- Eliminar tablas
drop table if exists file_register;

-- Crear tablas
create table file_register(
	id BIGSERIAL PRIMARY KEY,
	nombre varchar(255) UNIQUE, 
	fecha date DEFAULT now() ,
	estado char DEFAULT 'R', 
	prediction float DEFAULT -1.0 );

