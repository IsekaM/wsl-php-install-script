#!/usr/bin/env python3

import getpass, argparse, os, time, inspect

def run():
  if getpass.getuser() != 'root':
    return print('Please run this script as a root user.')
  else:
    install_programs()

def get_home_path():
  return os.path.expanduser(f'~{os.getenv("SUDO_USER")}')

def print_color(text, color = "blue"):
  signal = '[/]' if color == 'blue' else 'x'
  color = '\033[94m' if color == 'blue' else '\033[91m'

  print(f"\n{color}{signal} {text}\x1b[0m")
  
  time.sleep(1.25)

def update_programs():
  print_color('Updating installed applications...')
  os.system('apt update && apt upgrade -y')

def create_commands_and_arguments():
  parser = argparse.ArgumentParser(
    description='Installs PHP, Composer, MySQL and NodeJS on WSL (Ubuntu)'
  )

  subparser = parser.add_subparsers(title='main commands')

  install_subparser = subparser.add_parser(
    'install',
    help='Installs programs'
  )

  install_subparser.add_argument(
    '--php', 
    help='Installs PHP', 
    action='store_true'
  )

  install_subparser.add_argument(
    '--mysql', 
    help='Installs MySql', 
    action='store_true'
  )

  install_subparser.add_argument(
    '--node', 
    help='Installs NodeJs', 
    default=14, 
    type=int
  )

  install_subparser.add_argument(
    '--all', 
    help='Installs all programs', 
    action='store_true'
  )

  restore_db_subparser = subparser.add_parser(
    'restore-db', 
    help='Restores MySQL database from file'
  )

  restore_db_subparser.add_argument(
    'path', 
    help='Path to database', 
    type=str
  )

  return parser.parse_args()

def install_programs():
  args = create_commands_and_arguments()

  update_programs()

  add_custom_ps1()

  if args.all:
    install_all_programs(args.node)
    return
  elif args.mysql:
    install_mysql()
  elif args.php:
    install_php()
  elif args.node:
    install_node(args.node)
  elif args.path:
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
    'tokenizer',
    'soap',
    'curl',
    'gd',
  ]

  required_dependencies = [
    'lsb-release',
    'ca-certificates',
    'apt-transport-https',
    'software-properties-common'
  ]

  packages = list(map(lambda ext: f"php8.1-{ext} php7.4-{ext}", php_extensions))

  # Install PHP 8.1 and 7.4
  print_color("About to install PHP...")
  os.system(f"apt install {' '.join(required_dependencies)} -y")
  os.system(f"add-apt-repository ppa:ondrej/php -y")
  os.system(f"apt install {' '.join(packages)} -y")

  # Install Composer
  print_color('About to install Composer...')
  os.system('php -r "copy(\'https://getcomposer.org/installer\', \'composer-setup.php\');"')
  os.system('php composer-setup.php')
  os.system('php -r "unlink(\'composer-setup.php\');"')
  os.system('mv composer.phar /usr/local/bin/composer')

  # Add bash aliases
  add_bash_aliases()

def install_mysql():
  # Install MariaDB Server
  print_color('About to install MariaDB...')
  os.system("apt install mariadb-server -y")
  os.system("/etc/init.d/mysql start")
  os.system('echo -e "\ny\nn\ny\ny\ny\ny" | /usr/bin/mysql_secure_installation')

def install_node(version):
  # Install NodeJS
  print_color('About to install NodeJS and Yarn...')
  os.system(f"curl -sL https://deb.nodesource.com/setup_{version}.x | sudo -E bash -")
  os.system("apt install nodejs")
  os.system("npm i -g npm")
  os.system("npm i -g yarn")

def restore_database(path):
  print_color(f'About to restore database from {path}')
  os.system(f'mysql < {path}')

def add_bash_aliases():
  print_color("Attempting to add bash aliases...")

  home_path = get_home_path();
  bash_aliases_path = os.path.join(home_path, '.bash_aliases')

  with open(bash_aliases_path, 'a+') as bash_aliases_file:
    if 'pa="php artisan"' not in bash_aliases_file.read():
      bash_aliases_file.write('#PHP Aliases\nalias pa="php artisan"')
    else:
      print_color('Bash aliases already added', 'red')

def add_custom_ps1():
  print_color("Attempting to add custom PS1...")

  home_path = get_home_path()
  bash_rc_path = os.path.join(home_path, '.bashrc')
  file_content = r"""
    # Custom PS1
    parse_git_branch() {
      git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
    }

    export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] \n$ "
    export PATH="~/.npm-global/bin:~/.config/composer/vendor/bin:$PATH" 
  """.strip()

  with open(bash_rc_path, 'r+') as bash_rc_file:
    if 'parse_git_branch()' not in bash_rc_file.read():
      bash_rc_file.write(inspect.cleandoc(file_content))
      os.system(f'/bin/sh {bash_rc_path}')
    else:
      print_color('Custom PS1 already exists', 'red')

try:
  run()
except KeyboardInterrupt:
  print('You have stopped the installation.')
