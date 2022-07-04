# WSL PHP Install Script
This is a script made using Python that automates the installation of PHP, Composer, MySQL, as well as NodeJS on Ubuntu 20.04/22.04. I built this with Laravel developers in mind as I am one. If you wish to extend this script, please feel free to fork it and add to it 😃.

## Installation of Programs
Use the `./path/to/script.py install` command along with any of these arguments to install the programs you wish `--php`, `--mysql`, `--node=[version]` or `--all`. You can run `./path/to/script.py --help` to get more info.

## Restoring MySQL Database from a file
I usually backup my databases to a file when I am about to reinstall WSL for obvious reasons. Restoring a database isn't so hectic but I am "efficient" so I decided to add this feature to the script. To restore your database from a file, please run this command `./path/to/script restore-db path/to/db`.

## To be done
- Add error handling when a command fails to run
- I can't think of anything else. Let me know if you have any ideas 🤷🏾‍♂️
