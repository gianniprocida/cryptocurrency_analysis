scraper.py -> Scrape the historical price for each cryto from https://www.cryptodatadownload.com/data/binance/#google_vignette as csv file.


data_preparation.py-> Transform data from :

    
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


analysis.py -> Analysis with pandas 



Return distributions
![](Figure_1.png)


 Kernel Density Estimate
![](Figure_3.png)


Heat maps
![](Figure_4.png)