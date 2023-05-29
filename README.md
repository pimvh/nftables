# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

## Required variables

Review the variables as shown in defaults.

You can add a firewall definition to the variables for your host (../host_vars/[host_name].yaml), group of hosts (../group_vars/[group_name].yaml) using the following structure (see molecule.default.vars/test.yaml for an example):

```
nftables_ruleset:

  # firewall family and name"
  "inet firewall":

    # description of the table
    desc: "firewall of device"

    chains:

      # name of the respective chain
      input:
        # name of the variable from nftables_rules
        # that you would like to put in this chain
        - input_hook
        - valid_connections
        - ...

  # another table with the same structure
  "inet foo":

# the rules here ....
# every rule has two attributes:
# def: the definition of the rules or set of rules in valid nftables syntax
# depends_on: optional list of dependencies of variables from nftables_variables
nftables_rules:
  input_hook: >
    type filter hook input priority 0; policy drop;
  valid_connections:
    def: |
        ct state established, related accept
        ct state invalid drop

  new_connections:
    def: |
        ct state new accept


nftables_variables:
  header:
    note: this is a simple firewall, for ipv4 and ipv6
    def: "# built by me :)"

  tcp_ports:
    note: tcp ports configuration
    def: |
      {% if nftables_open_tcp_ports_global %}define OPEN_TCP_PORTS = { {{ nftables_open_tcp_ports_global | join(",") }} }{% endif +%}
      {% if nftables_open_tcp_ports_local %}define LOCAL_OPEN_TCP_PORTS = { {{ nftables_open_tcp_ports_local | join(",") }} }{% endif +%}
      {% if nftables_open_tcp_ports_vpn %}define VPN_TCP_PORTS = { {{ nftables_open_tcp_ports_vpn | join(",") }} }{% endif +%}

  ... (see defaults/main.yaml)


```

The ansible playbook will validate whether the correct variables are passed to the role using an argument_spec.

# Example playbook

Minimal (assuming you passed variables elsewhere):

```
hosts:
  - foo
roles:
  - pimvh.nftables

```

# TLDR - What will happen if I run this

- validate whether rules/some other variables are defined
- install nftables, and python interface
- create required nftable tables
- create dynamic tables as empty tables
- create an empty blocklist
- copy a nftables template to nftables directory
- edit nftables service to point to our new main file
- create script to reload firewall, which dumps tables outside of our control to files, and reloads the firewall after
- when nftables_abuseip_api_key is defined, add a script to pull the blocklist using their api, and make that a systemd service
- enable nftable service when requested
- uninstall iptables when requested

# Future Improvements

- Simply structure of rules that needs to be passed
- Improve argument_specs for `nftables_variables` and `nftables_ruleset`
