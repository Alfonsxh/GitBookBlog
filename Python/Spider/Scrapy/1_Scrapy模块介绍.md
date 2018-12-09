# Scrapy(1)-模块介绍

之前一直使用 **requests + re** 的方式做爬虫……所有的步骤：访问、分析结果、存储结果、多进程、异步等等，都是自己实现的……最大的坑莫过于 **正则匹配**，虽说 **正则** 很强大，但是经常会出现一些异常的数据。另外，爬取不同的网站，又得重新来一套！！

## Scrapy介绍

**Scrapy** 是一个为了爬取网站数据，提取结构性数据而编写的应用框架。 可以应用在包括数据挖掘，信息处理或存储历史数据等一系列的程序中。

![scrapy_architecture](/Image/Python/Scrapy/scrapy_architecture.png)

上图为 **Scrapy** 的整体架构图，各部分组件的主要功能如下：

- **Scrapy Engine(引擎)** - 引擎负责 **控制数据流在系统中所有组件中的流动**，并在相应动作发生发生时触发事件。数据流详细的处理流程见下面的 **数据流** 部分。
- **Scheduler(调度器)** - 调度器从引擎接受 **request** 并将他们入队，以便之后引擎请求它们时提供给引擎。
- **Downloader(下载器)** - 下载器负责获取页面的数据并提供给引擎，然后返回 **response** 经过引擎传递给 **spiders** 处理分析。
- **Spiders(结果分析)** - **Spiders** 由 **用户编写**，分析 **下载器** 返回的 **response**，从中提取 **item** 交由 **Item Pipeline** 处理，或者继续跟进 **url**，返回 **request** 给 **Scheduler**。
- **Item Pipeline(管道)** - 负责处理 **Spiders** 分析后返回的 **Item**。典型的处理有清理、验证及持久化(存取到数据库中)。
- **Downloader middlewares(下载中间件)** - 位于 **引擎** 和 **下载器** 之间，用于处理 **引擎发送给下载器的request** 和 **下载器返回的response**。
- **Spider middlewares(爬虫中间件)** - 位于 **引擎** 和 **Spiders** 之间，用于处理 **Spiders的输入(response)和输出(items或request)**。

数据流解析：

- 1、引擎打开一个网站，找到处理该网站的 **Spider**，并向该 **spider** 请求第一个要爬取的 **URL(s)(start_urls参数指定)**。之后引擎从 **Spider** 中获取到第一个要爬取的URL，并在 **调度器(Scheduler)** 以 **request调度**。
- 2、引擎向调度器请求下一个要爬取的URL。
- 3、调度器返回下一个要爬取的URL给引擎。
- 4、引擎将URL通过 **下载中间件(response)** 转发给 **下载器(Downloader)**。
- 5、一旦页面下载完毕，下载器生成一个页面的 **response**，并将其通过 **下载中间件(response)** 发送给引擎。
- 6、引擎将返回的 **response** 通过 **Spider中间件** 传递给 **Spider** 处理分析。
- 7、**Spider** 处理完后通过 **Spider中间件** 返回爬取到的 **Item** 及跟进的新的 **request** 给引擎。
- 8、引擎将返回的 **Item** 交由 **Item Pipeline** 处理，返回的 **request** 交给调度器存储。
- 9、从第二步开始，重复该过程，知道调度器没有更多的 **request**，引擎关闭该网站。

