# Matterhorn

Matterhorn allows you to transform your centralized Nagios configuration into
a Bernard configuration distributed around your hosts.

## Installation

Just download the code and install Pynag.

`pip install pynag`

## Usage

To generate all the Bernard configuration files into the `/tmp` directory:

`python main.py`

## Limits

Matterhorn mainly depends on the Pynag module. Which mean that Nagios configuration
incompatible with Pynag won't work with Matterhorn.
