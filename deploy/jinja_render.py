#!/usr/bin/env python3

import os
import sys

import jinja2

env = jinja2.Environment()
template = env.from_string(sys.stdin.read())
print(template.render(**os.environ))
