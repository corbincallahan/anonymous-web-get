# anonymous-web-get

Written by Corbin Callahan and Jack Fraser for CS457 fall 2020

Usage
* To run a 'stepping stone' server: python3 ss.py -p ####
  * port is optional, numeric only, default is 54321 when not specified
* To make request using awget: python3 awget.py URL -c FileName
  * URL is mandatory, specify file to fetch
  * -c is optional, specifies a chainfile to use, default is chaingang.txt when not specified


Because wget is not installed on the cs department machines, we used the requests library instead. This library requires that http or https is specified at the beginning of the url, so we add "http://" if a schema is not given.

The temporary files created by the stepping stones will include host and port in the filename. This is to avoid deleting the file as the next stepping stone is trying to write it, as all stepping stones are running in the same directory.
