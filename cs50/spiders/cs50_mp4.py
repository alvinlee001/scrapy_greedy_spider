# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
import urllib
import re

class CS50Mp4Scrapper(scrapy.Spider):
    name = "cs50_mp4"
    start_urls = [
        'https://cdn.cs50.net/ai/',
    ]

    custom_settings = {
        'DEPTH_LIMIT': 20
    }

    def __init__(self):
        self.history = set()

    def parse(self, response):
        links = response.css('a::attr(href)').getall()
        with open('cs50_result.txt', 'a') as result_file:
            with open('cs50_links.txt', 'a') as links_file:
                self.log('links: %s' % links)
                for next_page in links:
                    self.log('next_page: %s' % next_page)
                    if (next_page is '/'
                        or re.search(r"\.\.", next_page) is not None
                        or next_page in self.history):
                        continue
                    if next_page is not None:
                        next_page = response.urljoin(next_page)
                        self.log('parsing Url: %s' % response.url)
                        if re.search(r"720p\.mp4$", next_page) is not None:
                            result_file.write(next_page)
                            result_file.write('\n')
                        if (
                            re.search("(\?torrent|\?download|\?highlight|\.png|\.mp3|\.mp4|\.jpg|\.sha|\.md5|\.zip|\.txt|\.py|\.ttf|\.html|\.srt|\.csv|\.json|\.sha1|\.sha256|\.webm|\.pdf|\.vtt|\.css|\.gif|\.js|\.db|\.sqlite|\.h5|\.adoc|\.xml|\.wav|\.lua|\.pptx|\.db|\.c|\.sql|\.cs|\.meta|\.unity|\.fbx|\.prefab|\.webm|\.mat|\.FBX|\.asset|\.otf|\.tga|\.controller|\.otf)$", next_page) is None
                            and re.search("\#", next_page) is None
                            and re.search("lang$", next_page) is None
                            and re.search("lang\/$", next_page) is None
                            and not (next_page in self.history)
                            and self.is_child(next_page)
                            ):
                            self.history.add(next_page)
                            links_file.write(next_page)
                            links_file.write('\n')
                        #if re.search(r"\/$", next_page) is not None:
                            yield scrapy.Request(next_page, callback=self.parse, dont_filter=True)

    def is_child(self, page):
        for url in self.start_urls:
            if re.search(url, page) is not None:
                return True
        return False
