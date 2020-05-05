# Web Crawler
> The automatical web pages screenshooter.

## Table of contents
* [General info](#general-info)
* [Prerequisites](#prerequisites)
* [Specification](#specification)
* [Usage](#Usage)
* [Status](#status)

## General info
Current project is designed to solve the task of automatically gathering of screenshots from web pages. Communication with represented Web Crawler occurs through the console commands, result is being saved in the separate folder automatically created by the program.

Result of the program execution is being saved on disc with one or several screenshots depending on the input data. It could be one URL or list of addresses taken from the file (at current moment this may be a .txt file).

Web Crawler also may find other links from given URL, go through and take screenshots again until the necessary depth of walk.

## Prerequisites
There are several libraries that were connected to the program for correct execution of the task:

```python
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import argparse
import time
import os
```

External libraries:

Webdriver tool is used for automatic control of web browser like opening the browser window when program starts, taking screenshots, rescaling the driver window, scrolling page etc.

Requests library allows to send request to the website and get back response with all the necessary information from the webpage in one variable.

Using BeautifulSoup library helps to parse and find required data, for example necessary tags and attributes of tags that contain links to other pages.

Argparse library simplifies the input data process to start the program. Time is used to just add a short delay between opening page in browser and taking screenshots for fully loading website. Os library is used to automatically creation folders to save output data.


## Specification
To make possible the walk of WebCrawler through the website it’s needed to have on computer one of some web drivers, for example ChromeDriver, and show the way to that driver on disc in __init__() function:

`self.driver_path = "C:\\chromedriver\\chromedriver.exe"`

Walk_control() function contains screenshot_path variable that you may change for other way of saving images:

`screenshot_path = "C:\\Screenshots\\"`

Any path of folders that will be shown here, going to be automatically created by the program if that path not exists. Each website also will have separate folder for screenshots only from that resource.

Walk(url, depth) function contains the most important logical part that makes the program keep take links from the web page, take screenshots, go through the taken addresses and moves through using recursion.

Web Crawler may also work with proxy. In such case it’s needed to add special variables to work with proxy through the Requests library:

```python
def __init__(self):
# To work with proxy in requests library initialize variable
# in current function
self.proxies = {'protocol': 'IP or domain name:port number'}
def walk(self, url, depth):
	# Add this variable as parameter in requests.get method
	response = requests.get(url, proxies=self.proxies)
```

For Selenium webdriver it’s necessary to import an additional library:

```python
# Include the library down below to work with selenium proxy
# Set up proxy setting for webdriver in set_up() function
from selenium.webdriver.common.proxy import Proxy, ProxyType

def set_up(self):
	if not self.is_crawler_started:
		# Manually set parameters of proxy for web driver:
		proxy = Proxy()
		proxy.proxy_type = ProxyType.MANUAL
		proxy.http_proxy = "ip_address:port"
		proxy.socks_proxy = "ip_address:port"
		proxy.ssl_proxy = "ip_address:port"
		capabilities = webdriver.DesiredCapabilities.CHROME
		proxy.add_to_capabilities(capabilities)
		# Add capabilities as parameter in driver initialization
self.driver = webdriver.Chrome(self.driver_path,
desired_capabilities=capabilities)
```

## Usage
Program may be started by the next terminal command that should help to get all the necessary information about input data:

`(venv) C:\crawler\>python main.py --help`

Taking a single screenshot with next command:

`(venv) C:\crawler\>python main.py https://www.apple.com --depth 0`

This command will create automatically a folder with a top part of the website screenshot.

To get the images of whole the page with several screenshots just add command --fullpage parameter:

`(venv) C:\crawler\>python main.py https://www.apple.com --depth 0 --fullpage`

It’s allowed to give the program a list of URLs from the file, and program will create automatically the folder for each URL from the list:

`(venv) C:\crawler\>python main.py C:/default.txt --depth 0 --fullpage`

By using another depth instead of 0, you’ll get all the screenshots of webpages in one folder.

(!)	At current moment if you didn’t remove previous folders before the next execution, you’ll get an FileExistsError because your folder with name 1 exists (all images and folders get names by default with 1, 2, 3… etc.).

## Status
Project is: frozen

At current moment work on project is stopped.