Scrape the historical price for each cryto from https://www.cryptodatadownload.com/data/binance/#google_vignette


analysis.py -> Tranform data from :

            BTC/USDT                                            ETH/USD                           LTC/USDT
           
unix   symbol   date   ...  ...            unix   symbol   date  ...   ...            unix   symbol  date ... ...



to
                  BTC/USDT (closing price)    ETH/USDT (closing price)   LTC/USDT  
      date

First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
