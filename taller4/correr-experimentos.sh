#! /bin/sh

set -eu

LOGS_DIR='logs'
USERNAME='jcperez'

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
}

# ----------------------------------------------------------------------------
# Listado de universidades para correr el experimento:
# ----------------------------------------------------------------------------

run_abc www.uba.ar
run_abc www.undef.edu.ar
run_abc www.unab.edu.ar
run_abc www.unaj.edu.ar
run_abc undav.edu.ar
run_abc www.unca.edu.ar
run_abc www.undec.edu.ar
run_abc www.unc.edu.ar
run_abc www.uncuyo.edu.ar
run_abc www.uner.edu.ar
run_abc www.unf.edu.ar
run_abc www.unsam.edu.ar
run_abc www.ungs.edu.ar
