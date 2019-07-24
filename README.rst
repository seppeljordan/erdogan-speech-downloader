What?
=====

Download all speeches by Recep Tayyip Erdoğan from tccb.gov.tr as txt
files.


How?
====

We crawl the overview page to retrieve a list of all speeches and the
we download individual speeches via their links.


Installation
============

Currently this is a simple python script.


Debian/Ubuntu
=============

First create a folder where you want to download the speeches into.
In this guide we will use the folder ``~/speeches/`` The speeches will
be downloaded after you entered the following commands::
   sudo apt install python3-virtualenv
   mkdir -p ~/speeches
   cd ~/speeches
   virtualenv env
   source env/bin/activate
   git clone 'https://github.com/seppeljordan/erdogan-speech-downloader.git' code
   pip install -r code/requirements.txt
   python code/crawl.py
