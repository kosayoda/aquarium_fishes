aquarium_fishies
=================

Loads https://webglsamples.org/aquarium/aquarium.html, spawns fishes and set certain settings from the command-line.

Uses Selenium to spawn the browser. Currently supported are: Firefox, Google Chrome.

Only tested on Python >3.6.

Installation
-------------
1. Download the tar.gz file from `here`_.

.. _here: https://github.com/kosayoda/aquarium_fishes/releases/
2. In the same directory as the tar.gz file, run ``pip install <filename>``.
3. Run ``fishes -h`` to see a list of arguments.

Manual Installation
-------------------
Requirements
------------
- Python >3.6
- selenium >3.1
- webdriver_manager >1.7

Installation
-------------
1) Click the "Clone or download" button in the top right corner then click "Download ZIP". Alternatively, clone the repository using ``git clone``.

2) Unpack the zip file

3) Run the main script
::
    cd fishes
    python __main__.py

Usage
-----
fishes -h
::
    usage: fishes [-h] [-v] [-f] [-s] [-fs] browser

    Spawns an aquarium from https://webglsamples.org/aquarium/aquarium.html in the
    browser

    positional arguments:
    browser             browser used to load the website (options: Firefox,
                        Chrome)

    optional arguments:
    -h, --help          show this help message and exit
    -v, --verbose       Verbose output
    -f , --fishes       number of fishes to spawn (options: 1, 100, 500, 1000,
                        5000, 10000, 15000, 20000, 25000, 30000) (default: 500)
    -s , --speed        overall speed of the aquarium (options: 0, 1, 2, 3, 4)
                        (default: 2)
    -fs , --fishspeed   speed of the fish (options: 0, 1, 2) (default: 1)
