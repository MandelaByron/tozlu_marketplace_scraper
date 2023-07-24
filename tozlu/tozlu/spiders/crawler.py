import scrapy
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from ..items import TozluItem
from inline_requests import inline_requests
from scrapy.http import Request

headers = {
    
    "authority" : "www.tozlu.com",
    "accept" : "*/*",
    "accept-language" : "en-US,en;q=0.6",
    "cache-control" : "no-cache",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "x-requested-with" : "XMLHttpRequest"
}


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    allowed_domains = ["tozlu.com"]
    #start_urls = ["https://tozlu.com"]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
        'ROBOTSTXT_OBEY': False,
        'FEEDS':{
            'tozlu_data.csv':{
                'format':'csv',
                'overwrite':True
            }
        }
    }   
    strings=[
    
    {"FilterJson":"{\"CategoryIdList\":[271],\"BrandIdList\":[],\"SupplierIdList\":[],\"TagIdList\":[],\"TagId\":-1,\"FilterObject\":[],\"MinStockAmount\":-1,\"IsShowcaseProduct\":-1,\"IsOpportunityProduct\":-1,\"FastShipping\":-1,\"IsNewProduct\":-1,\"IsDiscountedProduct\":-1,\"IsShippingFree\":-1,\"IsProductCombine\":-1,\"MinPrice\":0,\"MaxPrice\":0,\"Point\":0,\"SearchKeyword\":\"\",\"StrProductIds\":\"\",\"IsSimilarProduct\":false,\"RelatedProductId\":0,\"ProductKeyword\":\"\",\"PageContentId\":0,\"StrProductIDNotEqual\":\"\",\"IsVariantList\":-1,\"IsVideoProduct\":-1,\"ShowBlokVideo\":-1,\"VideoSetting\":{\"ShowProductVideo\":-1,\"AutoPlayVideo\":-1},\"ShowList\":1,\"VisibleImageCount\":6,\"ShowCounterProduct\":-1,\"ImageSliderActive\":false,\"ProductListPageId\":0,\"ShowGiftHintActive\":false,\"IsInStock\":false,\"IsPriceRequest\":true,\"NonStockShowEnd\":0}","PagingJson":"{\"PageItemCount\":0,\"PageNumber\":1,\"OrderBy\":\"YAYINTARIHI\",\"OrderDirection\":\"DESC\"}","PageType":"1","PageId":"271"},
    #{"FilterJson":"{\"CategoryIdList\":[192],\"BrandIdList\":[],\"SupplierIdList\":[],\"TagIdList\":[],\"TagId\":-1,\"FilterObject\":[],\"MinStockAmount\":-1,\"IsShowcaseProduct\":-1,\"IsOpportunityProduct\":-1,\"FastShipping\":-1,\"IsNewProduct\":-1,\"IsDiscountedProduct\":-1,\"IsShippingFree\":-1,\"IsProductCombine\":-1,\"MinPrice\":0,\"MaxPrice\":0,\"SearchKeyword\":\"\",\"StrProductIds\":\"\",\"IsSimilarProduct\":false,\"RelatedProductId\":0,\"ProductKeyword\":\"\",\"PageContentId\":0,\"StrProductIDNotEqual\":\"\",\"IsVariantList\":-1,\"IsVideoProduct\":-1,\"ShowBlokVideo\":-1,\"VideoSetting\":{\"ShowProductVideo\":-1,\"AutoPlayVideo\":-1},\"ShowList\":1,\"VisibleImageCount\":6,\"ShowCounterProduct\":-1,\"ImageSliderActive\":false,\"ProductListPageId\":0,\"ShowGiftHintActive\":false,\"IsProductListPage\":true,\"NonStockShowEnd\":1}","PagingJson":"{\"PageItemCount\":0,\"PageNumber\":1,\"OrderBy\":\"KATEGORISIRA\",\"OrderDirection\":\"ASC\"}","CreateFilter":"false","TransitionOrder":"0","PageType":"1"},
  
]
    
    def get_pages(self,qs):
        url = "https://www.tozlu.com/api/product/GetProductList/?"
        
        r = requests.get(url,params=qs,headers=headers)
        
        data = r.json()
        
        pages = data['totalProductCount'] // 50
        pages = pages + 1
        print(f"total pages = {pages}")
        return pages
    
    
    def start_requests(self):
        url = "https://www.tozlu.com/api/product/GetProductList/?"


        #querystring = {"FilterJson":"{\"CategoryIdList\":[270],\"BrandIdList\":[],\"SupplierIdList\":[],\"TagIdList\":[],\"TagId\":-1,\"FilterObject\":[],\"MinStockAmount\":-1,\"IsShowcaseProduct\":-1,\"IsOpportunityProduct\":-1,\"FastShipping\":-1,\"IsNewProduct\":-1,\"IsDiscountedProduct\":-1,\"IsShippingFree\":-1,\"IsProductCombine\":-1,\"MinPrice\":0,\"MaxPrice\":0,\"SearchKeyword\":\"\",\"StrProductIds\":\"\",\"IsSimilarProduct\":false,\"RelatedProductId\":0,\"ProductKeyword\":\"\",\"PageContentId\":0,\"StrProductIDNotEqual\":\"\",\"IsVariantList\":-1,\"IsVideoProduct\":-1,\"ShowBlokVideo\":-1,\"VideoSetting\":{\"ShowProductVideo\":-1,\"AutoPlayVideo\":-1},\"ShowList\":1,\"VisibleImageCount\":6,\"ShowCounterProduct\":-1,\"ImageSliderActive\":false,\"ProductListPageId\":0,\"ShowGiftHintActive\":true,\"IsProductListPage\":true,\"NonStockShowEnd\":1}","PagingJson":"{\"PageItemCount\":0,\"PageNumber\":1,\"OrderBy\":\"KATEGORISIRA\",\"OrderDirection\":\"ASC\"}","CreateFilter":"false","TransitionOrder":"0","PageType":"1","PageId":"270"}
        
        for querystring in self.strings:
            pages = self.get_pages(qs=querystring)
            pages = 3
            for i in range(0,pages + 1):
                #print(i)
                qs = querystring
                qs["PagingJson"] = qs["PagingJson"].replace(f"\"PageNumber\":{i}",f"\"PageNumber\":{i+1}")
                print(qs["PagingJson"])
                link = url + urlencode(qs)
                
                yield scrapy.Request(url=link,headers=headers,callback=self.parse_page)
                
                
                
                
    @inline_requests
    def parse_page(self, response):
        data = response.json()
        
        for product in data['products']:
            category = product['category']
            
            scrap_url ='https://www.tozlu.com' + product['url']
            

            #list_price = product['productCartPrice'] + product['productCartPriceKDV']
            
            list_price= product['productSellPrice'] + product['productSellPriceKDV']
            
            parse_page = yield Request(url=scrap_url,meta={'playwright':True})
            
            price = parse_page.xpath("//div[@class='DetSepetFiyat']/span/text()").get()
            
            price = price.strip().replace('TL','').replace(',','.')
            
            product_id = product['productId']

                
            items = {
                
            }  

            
            brand = product['brand']
            
            name = product['name']
            
            items['name'] = name
            
            items['scrap_url']=scrap_url
            
            items['category'] = category
            
            
            
            items['price'] = round(price,1)
            
            
            
            items['list_price'] = round(list_price,1)
            
           
            
            items['brand'] = brand
            

            target_url = "https://www.tozlu.com/api/product/GetProductDetail"
            
            
            payload=f"{{\"ProductId\":{product_id},\"IsQuickView\":false}}"

            det_headers = {
                    #"cookie": "__cf_bm=LDhLSccKFFWhpZfR1Bov6fCwtlhWD7PYNwnlp_ixkFk-1689018215-0-Af%2Fffl0cJ7h6ctDQL%2FoKDWQuG%2BWj7Cac5TOoTi1O0Vmdmx%2FM5iFaUZp6IAZPCChsQq3c0R9h8IeO8Fwknr7Ygfs%3D; ApplicationGatewayAffinityTBS=27363341ce554d95bac7ac13581b4296; TcmxSID=y32u5mitpfafkikvvjin5m4y; CultureSettings=H4sIAAAAAAAEAAXByYJDMAAA0A9yQNV26IHaElsSlLqRdiy1j6F8%252fbxXmkLx1y0unT6xAqJGAvs9Fl7ZomDDwGXvIVQSWbP0w2JGmLTBc4K5B36Z5%252blXfLZODT4BkN51XUsDaMW90lS4Su5%252bio%252beadRh%252b%252bF1K6Ji95YJxxKb8s4CTXaAkJXswrO46%252bBLVu45HOraVlALHLcrCmZ5KJtv%252bgIG%252bf10o37Z4FAwiSbuBg5X4X0UFcFRKtZ6ztDcnDVdwEICLbtwR6oES4caT%252fmsj5ZGrOyo5mz69kmEkAjgTDyAnJXPfCXeKHHaycT1fKfj5MZ9TDY8yP4VuhnwUlnNaXY8ISJMT1GvIchf9TF0EjOpgnv6zbNQPy5UskpVhHZgqdPYfzm0327%252fMtk%252bsFgBAAA%253d",
                    "authority": "www.tozlu.com",
                    #"accept": ""*/*"",
                    "content-type": "application/json; charset=UTF-8",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "x-ajaxpro-token": "-UxfPR7hyQ1-Qz7PgY3REhvA2Rv2TfhAN9WrgrKojgwxjR56pViwtMG9J2ZfTIrmrB_qsnpKNQwNlpE8tCcAl29J1c4twKQNgdYj9GPCPc01",
                    "x-requested-with": "XMLHttpRequest"
                }
            response = scrapy.Request(url=target_url,method="POST",body=payload,headers=det_headers,callback=self.parse)
            
            response.cb_kwargs['items'] = items
            
            yield response
            
    def parse(self,response,items):
        yield_items = TozluItem()
        yield_items = items
        
        data = response.json()
        try:
            description = data['detail']['base']['properties']['description']
        except TypeError:
            description=''
        
        if description != None:
            yield_items['description'] = BeautifulSoup(description,'lxml').text.strip().replace('\n',' ')
        else:
            description=''
            
        try:    
            code = data['detailModel']['product']['tedarikciKodu']  
            
            list_=code.split('|')

            group_code =''.join(list_[0:2])
            
            yield_items['group_code'] = group_code
        except:
            yield_items['group_code'] = ''
        
        # try:
        #     yield_items['qty']=data['detail']['product']['stockAmount']
        # except:
        #     yield_items['qty']=''
        
        for counter,image in enumerate(data['detail']['product']['images'],start=1):
            if counter <=10 :
                image_url=image['bigImagePath']
                
                yield_items[f'image{counter}'] = image_url
            
        variants=data['detailModel']['productVariantData']
        
        if variants != None:
            colors = []
            for variant in variants:
                if variant['ekSecenekTipiTanim'] == 'Renk':
                    #yield_items['color'] = variant['tanim']
                    colors.append(variant['tanim'])
            
            for color in colors:
                
                for variant in data['detailModel']['products']:
                    size = variant['tedarikciKodu'].split('|')[-1]
                    
                    product_code = variant['stokKodu'] + ',' + color + ',' + size
                    
                    yield_items['product_code']=product_code
                    
                    yield_items['qty']=variant['stokAdedi']
                    
                    yield_items['color'] = color
                    
                    yield_items['size'] = size

                    yield yield_items
                    
                # elif variant['ekSecenekTipiTanim'] == 'Beden':
                                       
                #     yield_items['size'] = variant['tanim']
                    
                # else:
                #     yield_items['size']=''
                #     yield_items['color']=''
                # for product in data['detailModel']['products']:
                #     product_code = product['stokKodu']
                #     yield_items['product_code']=product_code
                    
                # yield yield_items
        else:
            yield_items['size']=''
            yield_items['color']=''
            product_code = data['detail']['product']['stockCode']
            yield_items['product_code']=product_code
            
            yield yield_items