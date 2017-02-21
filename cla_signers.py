#!/usr/bin/python
#
# Copyright 2017 JanusGraph Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Validator for the CLA signers YAML file."""

import sys
try:
    import yaml
except:
    from third_party.python import yaml


def ParseYaml(filename):
    with open(filename) as yaml_input:
        return yaml.safe_load(yaml_input.read())



def ValidateFile(filename):
    def ValidateAccounts(accounts):
        status_code = 0
        accounts_keys = ('name', 'email', 'github')
        for account in accounts:
            if sorted(account.keys()) != sorted(accounts_keys):
                status_code = 1
                sys.stderr.write('The only allowed and required keys for people/bot accounts are: %s.\n' % str(accounts_keys))
                sys.stderr.write('Invalid account record: %s\n\n' % account)
        return status_code

    status_code = 0

    data = ParseYaml(filename)
    ValidateAccounts(data['people'])
    ValidateAccounts(data['bots'])

    company_keys = ('name', 'people')
    for company in data['companies']:
        if sorted(company.keys()) != sorted(company_keys):
            status_code = 2
            sys.stderr.write('The only allowed and required keys for `company` are: %s.\n' % str(company_keys))
            sys.stderr.write('Invalid company record: %s\n\n' % company)
            continue
        people_status = ValidateAccounts(company['people'])
        if people_status != 0 and status_code == 0:
            status_code = people_status

    return status_code

def ShowSyntax(program):
    sys.stderr.write("""\
Syntax: %s [command] [file]

Commands:
  validate: verify invariants in given config file
""" % program)

def main(argv):
    program = argv[0]
    if len(argv) < 3:
        ShowSyntax(program)
        sys.exit(1)

    command = argv[1]
    filename = argv[2]

    if command == 'validate':
        sys.exit(ValidateFile(filename))
    else:
        sys.stderr.write('Invalid command: %s\n' % command)
        ShowSyntax(program)
        sys.exit(2)


if __name__ == '__main__':
    main(sys.argv)
