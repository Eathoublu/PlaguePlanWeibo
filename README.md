# PlaguePlanWeibo
微博瘟疫计划(PlaguePlanWeibo)的爬虫源码，该计划通过爬取微博的四亿月活用户分析微博网络人际关系。The source code of PlaguePlanWeibo ,which is a project to analyse relationships between users on the internet. 

## how to use
1. run python script in the terminal. '''python weibo_user_spider.py''' It will automantically run.
2. Also, you can import these classis into your own script to run it.make sure all classes in all files is included.
3. If you use the method mentioned in the part2, here's some note of using the main class UserSpider:
  - First, get a instance of this class."""example = UserSpider()"""
  - Use """example.run()""" to quickly start.
  - Sometimes, the cookie pre-set in the hardcode will be out of date.Use "example.setcookies(<new cookie string>)"to set a new cookie(domain:https://weibo.cn)for the script.
4. Ensure that all files is in the same workplace.

## how it work
1. It takes a method like "mining" in the blockchain tech, which means you can stop or start any time you like.It is fully data-drive.Any time you start the process, you mine users on the server,new task sheet will be ramdomly generated.It will never store the last step before you stop the process last time, which is a state-of-art mechanism.
2. It takes sqlite as its database.change the database to mysql might allowed it to work in DCS.

## Enjoy it!
