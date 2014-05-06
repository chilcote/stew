stew.py
=======

This script processes catalog(s) of packages, verifies the sha1 hash of each package, downloads any missing or updated packages, 
and compiles a new image consisiting of a given base OS X installer and the list of packages.

Requirements
------------
+ 10.9.x (you must build your images on a matching system)  
+ python 2.7  
+ InstallESD.dmg must be renamed in the format OSVERS_OSBUILD_InstallESD.dmg  
```
InstallESD.dmg -> 10.9.2_13C64_InstallESD.dmg
```  

Usage
-----

	Usage: sudo ./stew.py [options]

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
When you run ```stew.py``` for the first time, or with the ```-c``` option, you will be asked to populate a config file.  This file is stored at ```~/.stew_config``` and will be recreated any time you use the ```-c``` option. This facilitates the uploading of packages using ```scp```, so setting up a key-based login for your webserver is highly recommended.  

You will be asked to provide the following information:  

+ The FQDN of your webserver (example: mypackagerepo.mycorp.com)
+ The full path of your remote repo folder (example: /var/www/html/packages)  
	+ the web repo is just one single folder, which will contain all OS Installers, packages, and disk images  
+ The login user for your webserver (example: stewuser)

Uploading packages
------------------
You may upload packages with the ```-u``` option, or you may wish to copy the companion ```uptodate.py``` script to your $PATH and run that with the path to the package as its singular argument:  

	uptodate.py /path/to/package

Storing packages locally
------------------------
You do not have to use a web repo to store packages; you can store everything locally like an animal if you choose. You may simply answer the config questions with bogus info, and instead of uploading packages to the server option, place your packages in the cache folder and use the ```-C``` option to return the sha1 hash with which you can populate your catalog(s).  

	./stew.py -C ./cache/<package>

Catalogs
--------

Catalogs are plain text files describing the packages, and ```stew.py``` processes the catalog entries in the order listed. Specific catalog entries can be used to pass information to the script. For example:   

	base-installer: 10.9.2_13C64_InstallESD.dmg    
	base-catalog: 10.9.2.catalog  
	volume-name: 10.9.2  
	output-name: 10.9.2.dmg  

The only required definition is ```base-installer``` which can also be in your nested catalog. If you do not include a ```volume-name``` definition, the default will be "Macintosh HD". If you do not include an ```output-name``` definition, the default will be the OSVERS of your installer filename (see above).  

Packages are defined in the catalog with a name and sha1 hash, separated by spaces. For example:  

	create_luser-1.0.pkg ccb2794e33cc7a3399c5c955da1b6c917ecb1bbe
	apple_setup_done.pkg 3622b983e4d5d718aaf6b2f51fae060e737e1e3f
	command_line_tools_os_x_mavericks_for_xcode__late_october_2013.dmg cd325ee0b1720064292f2c86687449d0992f245b 

Runtime
-------
Pass your catalog with the ```-b``` option, and ```stew.py``` will process the catalog and create an image. You can give it the relative path to the catalog file or simply name it.  

	./stew.py -b 10.9.2.catalog
	./stew.py -b cache/example.catalog
 
 ```stew.py``` caches the base sparseimage of an OS and saves it to the cache directory, which will speed up subsequent builds.  

Credits
-------

This script was inspired by the awesome work by the [Google Mac Ops team](https://code.google.com/p/google-macops/source/browse/#svn%2Ftrunk%2Fcan_haz_image) and the wonderful [InstaDMG project](https://code.google.com/p/instadmg/).

Also, much credit goes to @MaverValp and his outstanding [AutoDMG application](https://github.com/MagerValp/AutoDMG) (which you should definitely use instead of my half-baked script), and his patience with my infinite complaining. 

License
-------

	Copyright 2014 Joseph Chilcote
	
	Licensed under the Apache License, Version 2.0 (the "License");
	you may not use this file except in compliance with the License.
	You may obtain a copy of the License at
	
		http://www.apache.org/licenses/LICENSE-2.0
	
	Unless required by applicable law or agreed to in writing, software
	distributed under the License is distributed on an "AS IS" BASIS,
	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
	See the License for the specific language governing permissions and
	limitations under the License.
