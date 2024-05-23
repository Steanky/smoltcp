import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

features = []


def feature(name, default, min, max, pow2=None):
    vals = set()
    val = min
    while val <= max:
        vals.add(val)
        if pow2 == True or (isinstance(pow2, int) and val >= pow2):
            val *= 2
        else:
            val += 1
    vals.add(default)

    features.append(
        {
            "name": name,
            "default": default,
            "vals": sorted(list(vals)),
        }
    )


feature("iface_max_addr_count", default=2, min=1, max=8)
feature("iface_max_multicast_group_count", default=4, min=1, max=1024, pow2=8)
feature("iface_max_sixlowpan_address_context_count", default=4, min=1, max=1024, pow2=8)
feature("iface_neighbor_cache_count", default=4, min=1, max=1024, pow2=8)
feature("iface_max_route_count", default=2, min=1, max=1024, pow2=8)
feature("fragmentation_buffer_size", default=1500, min=256, max=65536, pow2=True)
feature("assembler_max_segment_count", default=4, min=1, max=32, pow2=4)
feature("reassembly_buffer_size", default=1500, min=256, max=65536, pow2=True)
feature("reassembly_buffer_count", default=1, min=1, max=32, pow2=4)
feature("ipv6_hbh_max_options", default=4, min=1, max=32, pow2=4)
feature("dns_max_result_count", default=1, min=1, max=32, pow2=4)
feature("dns_max_server_count", default=1, min=1, max=32, pow2=4)
feature("dns_max_name_size", default=255, min=64, max=255, pow2=True)
feature("rpl_relations_buffer_count", default=16, min=1, max=128, pow2=True)
feature("rpl_parents_buffer_count", default=8, min=2, max=32, pow2=True)

# ========= Update Cargo.toml

things = ""
for f in features:
    name = f["name"].replace("_", "-")
    for val in f["vals"]:
        things += f"{name}-{val} = []"
        if val == f["default"]:
            things += " # Default"
        things += "\n"
    things += "\n"

SEPARATOR_START = "# BEGIN AUTOGENERATED CONFIG FEATURES\n"
SEPARATOR_END = "# END AUTOGENERATED CONFIG FEATURES\n"
HELP = "# Generated by gen_config.py. DO NOT EDIT.\n"
with open("Cargo.toml", "r") as f:
    data = f.read()
before, data = data.split(SEPARATOR_START, maxsplit=1)
_, after = data.split(SEPARATOR_END, maxsplit=1)
data = before + SEPARATOR_START + HELP + things + SEPARATOR_END + after
with open("Cargo.toml", "w") as f:
    f.write(data)


# ========= Update build.rs

things = ""
for f in features:
    name = f["name"].upper()
    things += f'    ("{name}", {f["default"]}),\n'

SEPARATOR_START = "// BEGIN AUTOGENERATED CONFIG FEATURES\n"
SEPARATOR_END = "// END AUTOGENERATED CONFIG FEATURES\n"
HELP = "    // Generated by gen_config.py. DO NOT EDIT.\n"
with open("build.rs", "r") as f:
    data = f.read()
before, data = data.split(SEPARATOR_START, maxsplit=1)
_, after = data.split(SEPARATOR_END, maxsplit=1)
data = before + SEPARATOR_START + HELP + things + "    " + SEPARATOR_END + after
with open("build.rs", "w") as f:
    f.write(data)
