from scrapy.cmdline import execute

# 基于用户id搜索： 第一位：type = 1 第二位：用户名  第三位：用户id 第四位：页数 第五位：是否要图片
# 例子：   1,重庆发布,1988438334,3,True
# 基于关键词搜索：  第一位：type = 2   第二位：关键词    第三位：1-综合 60-热门 61-实时  第四位：页数 第五位：是否要图片
# 例子    2,天盛长歌,60,3,True
execute("scrapy crawl weibo -a line=2,Olay,60,20,False@_@".split(' '))

# 基于微博id抓取转发内容：第一位：名称（建议:微博名_时间），第二位：微博id，第三位：页数
# execute(("scrapy crawl weibo_repost -a line=中国工商_180525,4243466675856175,20@_@").split(' '))
