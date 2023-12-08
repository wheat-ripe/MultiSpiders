from scrapy.cmdline import execute

# execute(['scrapy', 'crawlall'])
# execute(['scrapy', 'crawlall', 'scrapydownloadertest'])
# execute(['scrapy', 'crawlall', 'scrapydownloadertest', 'httpbin'])

execute(['scrapy', 'crawlall', 'images360', 'images'])

if __name__ == '__main__':
    execute()
