#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
print(sys.argv)


if len(sys.argv) != 2:
    print('Invalid input.')
    sys.exit(1)

if len(sys.argv) == 2:
    print(f'Running program: {sys.argv[0]}')
    print(f'Running program: {sys.argv[1]}')
    # sys.argv[1]
    cpu = CPU()
    cpu.load(sys.argv[1])
    cpu.run()
