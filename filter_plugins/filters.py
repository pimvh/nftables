#!/usr/bin/python3

import itertools

from ansible.errors import AnsibleFilterError

class FilterModule():
    ''' custom filter to check if something is a list '''

    def filters(self):
        return {
            'is_list'           : self.is_list,
            'multiline_indent'  : self.multiline_indent,
            'strip_family'      : self.strip_family,
            'get_rule_names'    : self.get_rule_names,
        }

    def is_list(self, obj):
        """ boolean whether something is a list object """
        if isinstance(obj, list):
            return True
        else:
            return False

    def multiline_indent(self, obj, indent=1):
        """ fix jinja multiline indentation """
        out = ""

        indentation = indent * ' '

        if isinstance(obj, list):
            for x in obj:
                out += indentation + str(x) + '\n'
            return out

        return indentation + str(obj).replace('\n', indentation + '\n') + '\n'

    def strip_family(self, obj):
        """ strip family from nftable item """
        return obj.split(" ")[-1]

    def get_rule_names(self, obj):
        """ get rule names from nested nftables yaml """

        if not isinstance(obj, dict):
            raise AnsibleFilterError('This only works on dict')

        all_rules = []

        for table in obj:
            for _, rules in obj[table].get('chains').items():
                all_rules.append(rules)

        all_rules = list(itertools.chain(*all_rules))

        return all_rules
