# Matterhorn

Matterhorn allows you to transform your centralized Nagios configuration into
a Bernard configuration distributed around your hosts.

## Installation

Just download the code and install [Pynag](https://github.com/pynag/pynag).

    sudo pip install pynag # to get the latest version
    sudo yum install pynag # on redhat if you get at least 0.5.0
    sudo apt-get install python-pynag pynag

## Usage

This script has to be run on the Nagios server host. It is going to load Nagios
configuration from its default location (`/etc/nagios3/nagios.cfg`).
To generate all the Bernard configuration files into the `/tmp` directory:

`python main.py`

## Limits

Matterhorn mainly depends on the Pynag module. Which mean that Nagios configuration
incompatible with Pynag won't work with Matterhorn.
