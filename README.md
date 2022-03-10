scraper.py -> Scrape the historical price for each cryto from https://www.cryptodatadownload.com/data/binance/#google_vignette as csv file.


analysis.py -> Tranform data from :

    
 <table>
<tr><th> BTC/USDT </th><th> ETH/USDT</th></tr>
<tr><td>

unix  | symbol | date | close | ....|       
----  | ------ |----- |-----  | ----|   
..... | ....   | .... |....   | ....|
     
    
</td><td>

unix | symbol | date| close| 
---- | ----   |---- |----  |
.... | ....   |.... |....  |

</td></tr> </table> 

to



date  | BTC/USDT | ETH/USDT  | XRP/USDT  |  ..... |       
----- | -------  |------     |------     |  ----- | 
..... | ......   | ....      |......     |   .....|

where the columns are the closing price for each crypto

