#!/usr/bin/env python3
import subprocess

with open('README.md') as f:
    lines = f.read().splitlines()

with open('/tmp/binding_readme.py', 'w') as f:

    language = None
    for line in lines:

        if line.startswith('```'):
            language = line[3:]
            continue

        if language is not None and line == '```':
            language = None
            continue

        if language == 'python':
            print(line)
            f.write(line + '\n')

subprocess.call(['/usr/local/bin/python3', '/tmp/binding_readme.py'])
