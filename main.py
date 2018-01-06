import ccxt
import time
import os

binance   = ccxt.binance({
    'apiKey': 'xxx',
    'secret': 'xxx',
})

def cointousd(amount,coinprice,usd):
 return(amount*float(coinprice)*float(usd))

coins = {'BTC/USDT':0,'TRX/BTC':877,'ADA/BTC':417}


def map(mapcoins,lastmappingcoins,coinstats):
	mapping = """==============================================\n|   Coin       |  Price     |   24% Change   \n"""
	for cryptoname,crypto in mapcoins.items():
	  mapping = mapping +"""| --------     |            |                \n| {6}    Since Last Update:{7}                        \n| {0}   {1}   {2}         \n| {3}   {4}   {5}         \n| Stats Up:{8} Down:{9}  Balance:${10}\n""".format(crypto["Time"],crypto["Price"],crypto["Change"],lastmappingcoins[cryptoname]["Time"],lastmappingcoins[cryptoname]["Price"],lastmappingcoins[cryptoname]["Change"],cryptoname,upordown(crypto["Price"],lastmappingcoins[cryptoname]["Price"]),coinstats[cryptoname]["UpDw"][0],coinstats[cryptoname]["UpDw"][1],coinstats[cryptoname]["Cost"])
	mapping = mapping + "==========================================="
	return(mapping)

def upordown(first,last):
 if first>last:
  result = "Up"
 elif first<last:
  result = "Down"
 else:
  result = "-"
 return(result)

def timeclean(time):
 date = time.split("T")[0]
 time = time.split("T")[1].rstrip("Z")
 return(time)

def twentfourchangeclean(twentfourchange):
 twentfourchange = round(twentfourchange,2)
 return("{}%".format(str(twentfourchange)))

def fetch(coins):
 #ToDo: add price of 1 coin to usd
 coinsret = {}
 for coin in coins:
  coinname = coin
  coin = binance.fetch_ticker(coin)
  datetime = coin["datetime"]
  datetime = timeclean(datetime)
  highlow = (coin["info"]["lowPrice"],coin["info"]["highPrice"])
  twentfourchange = coin["change"]
  twentfourchange = twentfourchangeclean(twentfourchange)
  price = coin["info"]["askPrice"]
  coinsret[coinname] = {"Time":datetime,"Price":price,"Change":twentfourchange}
 return(coinsret)

startinginfo = fetch(coins)
coincounter = {}
for asset in coins:
   up = 0
   down = 0
   cost = 0 
   coincounter[asset] = {}
   coincounter[asset]["Cost"] = cost 
   coincounter[asset]["UpDw"] =[up,down]

while True:
  lastinfo = startinginfo
  coininfo = fetch(coins)
  _=os.system('clear')
  startinginfo = coininfo
  for asset in coins:
   updwcheck = upordown(coininfo[asset]["Price"],lastinfo[asset]["Price"])
   if updwcheck == "Up":
    coincounter[asset]["UpDw"][0] = coincounter[asset]["UpDw"][0]+1
   if updwcheck == "Down":
    coincounter[asset]["UpDw"][1] = coincounter[asset]["UpDw"][1]+1
   if asset != "BTC/USDT":
    coincounter[asset]["Cost"] = cointousd(coins[asset],coininfo[asset]["Price"],coininfo["BTC/USDT"]["Price"])
   else:
    coincounter[asset]["Cost"] = 0
  print(map(coininfo,lastinfo,coincounter))
  time.sleep(.1)
