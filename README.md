# scrapy-game-information
A project based on scrapy which crawl game's information from store.steampowered.com
![image](https://github.com/gonggqing/scrapy-game-information/blob/main/game%20reviews.png)
A total visualization of this project, only select several game names to show
## Scrapy
I created two spiders, one nmaed [steamtopsell.py](https://github.com/gonggqing/scrapy-game-information/blob/main/steamtopsell.py) helps me to get all the game urls from the website, it crawled almost 4000 urls, saved as a [.txt file](https://github.com/gonggqing/scrapy-game-information/blob/main/games_url.txt). The other named [steam_game.py](https://github.com/gonggqing/scrapy-game-information/blob/main/steam_game.py), it helps me to get all the information that I want from a specific game url, which contains game name, game type, developer, evaluation and so on. You can create your spider use this command in shell (I'm using Mac Bigsur, Apple silicon M1)
```

$ pip install scrapy # wait till installation finished
$ cd . # current directory
$ scrapy startproject your_project
$ cd your_project 
$ scrapy genspider spider_name store.steampowered.com # create your spider with the website you want to crawl

# now you can customize your spider through my code here 'steamtopsell.py', 'steam_game.py'(not standard enough)
# or you can explore more details in [scrapy tutorial](https://docs.scrapy.org/en/latest/intro/tutorial.html)
# after that you can crawl the websites, using code below
$ scrapy crawl spider_name [, -o output.json]

```

## MySQL & Tableau
After I got my data from the website, I stored my data in MySQL database, and create a visualization dashboard in Tableau.
![image](https://github.com/gonggqing/scrapy-game-information/blob/main/nysql_games_info.png)
Spreadsheet in MySQL

![image](https://github.com/gonggqing/scrapy-game-information/blob/main/games_info.png)
Game information details, sorted by recent reviewers count

![image](https://github.com/gonggqing/scrapy-game-information/blob/main/game%20types.png)
Game types that have most players

First project on my github. Thank you for watching.
