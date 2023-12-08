import argparse
import os.path
import sys


def structs():
    parser = argparse.ArgumentParser()
    if len(sys.argv) != 3:
        parser.add_argument("source-spider", help="source spider project directory")
        parser.add_argument("target-spider", help="target spider project directory")
        parser.print_help()
        # args = parser.parse_args()
        # print(args)
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]
    if not (os.path.exists(source) and os.path.isdir(source) and os.path.exists(target)):
        parser._print_message('source spider project directory not exist')
        sys.exit(1)
    if not (os.path.exists(target) and os.path.isdir(target)):
        parser._print_message('target spider project directory not exist')

    paths = source.split('/')
    spider = paths[-1]

    paths = target.split('/')
    target_spider = paths[-1]

    source = source + '/' + spider
    target = target + '/' + target_spider

    os.makedirs(target + '/' + spider.lower(), exist_ok=True)
    print('create directory : ' + target + '/' + spider)

    items = 'cp {} {}'.format(source + '/items.py', target + '/' + spider)
    r = os.system(items)
    print(items + '\t' + str(r))
    middlewares = 'cp {} {}'.format(source + '/middlewares.py', target + '/' + spider)
    r = os.system(middlewares)
    print(middlewares + '\t' + str(r))
    pipelines = 'cp {} {}'.format(source + '/pipelines.py', target + '/' + spider)
    r = os.system(pipelines)
    print(pipelines + '\t' + str(r))
    settings = 'cp {} {}'.format(source + '/global.py', target + '/' + spider)
    r = os.system(settings)
    print(settings + '\t' + str(r))
    spiders = 'cp -r {} {}'.format(source + '/spiders/*', target + '/spiders')
    r = os.system(spiders)
    print(spiders + '\t' + str(r))


def structs_2():
    parser = argparse.ArgumentParser()
    if len(sys.argv) != 3:
        parser.add_argument("source-spider", help="source spider project directory")
        parser.add_argument("target-spider", help="target spider project directory")
        parser.print_help()
        # args = parser.parse_args()
        # print(args)
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]
    if not (os.path.exists(source) and os.path.isdir(source) and os.path.exists(target)):
        parser._print_message('source spider project directory not exist')
        sys.exit(1)
    if not (os.path.exists(target) and os.path.isdir(target)):
        parser._print_message('target spider project directory not exist')

    spiders = 'cp -r {} {}'.format(source, target)
    r = os.system(spiders)
    print(spiders + '\t' + str(r))


# python3 addspider.py /Users/michael/tmp/ScrapyDownloaderTest
# /Users/michael/ws_code/python/Python3WebSpider/MutilSpiders
if __name__ == '__main__':
    structs()
    # structs_2()
