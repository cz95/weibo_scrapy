from scrapy.cmdline import execute

# 基于用户id搜索： 第一位：type = 1 第二位：用户名  第三位：用户id 第四位：页数 第五位：是否要图片
# 例子：   1,重庆发布,1988438334,3,True
# 基于关键词搜索：  第一位：type = 2   第二位：关键词    第三位：1-综合 60-热门 61-实时  第四位：页数 第五位：是否要图片
# 例子    2,天盛长歌,60,3,True

# execute(("scrapy crawl weibo -a line=1,重庆发布,1988438334,3,True@_@").split(" "))

# 爬取当前微博转发信息 第一位：项目名（一般微博名+日期） 第二位：微博id  第三位：转发页码（一页一般十条信息）
# execute(("scrapy crawl weibo_repost -a line=中国工商_180525,4243466675856175,20@_@").split(" "))

# 爬取当前微博评论信息 第一位：项目名（一般微博名+日期） 第二位：微博id  第三位：评论页码（一页一般十条信息）
execute(("scrapy crawl weibo_comment -a line=央视新闻_190218,4341018118015865,20@_@").split(" "))
