FROM postgres:13.14-bullseye

ADD fips.csv /docker-entrypoint-initdb.d
ADD insert_fips.sh /docker-entrypoint-initdb.d
