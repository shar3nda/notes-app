#!/usr/bin/env python3

import jinja2
import os
import sys

env = jinja2.Environment()
template = env.from_string(sys.stdin.read())
print(template.render(**os.environ))
