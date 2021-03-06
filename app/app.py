import sys
import logging
import pandas as pd
from datetime import datetime
from alpaca import *
from util import *
from study import *
from dbase import *
from correlate import *

def isTagInOptions(tag:str, cmds:list):
    return True if tag in cmds else False

def AppDaily():
    Run()
    logging.info('----------------------> Complete Run')
    AlpacaDaily.All()
    logging.info('----------------------> Complete AlpacaDaily.All')
    YahooDaily.All()
    logging.info('----------------------> Complete YahooDaily.All')
    AlpacaCrypto.All()
    logging.info('----------------------> Complete AlpacaCrypto.All')
    AllStocks.DownloadFavorites()
    logging.info('----------------------> Complete AllStocks.DownloadFavorites')
    FilterPriceMovement.All(isSaveToDb=True)
    logging.info('----------------------> Complete FilterPriceMovement.All')
    TightMinMax.All()
    logging.info('----------------------> Complete TightMinmax.All')
    StockFinancial.All()
    logging.info('----------------------> Complete StockFinancial.All')
    FilterAtr.All()
    logging.info('----------------------> Complete FilterAtr.All')
    FilterEma.All()
    logging.info('----------------------> Complete FilterEma.All')
    FilterKeyLevels.All()
    logging.info('----------------------> Complete FilterKeyLevels.All')
    FilterFibonacciRetracement.All()
    # logging.info('----------------------> Complete FilterFibonacciRetracement.All')
    # FilterThreeBars.All()
    # logging.info('----------------------> Complete FilterThreeBars.All')
    # FilterRelativeVolume.All()
    logging.info('----------------------> Complete FilterRelativeVolume.All')
    FilterVolumeProfile.All()
    logging.info('----------------------> Complete FilterVolumeProfile.All')
    FilterGapper.All()
    logging.info('----------------------> Complete FilterGapper.All')
    FilterCandlePattern.All()
    logging.info('----------------------> Complete FilterCandlePattern.All')
    FilterDoubleTop.All()
    logging.info('----------------------> Complete FilterDoubleTop.All')
    FilterTrends.All()
    logging.info('----------------------> Complete FilterTrends.All')
    FilterRsiDivergence.All()
    logging.info('----------------------> Complete FilterRsiDivergence.All')
    FilterCorrelate.All()
    logging.info('----------------------> Complete FilterCorrelate.All')
    FilterLongWickCandle.All()
    logging.info('----------------------> Complete FilterVolumeSpreadAnalysis.All')
    FilterVolumeSpreadAnalysis.All()
    logging.info('----------------------> Complete FilterLongWickCandle.All')
    PushToServer()
    logging.info('----------------------> Complete PushToServer')
    ProductionAssetDataSync.All()
    logging.info('----------------------> Complete ProductionAssetDataSync')

def AppCorrelation():
    # Run()
    # logging.info(f'----------------------> Start AlpacaDaily.All')
    # AlpacaDaily.All()
    # logging.info(f'----------------------> Complete AlpacaDaily.All')
    # YahooDaily.All()
    # logging.info(f'----------------------> Complete YahooDaily.All')
    # AlpacaCrypto.All()
    # logging.info(f'----------------------> Complete AlpacaCrypto.All')
    # AtrCalculate.All()
    # logging.info(f'----------------------> Complete AtrCalculate.All')
    CorrelateAssets.All(isSendToServer=False, days=45, minAtr=5)
    logging.info(f'----------------------> Complete CorrelateAssets.All')
    CorrelateAssets.All(isSendToServer=False, days=90, minAtr=5)
    logging.info(f'----------------------> Complete CorrelateAssets.All')
    CorrelateAssets.All(isSendToServer=False, days=180, minAtr=5)
    logging.info(f'----------------------> Complete CorrelateAssets.All')

def AppMarketOpen(isCenterOfControl=False):
    logging.info('----------------------> Start LastNightGapper')
    LastNightGapper.All()
    if isCenterOfControl:
        logging.info('----------------------> Start filterCenterOfControlVP')
        FilterCenterOfControlVP.All(True)
        logging.info('----------------------> Complete filterCenterOfControlVP')
    PushToServer()
    logging.info('----------------------> Complete PushToServer')


def AppDeleteMarketDataTable():
    app = MarketDataDb()
    app.ResetMarketDataTable()


def RunApp():
    today = datetime.now()
    print(f'{today.hour} {today.minute}')
    if today.hour == 21 and today.minute == 15:
        AppDaily()
    elif today.hour == 5 and today.minute == 30:
        AppMarketOpen(False)
    elif today.hour == 6 and today.minute == 0:
        AppMarketOpen(False)
    elif today.hour == 6 and today.minute == 20:
        AppMarketOpen(True)

if __name__ == "__main__":
    formatter = '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter,
                        datefmt='%d-%b-%y %H:%M:%S', filename="analyzer.log")
    logging.info("APP.PY Started")

    if isTagInOptions('--test', sys.argv):        
        FilterGapper.All()
        logging.info('----------------------> Complete FilterGapper.All')
        PushToServer()
        logging.info('----------------------> Complete PushToServer')
    elif isTagInOptions('--reset', sys.argv):
        AppDeleteMarketDataTable()
        AppDaily()
    elif isTagInOptions('--mo', sys.argv):
        AppMarketOpen()
    elif isTagInOptions('--corr', sys.argv):
        AppCorrelation()
    elif isTagInOptions('--day', sys.argv):
        AppDaily()
    elif isTagInOptions('--fin', sys.argv):
        StockFinancial.All(isDebug=True, isForceDl=True)
    else:
        SetInterval(60, RunApp)

    # db = SecDb()
    # db.SetLastDaily('AAPL', 170.33, '2020-01-28')
    # data = db.GetLastDaily('AAPL') 
    # print(data)
    # LastNightGapper.All()
    logging.info('done')
