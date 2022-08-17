# Spreadsheet Energy System Model Generator (SESMG) ![what-why](https://cs.adelaide.edu.au/~christoph/badges/content-what-why-brightgreen.svg) ![how](https://cs.adelaide.edu.au/~christoph/badges/content-how-green.svg)

The **SESMG** provides a spreadsheet interface to the "Open Energy Modeling Framework" ("oemof"), allowing modeling and optimization of urban energy systems based the spreadsheet. 

**SESMG** makes it easier to create oemof-based energy system models.

- You don't need to touch the command line.
- You don't need programming skills.
- **SESMG** is an intuitive spreadsheet driven tool.

The components defined in this spreadsheet are defined with the included Python 
program and the open source Python library "oemof", assembled to an energy system 
and optimized with open source solvers (e.g. “CBC”). The modeling results can be 
viewed and analyzed using a browser-based results output.

![workflow_graph_SESMG](/docs/images/SESMG_principle.png)

## Quick Start ![how](https://cs.adelaide.edu.au/~christoph/badges/content-how-green.svg)

### Step 1) Download Python 3.7 

- go to the Python download page
- chose a Python version (e.g. “Python 3.7.6”) and click “download”
- download the operating system specific installer (e.g. “Windows x86-64 executable installer”)
- execute the installer on your computer

Linux only: 
- run `$ sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 2`
- test by running `$ python3 --version`

### Step 2) Download the SESMG from GIT as .zip folder 

### Step 3) Extract the .zip folder into any directory on the computer
Watch out: we do not support spaces in the path yet. It will lead to an error if there is one.

### Step 4) Install pip (Linux only)

run `$ sudo apt-get install python3-pip`

### Step 5) Install tkinter (Linux only)

run `$ sudo apt-get install python3.7-tk`

### Step 6) Download the CBC-solver (Windows and Linux only) 

#### For Windows:

Download [here](http://ampl.com/dl/open/cbc/cbc-win64.zip)

<u>Within this step there are two options: </u>
- install the cbc-Solver on your whole operating system.
- copy and paste the downloaded executable two your **SESMG**-working directory.

#### For Linux:

run `$ sudo apt-get install coinor-cbc`

### Step 7) Install Graphviz (Windows and Linux only) 

#### For Windows:
Download [here](https://graphviz.gitlab.io/download/)

- Select and download the graphviz version for your device (e.g. graphviz-2.38.msi for Windows).
- Execute the installation manager you just downloaded. Choose the following directory for the installation: “C:\Program Files (x86)\Graphviz2.38" (should be the default settings).

#### For Linux:

run `$ sudo apt-get install graphviz`

### Step 8) Start the operating system specific installation file


## SESMG Features & Releases ![what-why](https://cs.adelaide.edu.au/~christoph/badges/content-what-why-brightgreen.svg) 

### Project Status 
[![Documentation Status](https://readthedocs.org/projects/spreadsheet-energy-system-model-generator/badge/?version=latest)](https://spreadsheet-energy-system-model-generator.readthedocs.io/en/latest/?badge=latest)
[![Requirements Status](https://requires.io/github/chrklemm/SESMG/requirements.svg?branch=master)](https://requires.io/github/chrklemm/SESMG/requirements/?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/d82c7d94f8f421db19ce/maintainability)](https://codeclimate.com/github/GregorBecker/SESMG/maintainability)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/GregorBecker/SESMG/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/GregorBecker/SESMG/?branch=master)
[![codecov](https://codecov.io/gh/GregorBecker/SESMG/branch/master/graph/badge.svg?token=9UW00ZSDYC)](https://codecov.io/gh/GregorBecker/SESMG)
[![Coverage Status](https://coveralls.io/repos/github/GregorBecker/SESMG/badge.svg?branch=master)](https://coveralls.io/github/GregorBecker/SESMG?branch=master)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d82c7d94f8f421db19ce/test_coverage)](https://codeclimate.com/github/GregorBecker/SESMG/test_coverage)


### Examples
Examples are stored in a separate GIT-Repository: https://github.com/chrklemm/SESMG_Examples.

### Project status
✓ Draft (alpha, beta) State <br />
✓ Modeling and Optimization of holistic energy systems <br />
✓ Several result plotting oportunities <br />
✓ Usable on Windows, MacOS, and Linux <br />

✘ No support of Python 3.8 and newer <br />
✘ Issues on installing depedencies <br />
✘ Incomplete Documentation <br />
✘ Programming of tests still pending <br />
✘ More time to code other things ... wait ✓!  

## Detailed Documentation! ![references](https://cs.adelaide.edu.au/~christoph/badges/content-references-orange.svg)

The [documentation](https://spreadsheet-energy-system-model-generator.readthedocs.io/en/latest/),
which includes detailed instructions for **installation** and **use**, **troubleshooting** 
and much more, can be accessed via the following link:

https://spreadsheet-energy-system-model-generator.readthedocs.io/en/latest/.

## Questions? ![who](https://cs.adelaide.edu.au/~christoph/badges/content-who-yellow.svg) ![references](https://cs.adelaide.edu.au/~christoph/badges/content-references-orange.svg)

[Use the Discussions Section](https://github.com/chrklemm/SESMG/discussions) and let's chat!

## Credits ![who](https://cs.adelaide.edu.au/~christoph/badges/content-who-yellow.svg)

### Contact and Code of Conduct 

Code of Conduct can be found [here](/CODE_OF_CONDUCT.md).

#### Contact information 
Münster University of Applied Sciences

Christian Klemm - christian.klemm@fh-muenster.de

### Acknowledgments

The Spreadsheet Energy System Model Generator was carried out within the 
research project [R2Q "Resource Planing for Urban Districts](https://www.fh-muenster.de/forschungskooperationen/r2q/index.php). 
The project was funded by the Federal Ministry 
of Education and Research (BMBF) funding program [RES:Z "Resource-Efficient Urban Districts](https://ressourceneffiziente-stadtquartiere.de). The funding measure is part of the flagship initiative "City of the Future" within the BMBF's framework programme "Research for Sustainable Development - FONA3".
The contributors gratefully acknowledge the support of BMBF (grant number 033W102).

### License

This project is published under GNU GPL-3.0 license, click [here](https://github.com/chrklemm/SESMG/blob/master/LICENSE) for more details.

## Contributing ![contribution](https://cs.adelaide.edu.au/~christoph/badges/content-contribution-blue.svg)

Issues and Pull Requests are greatly appreciated. If you've never contributed to an open source project before I'm more than happy to walk you through how to create a Pull Request.

Detailed description of the contribution procedure as well as the projects coding standards can be found [here](/docs/CONTRIBUTING.md).