整个 **Scrapy** 由非阻塞的方式实现，基于事件驱动网络框架 [Twisted](https://twistedmatrix.com/trac/)编写。

对于简单的应用来说，用户需要只需要在 **spider** 中完成处理引擎发来的 **response** 的功能，以及 **Item Pipeline** 中处理引擎传来的数据即可。

![scrapy_assembly](/Image/Python/Scrapy/scrapy_assembly.png)

## 组件

**Scrapy** 的主要组件都在上面的图中了。下面主要结合爬取 [起点中文网](https://www.qidian.com/) 介绍可能需要用户实现的部分组件。

### Spider

**Spider类** 定义了如何爬取网站。包括爬取的动作(是否跟进爬取网站中的链接)，以及如何从网页中提取结构化的数据(item)。**Spider** 就是 **定义爬取的动作及分析网页的地方**。

整个 **Scrapy** 框架的起点是 **start_requests函数**，它的作用是处理 **start_urls** 中定义的起始url，返回 **request** 给引擎。当然，也可以 **重写start_requests函数**，自己处理。

**start_requests函数** 的代码如下，首先判断是否重写了 **make_requests_from_url函数**，重写了就用它处理 **start_urls列表** 中的url。否则，返回 **Request** 对象给引擎。

```python
def start_requests(self):
    cls = self.__class__
    if method_is_overridden(cls, Spider, 'make_requests_from_url'):
        warnings.warn(
            "Spider.make_requests_from_url method is deprecated; it "
            "won't be called in future Scrapy releases. Please "
            "override Spider.start_requests method instead (see %s.%s)." % (
                cls.__module__, cls.__name__
            ),
        )
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    else:
        for url in self.start_urls:
            yield Request(url, dont_filter=True)
```

**parse函数** 是用来处理 **下载器** 下载完网页内容后返回的 **response**。它可以继续爬取 **response** 中的 **嵌套url链接**，此时给引擎返回 **resquest**。也可以返回 **item** 给引擎，进入数据本地化存储流程。

**parse函数** 必须由子类实现！

```python
# Spider基类中的parse函数
def parse(self, response):
        raise NotImplementedError('{}.parse callback is not defined'.format(self.__class__.__name__))
```

所以呢，最开始部分可以有两种实现：

```python
# 1、不重写start_requests方式
class QidianSpider(scrapy.Spider):
    name = "qidian"
    start_urls = [
        "https://www.qidian.com/all?orderId=&page=1&style=2&pageSize=20&siteid=1&pubflag=0&hiddenField=0"
    ]

    def parse(self, response):
        max_page = response.css(".lbf-pagination-item").xpath("./a/text()")[-2].extract()

        for page in range(1, int(max_page) + 1):
            page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page = page)
            yield scrapy.Request(url = page_url, callback = self.parse_page)

    def parse_page(self, response):
        pass

# 2、重写start_requests方式
class QidianSpider(scrapy.Spider):
    name = "qidian"

    def start_requests(self):
        begin_url = "https://www.qidian.com/all?orderId=&page=1&style=2&pageSize=20&siteid=1&pubflag=0&hiddenField=0"
        yield scrapy.Request(url = begin_url, callback = self.parse)

    def parse(self, response):
        max_page = response.css(".lbf-pagination-item").xpath("./a/text()")[-2].extract()

        for page in range(1, int(max_page) + 1):
            page_url = "https://www.qidian.com/all?orderId=&style=2&pageSize=50&siteid=1&pubflag=0&hiddenField=0&page={page}".format(page = page)
            yield scrapy.Request(url = page_url, callback = self.parse_page)

    def parse_page(self, response):
        pass
```

在处理嵌套中的链接时，当下载器返回 **对应链接的response** 时，会调用 **对应链接的回调函数** 进行处理。回调函数的功能和 **parse函数** 的功能类似，只不过 **parse函数** 是此类调用的总入口。

### Item Pipelines

这里其实是分为两部分： **Item** 和 **Pipelines**。

#### Item

爬虫的主要目的就是 **从非结构化的数据源中提取结构性的数据**。虽然也可以使用 **dict** 来返回提取的数据，但其缺少结构性，容易出错。

**Item** 对象是种简单的容器，保存了爬取得到的数据，提供了 **类似于字典** 的API以及用来声明可用字段的简单语法。

```python
import scrapy


class ScrapyframetestItem(scrapy.Item):
    # define the fields for your item here like:
    man_type = scrapy.Field()  # 主类型
    sub_type = scrapy.Field()  # 副类型
    novel_name = scrapy.Field()  # 小说名称
    novel_link = scrapy.Field()  # 小说链接
    novel_id = scrapy.Field()  # 小说ID标识
    author_name = scrapy.Field()  # 作者名称
    author_link = scrapy.Field()  # 作者链接
    author_id = scrapy.Field()  # 作者ID标识
```

**Item** 有点儿类似于 **Django中的Model**，不过没有那么多不同的字段类型(Field type)，更为简单。

它的存取和字典是一样的。

```python
item = ScrapyframetestItem(man_type = "科幻", sub_type = "机甲", novel_name = "One pis", novel_link = "http://1234.com",
                            novel_id = "123", author_name = "lufei", author_link = "http://232455.com", author_id = "321")
print("item:\n", item)
print("\nOld name:\n", item["novel_name"])

item["novel_name"] = "Dragon Ball"
print("\nNew name:\n", item.get("novel_name", "attr not exist!"))

print("\nNew name:\n", item.get("novel", "attr not exist!"))

# output:
# item:
#  {'author_id': '321',
#  'author_link': 'http://232455.com',
#  'author_name': 'lufei',
#  'man_type': '科幻',
#  'novel_id': '123',
#  'novel_link': 'http://1234.com',
#  'novel_name': 'One pis',
#  'sub_type': '机甲'}
#
# Old name:
#  One pis
#
# New name:
#  Dragon Ball
#
# New name:
#  attr not exist!
```

#### Pipeline

**Pipeline** 模块用来处理在 **Spider** 中收集的 **Item** 对象。

用户可以在 **Pipeline** 中

- 清理HTML数据
- 验证爬取的数据
- 查重并丢弃
- 将爬取的结果存储到数据库中

每个 **Pipeline** 都是一个单独的类，它不继承任何其他的基类。在使用时，需要先激活，在 **setting.py** 配置文件中指定 **ITEM_PIPELINES** 参数。后面的数字表示的是运行的优先级，**数字越小优先级越高**，范围为 **0-1000**。

```python
ITEM_PIPELINES = {
    'ScrapyFrameTest.QidianPipelines.pipelines.ScrapyframetestPipeline': 1,
   # 'ScrapyFrameTest.pipelines.ScrapyframetestPipeline': 300,
}
```

在用户编写的 **Pipeline** 类中必须实现 ***process_item(self, item, spider)*** 函数。该函数在处理时，要么返回 **item对象**，要么抛出 **DropItem** 异常。被丢弃的 **item** 将不会被之后的pipeline组件处理。

如下，实现的是 **pipeline** 处理 **item**，首先判断传入的item是否是指定的类型，如果不是则抛出 **DropItem** 异常。如果是指定类型，则将每部小说的信息从item中取出存入mysql中。

```python
def process_item(self, item, spider):
    if isinstance(item, ScrapyframetestItem):
        novel_id = item["novel_id"]
        novel_name = item["novel_name"]
        novel_link = item["novel_link"]
        man_type = item["man_type"]
        sub_type = item["sub_type"]
        author_id = item["author_id"]
        author_name = item["author_name"]
        author_link = item["author_link"]

        QidianDb.insert_table(novel_id = novel_id,
                                novel_name = novel_name,
                                novel_link = novel_link,
                                man_type = man_type,
                                sub_type = sub_type,
                                author_id = author_id,
                                author_name = author_name,
                                author_link = author_link)
        return item
    else:
        raise DropItem("Item type not allow!")
```

**Pipeline组件** 还有其他的几个函数可以实现：

- **open_spider(self, spider)** - 在 **Spider开启时** 被自动调用，用户可以在这里进行一些诸如开启数据库的操作。
- **close_spider(self, spider)** - 在 **Spider关闭时** 被自动调用，用户可以在这里做一些收尾工作，如关闭数据库操作。
- **from_crawler(cls, crawler)** - 这是一个类方法，需使用 **@classmethod** 装饰。它的传入参数 **crawler** 包含了scrapy的所有核心组件信息。最后需要返回一个 **pipeline** 实例。

```python
def open_spider(self, spider):
    print("Begin Spider!")
    QidianDb.OpenDB()

def close_spider(self, spider):
    print("End Spider!")
    QidianDb.CloseDB()
```

### Downloader Middleware

// todo

### Spider Middleware

// todo

## 参考

- [Scrapy 1.5 documentation](https://doc.scrapy.org/en/latest/index.html)
- [Python爬虫之Scrapy学习（基础篇）](https://juejin.im/post/5ad41ff7f265da23945ff1a6)