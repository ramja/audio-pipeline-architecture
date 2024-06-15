#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="./application_default_credentials.json"
python3 -m luigi --module etl2 Plot
