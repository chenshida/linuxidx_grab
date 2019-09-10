#!/usr/bin/python3
# -*- coding: utf-8 -*-
__Author__ = 'csd'
__version__ = "1.0"
__data__ = "2019.09.04"

import os
import sys
from scrapy import cmdline

def main():
    cmdline.execute('scrapy crawl graber'.split())


if __name__ == "__main__":
    main()
