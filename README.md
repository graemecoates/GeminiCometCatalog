# GeminiCometCatalog
This is a simple python3 script used to calculate current comet positions and upload via FTP to a Gemini-2 telescope mount controller. This makes the comet catalogue available via the Catalogs function on the Gemini-2 web interface and avoids having to use planetarium type software to point at a comet. Note that the comet positions (geocentric, as per the settings in the script) are only calculated at time of running the script - for slow moving comets, this should be more than good enough for pointing purposes if run relatively recently (e.g. at start of session). For faster moving comets, you may need to re-run the script more frequently to update the catalog positions!

## Getting Started
### Prerequisites

The script requires Python 3 to run, and was developed and tested under Python 3.5. The [pyephem](https://rhodesmill.org/pyephem/) module is required for the calculation of RA/Dec from the orbital elements. 

The full list of python modules required are:
```
ephem (provided by pyephem)
os
shutil
ftplib
urllib.request
datetime
```

The target machine requires access to the internet to download the comet elements (in xephem format suitable for pyephem) from the Minor Planet Centre, at: https://minorplanetcenter.net/iau/Ephemerides/Comets/Soft03Cmt.txt. This machine also needs to be able to ftp to the target Gemini 2 controller. Note that this script does not (yet) support catalogue upload via serial/USB. 

### Installing

1. Install python 3 on the target machine. (See Python website or OS packages for suitable installation packages).
2. Install python modules:
```
pip install pyephem 
```
The other modules are part of the standard library.

## Deployment

Copy the script into a target directory where you have permissions to write files and execute the script.

## Usage

Edit script.py and set the variables as required.

Run the script as follows:
```
python3 script.py
```

## Authors

* **Graeme Coates** - *Initial work* - [Chromosphere](https://www.chromosphere.co.uk)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Brandon Rhodes, author of pyephem
* Elwood Downey, author of xephem (the routines behind pyephem)
* The late Tom Hilton, author of: https://gemini2-com
* Didier Garrou, who wrote details on the Gemini catalogues and their upload: http://garriou.didier.free.fr/astro/gemini_anglais.html

## To-dos

* Move the params into their own file
* Migrate to Skyfield instead of (deprecated) pyephem when comet elements are supported
* Force upload into G2 HC unit (how?)
* Upload via serial for Gemini 1 units
