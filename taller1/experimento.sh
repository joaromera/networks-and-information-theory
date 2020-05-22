#! /bin/sh

DT="$(date "+%Y-%m-%d-%H-%M")"
time poetry run python mostrar_fuentes.py > "${DT}-${USER}.log"
