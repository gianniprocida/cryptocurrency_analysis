scraper.py -> Scrape the historical price for each cryto from https://www.cryptodatadownload.com/data/binance/#google_vignette as csv file.


analysis.py -> Tranform data from :

    
 <table>
<tr><th> BTC/USDT </th><th> ETH/USDT</th></tr>
<tr><td>

unix  | symbol | date | open | ....|       
----  | ------ |----- |----- | ----|   
..... | ....   | .... |....  | ....|
     
    
</td><td>

unix | symbol | date| open | 
---- | ----   |---- |----  |
.... | ....   |.... |....  |

</td></tr> </table> 

to



date  | BTC/USDT | ETH/USDT  | XRP/USDT  |  ..... |       
----- | -------  |------     |------     |  ----- | 
..... | ......   | ....      |......     |   .....|


