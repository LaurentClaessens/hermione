#!/bin/bash

#
# This script installs the required venv for the linter.
#

# apt install  make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git


# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# cd ~/.pyenv/libexec
# ./pyenv install 3.7.4

# You may have to hack
# cd /usr/lib/x86_64-linux-gnu
# sudo ln -s libffi.so.7 libffi.so.6

VERSION=3.7.4
PYTHON3=~/.pyenv/versions/$VERSION/bin/python3
MAIN_DIR=$PWD
VENV_DIR=$MAIN_DIR/venv
BIN_DIR=$VENV_DIR/bin


pip3_install()
{
    PACKAGE=$1
    cd $BIN_DIR
    ./pip3 install $PACKAGE
}

upgrade_pip()
{
    cd $BIN_DIR
    ./pip3 install --upgrade pip
}

install_venv()
{
    $PYTHON3 -m venv $VENV_DIR
}

install_pip_packages()
{
    pip3_install youtube-dl
    pip3_install requests
    pip3_install lxml
    pip3_install pylint
    pip3_install pydocstyle
    pip3_install pycodestyle
}

install_venv
upgrade_pip
install_pip_packages
