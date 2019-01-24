#!/usr/bin/env python3

import sys
import os
import yaml
import json

# Reading parameters
config_file = sys.argv[1]
with open(config_file, "r") as f:
    opt = json.load(f)
    yaml_file = os.path.splitext(config_file)[0]+'.yaml'
    with open(yaml_file, "w") as yaml_f:
        yaml.dump(opt, yaml_f, allow_unicode=True, default_flow_style=False)

    print(yaml_file)

    # opt = yaml.load(f)
    # print(opt)
