#!/usr/bin/env python3

import getpass, argparse

def run():
  if getpass.getuser() != 'root':
    return print('Please run this script as a root user.')
  else:
    install_programs()

def install_programs():
  parser = argparse.ArgumentParser(
      description='Installs PHP, Composer, MySQL and NodeJS on WSL (Ubuntu)'
    )

  parser.add_argument('--php', help='Installs PHP')
  parser.add_argument('--mysql', help='Installs MySql')
  parser.add_argument('--node', help='Installs NodeJs')
  parser.add_argument('--all', help='Installs all programs')

  args = parser.parse_args()

  if args.all:
    install_all_programs()
    return
  elif args.mysql:
    install_mysql()
  elif args.php:
    install_php()
  elif args.node:
    install_node()

def install_all_programs():
  pass

def install_php():
  pass

def install_mysql():
  pass

def install_node():
  pass
