#!/usr/bin/env python3

import getpass, argparse, os, time

def run():
  if getpass.getuser() != 'root':
    return print('Please run this script as a root user.')
  else:
    install_programs()

def print_blue(text):
  red = '\n\033[94m'
  print(f"{red}{text}")
  time.sleep(2)

def update_programs():
  print_blue('Updating installed applications...')
  os.system('apt update && apt upgrade -y')

def install_programs():
  update_programs()

  parser = argparse.ArgumentParser(
    description='Installs PHP, Composer, MySQL and NodeJS on WSL (Ubuntu)'
  )

  parser.add_argument('--php', help='Installs PHP', action='store_true')
  parser.add_argument('--mysql', help='Installs MySql', action='store_true')
  parser.add_argument('--db-path', help='Restores database from specified path')
  parser.add_argument('--node', help='Installs NodeJs', default=14, type=int)
  parser.add_argument('--all', help='Installs all programs', action='store_true')

  args = parser.parse_args()

  if args.all:
    install_all_programs(args.node)
    return
  elif args.mysql:
    install_mysql()
  elif args.php:
    install_php()
  elif args.node:
    install_node(args.node)
  elif args.db_path:
    restore_database(args.db_path)
  else:
    print('Invalid argument(s) passed to this command')

def install_all_programs(node_version):
  install_php()
  install_mysql()
  install_node(node_version)

def install_php():
  php_extensions = [
    'cli', 
    'mbstring', 
    'common',
    'mysql',
    'sqlite3',
    'xml',
    'pdo',
    'zip',
    'json',
    'tokenizer'
  ]

  required_dependencies = [
    'lsb-release',
    'ca-certificates',
    'apt-transport-https',
    'software-properties-common'
  ]

  # Install PHP 8.1 and 7.4
  print_blue("About to install PHP...")
  os.system(f"apt install {' '.join(required_dependencies)} -y")
  os.system(f"add-apt-repository ppa:ondrej/php -y")
  os.system(f"apt install -y php{8.1,7.4}-{','.join(php_extensions)} -y")

  # Install Composer
  print_blue('About to install Composer...')
  os.system('php -r "copy(\'https://getcomposer.org/installer\', \'composer-setup.php\');"')
  os.system('php composer-setup.php')
  os.system('php -r "unlink(\'composer-setup.php\');"')
  os.system('mv composer.phar /usr/local/bin/composer')

def install_mysql():
  # Install MariaDB Server
  print_blue('About to install MariaDB...')
  os.system("apt install mariadb-server -y")
  os.system('echo -e "\ny\nn\ny\ny\ny\ny" | /usr/bin/mysql_secure_installation')

def install_node(version):
  # Install NodeJS
  print_blue('About to install NodeJS and Yarn')
  os.system(f"curl -sL https://deb.nodesource.com/setup_{version}.x | sudo -E bash -")
  os.system("apt install nodejs")
  os.system("npm i -g npm")
  os.system("npm i -g yarn")

def restore_database(path):
  print_blue(f'About to restore database from {path}')
  os.system(f'mysql < {path}')

try:
  run()
except KeyboardInterrupt:
  print('You have stopped the installation.')
