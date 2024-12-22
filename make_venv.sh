#!/bin/bash

#

# sudo apt install  build-essential zlib1g-dev libffi-dev libssl-dev libreadline-dev libsqlite3-dev liblzma-dev libbz2-dev
# git clone https://github.com/pyenv/pyenv.git ~/.pyenv
# ~/.pyenv/bin/pyenv install -v 3.10.6

set -u

VERSION=3.13.1
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
    echo $PYTHON3
    echo $VENV_DIR
    $PYTHON3 -m venv $VENV_DIR
}

install_pip_packages()
{
    pip3_install yt-dlp
    pip3_install requests
    pip3_install lxml
    pip3_install pylint
    pip3_install pydocstyle
    pip3_install pycodestyle
}

install_venv
upgrade_pip
install_pip_packages

cd $BIN_DIR
./pip3 install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz
echo "Le force-reinstall n'est peut-être plus obligatoire."

