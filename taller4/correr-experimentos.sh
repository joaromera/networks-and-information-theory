#! /bin/sh
set -eu

# USO:
# Refefiní USERNAME. Desp, pone el listado de URLS al fondo. Si no tenes poetry
# instalado, borrá la parte que dice `poetry run`Desp, pone el listado de URLS
# al fondo. Si no tenes poetry instalado, borrá la parte que dice `poetry run`.
USERNAME='nnatalia'

# ----------------------------------------------------------------------------

LOGS_DIR='logs'

# Genera el nombre de archivo para una url y un nameserver.
# usage: format_filename 'www.uba.ar' 'x'
format_filename() {
    domain="${1}"
    nameserver_name="${2}"
    domain="$( echo "${domain}" | sed 's#\.##g' )"
    echo "${LOGS_DIR}/${USERNAME}-${domain}-${nameserver_name}.txt"
}

# Corre dns.py para un nameserver en particular
run_with_nameserver() {
    domain="${1}"
    nameserver="${2}"
    nameserver_name="${3}"
    output_file="$( format_filename "${domain}" "${nameserver_name}" )"

    echo ">>> Corriendo para ${domain} - ${nameserver_name} - ${output_file}"

    # Yo uso `poetry`. Si no usas poetry, borrá `poetry run`.
    sudo poetry run python3 src/dns.py "${domain}" "${nameserver}" > "${output_file}"
}

# Corre dns.py para los nameservers root a, b y c.
run_abc() {
    domain="${1}"
    run_with_nameserver "${domain}" "198.41.0.4"   "a" # a.root-servers.net
    run_with_nameserver "${domain}" "199.9.14.201" "b" # b.root-servers.net
    run_with_nameserver "${domain}" "192.33.4.12"  "c" # c.root-servers.net
    run_with_nameserver "${domain}" "199.7.91.13"  "d" # d.root-servers.net
    run_with_nameserver "${domain}" "192.203.230.10"  "e" # e.root-servers.net
    run_with_nameserver "${domain}" "192.5.5.241"  "f" # e.root-servers.net
    run_with_nameserver "${domain}" "192.112.36.4"  "g" # e.root-servers.net
    run_with_nameserver "${domain}" "198.97.190.53"  "h" # e.root-servers.net
    run_with_nameserver "${domain}" "192.36.148.17"  "i" # e.root-servers.net
    run_with_nameserver "${domain}" "192.58.128.30"  "j" # e.root-servers.net
    run_with_nameserver "${domain}" "193.0.14.129"  "k" # e.root-servers.net
    run_with_nameserver "${domain}" "199.7.83.42"  "l" # e.root-servers.net
    run_with_nameserver "${domain}" "202.12.27.33"  "m" # e.root-servers.net
}

# ----------------------------------------------------------------------------
# Listado de universidades para correr el experimento:
# ----------------------------------------------------------------------------

#Ejemplo:
run_abc www.uba.ar