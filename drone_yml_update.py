#!/usr/bin/env python

import argparse
import fileinput
import yaml
import re


def convert_var(group):
    return "$$" + group.group(1).strip()


def replace_template_vars(filename):
    for line in fileinput.input(filename, inplace=True):
        line = re.sub(r"{{(\w+)}}", convert_var, line)
        print line,


def update_publish(drone_yml):
    if not 'publish' in drone_yml:
        return False

    for key in drone_yml['publish'].keys():
        if 'branch' in drone_yml['publish'][key]:
            drone_yml['publish'][key]['when'] = \
                dict(branch=drone_yml['publish'][key]['branch'])

        if key == 'docker':
            drone_yml['publish']['docker']['tags'] = ['$(git rev-parse --short HEAD)']
            drone_yml['publish']['docker']['docker_host'] = "$$docker_server"

        remove_keys = ['push_latest', 'docker_publish', 
                       'branch', 'docker_port', 'docker_version', 'docker_server']
        for remove_key in remove_keys:
            if remove_key in drone_yml['publish'][key]:
                del drone_yml['publish'][key][remove_key]

    return True


def replace_hipchat_with_slack(drone_yml):
    if not 'notify' in drone_yml:
        return False
    if not 'hipchat' in drone_yml['notify']:
        return False

    del drone_yml['notify']['hipchat']
    drone_yml['notify']['slack'] = dict(
            webhook_url='$$slack_webhook',
            on_started=False,
            on_success=False,
            on_failure=True)

    return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert .drone.yml files from < 2.0 to v3 format')
    parser.add_argument('path', type=str)
    args = parser.parse_args()

    replace_template_vars(args.path + '/.drone.yml')

    drone_yml = yaml.load(open(args.path + '/.drone.yml').read())

    result = "Update .drone.yml to v3: publish {}, notify: {}".format(
            update_publish(drone_yml),
            replace_hipchat_with_slack(drone_yml))

    output = file(args.path + '/.drone.yml', 'w')
    yaml.dump(drone_yml, output, default_flow_style=False, indent=2)

    print result
