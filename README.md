stew
=======

This script processes catalog(s) of packages, verifies the sha1 hash of each package, downloads any missing or updated packages, 
and compiles a new image consisting of a given base OS X installer and the list of packages.

Requirements
------------

+ 10.9.x and above (you must build your images on a matching system)
+ python 2.7
+ InstallESD.dmg must be renamed in the format OSVERS_OSBUILD_InstallESD.dmg
```
InstallESD.dmg -> 10.9.2_13C64_InstallESD.dmg
```

Usage
-----

    Usage: sudo ./stew [options]

    Options:
      -h, --help            show this help message and exit
      -b CATALOG, --build=CATALOG
                            Specify catalog to process
      -c, --configure       Set up or recreate configuration file
      -u PACKAGE, --upload=PACKAGE
                            Upload package to webserver
      -C FILENAME, --checksum=FILENAME
                            Return checksum of a cached package


Configuration
-------------

When you run ```stew``` for the first time, or with the ```-c``` option, you will be asked to populate a config file.  This file is stored at ```~/.stew_config``` and will be recreated any time you use the ```-c``` option. This facilitates the uploading of packages using ```scp```, so setting up a key-based login for your webserver is highly recommended.

You will be asked to provide the following information:

+ The FQDN of your webserver (example: mypackagerepo.mycorp.com)
+ The full path of your remote repo folder (example: /var/www/html/packages)
    + the web repo is just one single folder, which will contain all OS Installers, packages, and disk images
+ The login user for your webserver (example: stewuser)

Uploading packages
------------------

```stew``` supports both the pkg and dmg format for processing packages. You may simply upload packages with the ```stew -u``` option, or you may wish to copy the companion ```uptodate``` script to your $PATH and use that. ```uptodate``` also offers the ability to list catalogs and automates the editing and updating of catalog files:

        usage: uptodate [-h] [-p PACKAGE] [-c CATALOG] [-l LIST_CATALOG]

        optional arguments:
          -h, --help            show this help message and exit
          -p PACKAGE, --package PACKAGE
                                /path/to/package
          -c CATALOG, --catalog CATALOG
                                /path/to/catalog
          -l LIST_CATALOG, --list_catalog LIST_CATALOG
                                /path/to/catalog

For example, to upload a package to your webserver, and update a catalog:

        uptodate -p /path/to/package -c /path/to/catalog

To update a catalog's metadata, such as volume name and output name:

        uptodate -c /path/to/catalog

Storing packages locally
------------------------

You do not have to use a web repo to store packages; you can store everything locally like an animal if you choose. You may simply answer the config questions with bogus info, and instead of uploading packages to the server option, place your packages in the cache folder and use the ```-C``` option to return the sha1 hash with which you can populate your catalog(s).

    ./stew -C ./cache/<package>

Catalogs
--------

Catalogs are json files describing information about your image and passing packages to ```stew``` for processing. Each build requires two catalogs: one providing information about the output name, volume name, and third party packages, and another describing the base OS build number and any available Apple updates. You will reference the os-catalog you want to use inside your custom catalog.  For example, here is a custom catalog:

    {
        "os-catalog": "10.9.2.catalog",
        "volume-name": "OSX10.9.2_13C64",
        "output-name": "OSX10.9.2_13C64.dmg",
        "packages": [
            [
                "create_luser-1.0.pkg",
                "ccb2794e33cc7a3399c5c955da1b6c917ecb1bbe"
            ],
            [
                "apple_setup_done.pkg",
                "3622b983e4d5d718aaf6b2f51fae060e737e1e3f"
            ],
            [
                "command_line_tools_os_x_mavericks_for_xcode__late_october_2013.dmg",
                "cd325ee0b1720064292f2c86687449d0992f245b"
            ]
        ]
    }

This catalog calls out '10.9.2.catalog' as its os-catalog. An os-catalog might look like this:

    {
        "os-installer": "10.9.0_13A603_InstallESD.dmg",
        "packages": [
            [
                "iTunes11.1.5.dmg",
                "d731cabbe1f9213491f3169921a45986ac944e58"
            ],
            [
                "JavaForOSX2013-05.dmg",
                "ce78f9a916b91ec408c933bd0bde5973ca8a2dc4"
            ]
        ]
    }


```stew``` gathers this information, and processes all packages in the os-catalog before moving on to your defined catalog.

If you do not include a ```volume-name``` definition, the default will be "Macintosh HD". If you do not include an ```output-name``` definition, the default will be the $OSVERS of your installer filename (see above).

Runtime
-------

Pass your catalog with the ```-b``` option, and ```stew``` will process the catalog and create an image. You can give it the relative path to the catalog file or simply name it.

    sudo ./stew -b example.catalog
    sudo ./stew -b example
    sudo ./stew -b catalogs/example.catalog
 
 ```stew``` caches the base sparseimage of an OS and saves it to the cache directory, which will speed up subsequent builds.  

Credits
-------

This script was inspired by the awesome work by the [Google Mac Ops team](https://code.google.com/p/google-macops/source/browse/#svn%2Ftrunk%2Fcan_haz_image) and the wonderful [InstaDMG project](https://code.google.com/p/instadmg/).

Also, much credit goes to @MaverValp and his outstanding [AutoDMG application](https://github.com/MagerValp/AutoDMG) (which you should definitely use instead of my half-baked scripts), and his patience with my infinite complaining.

License
-------

    Copyright 2015 Joseph Chilcote
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
