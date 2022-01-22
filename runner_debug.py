import os
from scrapy.cmdline import execute

os.chdir(os.path.dirname(os.path.realpath(__file__)))

try:
    execute(
        [
            'scrapy',
            'crawl',
            'quotes_ajax', # The name your spider (in files belong to spiders folder)
            '-o',
            'out.json',
        ]
    )
except SystemExit:
    pass