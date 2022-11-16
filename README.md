# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

## Required variables

Review the variables as shown in defaults.

1. Review rules.example and variables.example and define your custom rules and required variables for your firewall.

2. Add a firewall definition to the variables for your host (../host_vars/[host_name].yaml), group of hosts (../group_vars/[group_name].yaml) or to defaults/main.yaml, using the following structure:

```
nftables:

  # firewall family and name"
  "inet firewall":

    # description of the table
    desc: "firewall of device"

    chains:

      # name of the respective chain
      input:
        # name of the variable from nft_rules
        # that you would like to put in this chain
        - input_hook
        - valid_connections
        - ...

  # another table with the same structure
  "inet foo":
  ...
```

The ansible playbook will validate whether the variables exist that you defined before running.

# Example playbook

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
- when abuseip_api_key is defined, add a script to pull the blocklist using their api, and make that a cronjob
- enable nftable service when requested
- uninstall iptables when requested

# License

The GPLv3 License (GPLv3)

Copyright (c) 2022 Author

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
