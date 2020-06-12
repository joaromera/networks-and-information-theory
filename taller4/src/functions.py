classes = {
    1:"IN"
}

types = {
    1:"A",
    2:"NS",
    5:"CNAME",
    6:"SOA",
    15:"MX",
    28:"AAAA"
}

def translate_class(resource_record_class:int) -> str:
    """Get human readable string from class number (which comes from a ShortEnumField)"""
    return classes[resource_record_class]

def translate_type(resource_record_type:int) -> str:
    """Get human readable string from type number"""
    return types[resource_record_type]

def print_dns_register(resource_record:scapy.layers.dns.DNSRR):
    domain_name = str(resource_record.rrname)
    time_to_live = resource_record.ttl
    register_class = translate_class(resource_record.rclass)
    register_type = translate_type(resource_record.type)
    value = ""
    # MX entries use exchange attribute for value
    # SOA entries use mname attribute for value
    # Other entries use rdata attribute for value
    try:
        value = str(resource_record.rdata)
    except AttributeError:
        try:
            value = str(resource_record.exchange)
        except AttributeError:
            value = str(resource_record.mname)
    print("{:30s} {:10d} {:5s} {:5s} {:30s}".format(
        domain_name, time_to_live, register_class, register_type, value))

def print_section(name:str ,section):
    if section:
        print(name + " SECTION:")
        for reg in section.iterpayloads():
            print_dns_register(reg)