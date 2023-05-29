#!/usr/bin/python3

import itertools

from ansible.errors import AnsibleFilterError
from ansible.template import AnsibleUndefined


class FilterModule:
    """custom filter to check if something is a list"""

    def filters(self):
        return {
            "is_list": self.is_list,
            "multiline_indent": self.multiline_indent,
            "strip_family": self.strip_family,
            "get_rule_names": self.get_rule_names,
            "get_rule_dependencies": self.get_rule_dependencies,
        }

    def is_list(self, obj):
        """boolean whether something is a list object"""
        if isinstance(obj, list):
            return True
        else:
            return False

    def multiline_indent(self, obj, indent=1):
        """fix jinja multiline indentation"""
        out = ""

        indentation = indent * " "

        if isinstance(obj, list):
            for x in obj:
                out += indentation + str(x) + "\n"
            return out

        return indentation + str(obj).replace("\n", indentation + "\n") + "\n"

    def strip_family(self, obj):
        """strip family from nftable item"""
        return obj.split(" ")[-1]

    def get_rule_names(self, obj):
        """get rule names from nested nftables yaml"""

        if isinstance(obj, AnsibleUndefined):
            return []

        elif not isinstance(obj, dict):
            raise AnsibleFilterError("This only works on dict")

        all_rules = []

        for table in obj:
            for _, rules in obj[table].get("chains").items():
                all_rules.append(rules)

        all_rules = list(itertools.chain(*all_rules))

        return all_rules

    def get_rule_dependencies(self, obj, all_rules):
        """get rule potential rule dependencies from nested nftables yaml"""

        if isinstance(obj, AnsibleUndefined):
            return []

        elif not isinstance(obj, dict):
            raise AnsibleFilterError("This only works on dict")

        dependencies = []

        for table in obj:
            for _, rules in obj[table].get("chains").items():
                for rule in rules:
                    current_rule = all_rules[rule]
                    if rule_dependencies := current_rule.get("depends_on"):
                        if not isinstance(rule_dependencies, list):
                            raise AnsibleFilterError(
                                "dependency for %s should be list", rule
                            )

                        for dep in rule_dependencies:
                            dependencies.append(dep)

        # return deduplicated dependencies
        return list(set(dependencies))
