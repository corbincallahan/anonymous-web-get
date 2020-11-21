# anonymous-web-get

Written by Corbin Callahan and Jack Fraser for CS457 fall 2020

Because wget is not installed on the cs department machines, we used the requests library instead. This library requires that http or https is specified at the beginning of the url, so we add "http://" if a schema is not given.

The temporary files created by the stepping stones will include host and port in the filename. This is to avoid deleting the file as the next stepping stone is trying to write it, as all stepping stones are running in the same directory.
