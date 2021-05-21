import scrapy
import pandas as pd

class SteamGameSpider(scrapy.Spider):
    name = 'steam_game'
    allowed_domains = ['store.steampowered.com/']

    def start_requests(self):
        # 只放了几个url，通过steamtopsell.py爬取的urls保存在games_url.txt/csv文件中
        start_urls = ["https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/",
                      "https://store.steampowered.com/sub/124923/",
                      "https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/",
                      "https://store.steampowered.com/app/1259420/Days_Gone/",
                      "https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/",
                      "https://store.steampowered.com/app/292030/The_Witcher_3_Wild_Hunt/",
                     ]
        for url in start_urls:
            yield scrapy.Request(str(url), callback=self.parse)

    def parse(self, response):
        # 先给字典中的字段分配空间，有些url不存在该字段会报错（不影响运行）
        game_name,release_date,price,recent_eval,counts_re,total_eval = response.url, None,None,None,None,None
        counts_all,game_type,developers,publishers,overall,recent = None,None,None,None,None,None
        # 游戏名
        game_name = response.xpath("//div[contains(@class, 'apphub_HomeHeaderContent')]\
        //div[contains(@class, 'apphub_AppName')]/text()").extract_first()
        # 发售日期
        release_date = response.xpath("//div[contains(@class, 'release_date')]\
        //div[contains(@class, 'date')]/text()").extract_first()
        # 价格
        price = response.xpath("//div[contains(@class, 'game_purchase_action')]\
        //div[contains(@class, 'game_purchase_price price')]/text()").extract_first()
        # 是否有折扣
        discount_price = response.xpath("//div[contains(@class, 'game_purchase_action')]\
        //div[contains(@class, 'discount_final_price')]/text()").extract_first()
        # 只保留当前折扣价格
        if discount_price is not None:
            price = discount_price
        # 游戏评价
        eval = response.xpath("//div[contains(@class, 'user_reviews_summary_row')]/@data-tooltip-html")
        if eval is not None:
            if len(eval)==2:
                recent_eval, total_eval = eval.extract()
            else:
                total_eval = eval.extract()
        # 总体测评
        overall_ = response.xpath("//div[contains(@id, 'review_histograms_container')]\
        //div[contains(text(), 'Overall')]/following-sibling::span/text()").extract()
        if  overall_ != []:
            if len(overall_)==2:
                overall, counts_all = response.xpath("//div[contains(@id, 'review_histograms_container')]\
                //div[contains(text(), 'Overall')]/following-sibling::span/text()").extract()
            elif len(overall_)==1:
                overall = overall_
        # 近期测评
        re_eval = response.xpath("//div[contains(@id, 'review_histograms_container')]\
        //div[contains(text(), 'Recent')]/following-sibling::span/text()").extract()
        if re_eval != []:
            recent, counts_re = response.xpath("//div[contains(@id, 'review_histograms_container')]\
            //div[contains(text(), 'Recent')]/following-sibling::span/text()").extract()
        # 游戏类型，只保留玩家标签的第一个
        game_type = response.xpath("//div[contains(@class, 'details_block')]/a/text()").extract_first()
        # 开发商，只保留第一个
        developers = response.xpath("//div[contains(@class, 'details_block')]\
        /div[contains(@class, 'dev_row')]/b[contains(text(),'Developer')]/following-sibling::a/text()").extract_first()
        # 发行商，一般只有一个
        publishers = response.xpath("//div[contains(@class, 'details_block')]\
        /div[contains(@class, 'dev_row')]/b[contains(text(),'Publisher')]/following-sibling::a/text()").extract_first()

        if price is not None:
            price = price.replace('\t','').replace('\r','').replace('\n', '').replace(',', '')

        if counts_all or counts_re is not None:
            counts_all = int(str(counts_all).replace('reviews', '').replace('(','').replace(')','').replace(',',''))
            counts_re = int(str(counts_re).replace('reviews', '').replace('(','').replace(')','').replace(',',''))

        print("Processing: ", game_name)
# 我没有import .Item，直接是存在字典里通过shell输出的
# 在shell通过命令 $ scrapy crawl steam_game -o games_info.json 得到输出，再通过pandas转成想要的格式导入mysql
        game_info = {
            'name': game_name,
            'release date': release_date,
            'price': price,
            'recent reviews': recent_eval,
            'recent reviewers count': counts_re,
            'overall reviews': total_eval,
            'total reviewers count': counts_all,
            'game type': game_type,
            'Developer': developers,
            'Publisher': publishers,
            'overall evaluation': overall,
            'recent evaluation': recent
        }

        yield game_info
