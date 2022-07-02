#!/usr/bin/env python3

import getpass, argparse

def run():
  if getpass.getuser() != 'root':
    return print('Please run this script as a root user.')
  else:
    install_programs()

def install_programs():
  pass
