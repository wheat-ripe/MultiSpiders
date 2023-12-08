import copy
import os.path
from pathlib import Path

import scrapy.crawler
from scrapy.commands import BaseRunSpiderCommand
from scrapy.exceptions import UsageError
from scrapy.settings import Settings
from scrapy.utils.conf import closest_scrapy_cfg


class Command(BaseRunSpiderCommand):
    requires_project = True

    def syntax(self):
        return "[options] [module] [spider]"

    def short_desc(self):
        return "Run all spider"

    def run(self, args, opts):
        if len(args) > 2:
            raise UsageError("running 'scrapy crawlall [module] [spider]' to crawl")

        # 该目录结构一定: scrapy.utils.project.inside_project() == True
        # 暂未使用从该文件获取根目录
        projdir = str(Path(closest_scrapy_cfg()).parent)
        if not os.path.exists(projdir):
            raise UsageError("running 'scrapy crawlall', this project structure illegal")
        base_setting = copy.deepcopy(self.crawler_process.settings)

        if len(args) == 0:
            self.run_all(opts, projdir, base_setting)
        elif len(args) == 1:
            if not os.path.exists(projdir + '/' + args[0]) \
                    or not os.path.exists(projdir + '/' + args[0] + '/settings.py'):
                raise UsageError(f"running 'scrapy crawlall [module] [spider]', module {args[0]} no exist")
            else:
                self.run_module(args, opts, base_setting)
        elif len(args) == 2:
            if not os.path.exists(projdir + '/' + args[0]) \
                    or not os.path.exists(projdir + '/' + args[0] + '/settings.py'):
                raise UsageError(f"running 'scrapy crawlall [module] [spider]', module {args[0]} no exist")
            else:
                self.run_module_spider(args, opts, base_setting)

    def run_module_spider(self, args, opts, base_setting):
        module = args[0]
        spider = args[1]
        new_settings = Settings()
        new_settings.setmodule(module + '.settings', priority="spider")
        merge_setting = Settings(base_setting)
        merge_setting.update(new_settings)
        self.crawler_process.settings = merge_setting
        self.crawler_process.spider_loader = scrapy.crawler.CrawlerRunner._get_spider_loader(merge_setting)
        if spider not in self.crawler_process.spider_loader.list():
            raise UsageError(f"running 'scrapy crawlall [module] [spider]', {module} {spider} no exist")

        print(f'********* crawl spider : {module}.{spider} *********')
        crawl_defer = self.crawler_process.crawl(spider, **opts.spargs)
        if getattr(crawl_defer, "result", None) is not None and issubclass(
                crawl_defer.result.type, Exception
        ):
            print(f'********* crawl spider fail : {module}.{spider} *********')
            self.exitcode = 1
        else:
            self.crawler_process.start()

            if (
                    self.crawler_process.bootstrap_failed
                    or hasattr(self.crawler_process, "has_exception")
                    and self.crawler_process.has_exception
            ):
                self.exitcode = 1

    def run_module(self, args, opts, base_setting):
        module = args[0]
        can_start = True
        new_settings = Settings()
        new_settings.setmodule(module + '.settings', priority="spider")
        merge_setting = Settings(base_setting)
        merge_setting.update(new_settings)
        self.crawler_process.settings = merge_setting
        self.crawler_process.spider_loader = scrapy.crawler.CrawlerRunner._get_spider_loader(merge_setting)
        spider_loader = self.crawler_process.spider_loader
        for spider_name in spider_loader.list():
            print(f'********* crawl spider : {module}.{spider_name} *********')
            ##
            crawl_defer = self.crawler_process.crawl(spider_name, **opts.spargs)
            if getattr(crawl_defer, "result", None) is not None and issubclass(
                    crawl_defer.result.type, Exception
            ):
                print(f'********* crawl spider fail : {module}.{spider_name} *********')
                can_start = False

        if not can_start:
            self.exitcode = 1
        else:
            self.crawler_process.start()

            if (
                    self.crawler_process.bootstrap_failed
                    or hasattr(self.crawler_process, "has_exception")
                    and self.crawler_process.has_exception
            ):
                self.exitcode = 1

    def run_all(self, opts, projdir, base_setting):

        can_start = True
        for module in os.listdir(projdir):
            if os.path.isfile(module):
                continue
            if module == 'commands' or module == 'venv' or module.startswith('__') \
                    or not os.path.exists(projdir + '/' + module + '/settings.py'):
                continue
            new_settings = Settings()
            new_settings.setmodule(module + '.settings', priority="spider")
            merge_setting = Settings(base_setting)
            merge_setting.update(new_settings)
            self.crawler_process.settings = merge_setting
            # self.crawler_process.spider_loader = self.crawler_process._get_spider_loader(merge_setting)
            self.crawler_process.spider_loader = scrapy.crawler.CrawlerRunner._get_spider_loader(merge_setting)
            spider_loader = self.crawler_process.spider_loader
            # for spidername in args or spider_loader.list():
            for spider_name in spider_loader.list():
                print(f'********* crawl spider : {module}.{spider_name} *********')
                ##
                crawl_defer = self.crawler_process.crawl(spider_name, **opts.spargs)
                if getattr(crawl_defer, "result", None) is not None and issubclass(
                        crawl_defer.result.type, Exception
                ):
                    print(f'********* crawl spider fail : {module}.{spider_name} *********')
                    can_start = False
        if not can_start:
            self.exitcode = 1
        else:
            self.crawler_process.start()

            if (
                    self.crawler_process.bootstrap_failed
                    or hasattr(self.crawler_process, "has_exception")
                    and self.crawler_process.has_exception
            ):
                self.exitcode = 1
