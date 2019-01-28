from scrapy.cmdline import execute

# execute(["scrapy", "crawl", "weibo", "-a",
#          "line='2,天盛长歌,60,2,False@_@2,重庆,61,2,False'"])

execute(["scrapy", "crawl", "weibo_repost", "-a",
         "line='中国工商_180525,4243466675856175,20@_@'"])
