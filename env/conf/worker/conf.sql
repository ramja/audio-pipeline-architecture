																																																																																																																																																									create table file_register (id BIGSERIAL PRIMARY KEY,nombre varchar(255) UNIQUE, fecha date DEFAULT now() ,estado char DEFAULT 'R');