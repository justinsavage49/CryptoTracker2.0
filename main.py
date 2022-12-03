from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *    
from PyQt5.QtGui import *
import datetime as dt
import pandas_datareader as web
from forex_python.converter import CurrencyRates
import sys

class MainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 285)
        self.setWindowTitle('Crypto Tracker')
        self.setStyleSheet('''
        background-color: #222223;
        border: 3px ridge grey;
        font-size: 14px;
        ''')
        self.yPos = 25

        #INIT DATA
        self.cryptoList = [
        ['BTC', 'Bitcoin'], ['ETH', 'Ethereum'], ['BNB', 'Binance'], ['XRP', 'Ripple'],
        ['DOGE', 'Dogecoin'], ['LTC', 'Litecoin'], ['ADA', 'Cardano'], ['XMR', 'Monero'],
        ['SOL', 'Solana'], ['TRX', 'TRON'], ['DOT', 'Polkadot']
        ]
        self.currencyList = ['USD', 'EUR', 'GBP', 'JPY', 'MXN']
        self.currentTrackers = []
        self.currency = 'USD'

        self.mainMenu = self.menuBar()
        self.mainMenu.setStyleSheet('''
        background-color: white;
        border: 0px, solid, white;
        ''')
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.editMenu = self.mainMenu.addMenu('&Edit')
        self.helpMenu = self.mainMenu.addMenu('&Help') 
        self.currencyMenu = self.mainMenu.addMenu('&Currency')
        
        #CURRENCY SELECTOR MENU
        for i in range(len(self.currencyList)):
            currencyAction = QAction(self.currencyList[i], self)
            currencyAction.setCheckable(True)
            self.currencyMenu.addAction(currencyAction)
            currencyAction.triggered.connect(lambda action, i=i: self.OnClickCurrency(self.currencyList[i]))            
        
        self.addTrackerMenu = self.mainMenu.addMenu('&[Add Tracker]')
        
        #ADD CRYPTO LIST
        for i in range(len(self.cryptoList)):
            cryptoAction = QAction(self.cryptoList[i][0], self)
            self.addTrackerMenu.addAction(cryptoAction)
            cryptoAction.triggered.connect(lambda action, i=i: self.OnClickCrypto(self.cryptoList[i][0], self.cryptoList[i][1]))

        #DELETE TRACKER BUTTON
        self.deleteBtn = QPushButton('&[Delete Tracker]', self.mainMenu)
        self.deleteBtn.move(285, 0)
        self.deleteBtn.clicked.connect(self.OnClickDelete)
        self.deleteBtn.setStyleSheet('''
        QPushButton {
        text-align: center;
        height: 25px;
        width: 110px;
        font-size: 14px;
        color: red;}
        QPushButton:hover {
        background-color: rgba(255, 0, 0, 0.3);
        }''')
    
    def OnClickCurrency(self, currency):
        global selectedCurrency
        selectedCurrency = currency
        self.currency = currency
    
    def OnClickCrypto(self, crypto, full):    
        trackerSlot = QLabel(self)
        trackerSlot.setGeometry(0, self.yPos, 400, 65)
        trackerSlot.setAlignment(Qt.AlignLeft)
        trackerSlot.setStyleSheet('''
        background: rgba(0,0,0,0);
        font-size: 30px;
        text-align: center;
        color: orange;
        border: 0px solid white;
        border-bottom: 3px ridge grey; 
        ''')

        #MAIN TRACKER TITLE 'BTC'
        cryptoAbbrev = QLabel(crypto, trackerSlot)
        cryptoAbbrev.setGeometry(8,-6,200,50)
        cryptoAbbrev.setStyleSheet('''
        border: 0px, solid, white;
        ''')

        #FULL CRYPTO NAME
        cryptoFull = QLabel(full, trackerSlot)
        cryptoFull.setGeometry(10, 22, 200, 50)
        cryptoFull.setStyleSheet('''
        border: 0px, solid, white;
        font-size: 16px;
        ''')

        #CRYPTO PRICE
        self.MarketInfo(crypto)
        priceLabel = QLabel(self.marketPrice, trackerSlot)
        priceLabel.setGeometry(148, 19, 200, 50)
        priceLabel.setAlignment(Qt.AlignRight)
        if self.priceDelta > 0:
            priceLabel.setStyleSheet('''
            border: 0px, solid, white;
            color: rgba(39, 222, 11, 1);
            font-size: 36px;
            ''')
        else:
            priceLabel.setStyleSheet('''
            border: 0px, solid, white;
            color: red;
            font-size: 36px;
            ''')

        #OPEN/CURRENT PRICE DELTA
        priceDelta = str(format(round(self.priceDelta, 2), '.2f'))
        deltaLabel = QLabel('Open Δ', trackerSlot)
        deltaLabel.setGeometry(102, -15, 75, 75)
        deltaLabel.setStyleSheet('''
        border: 0px, solid, white;
        color: white;
        font-size: 20px;
        font-style: bold;
        ''')
        deltaLabel1 = QLabel(priceDelta + '%', trackerSlot)
        deltaLabel1.setGeometry(102, 12, 75, 70)
        if self.priceDelta > 0:
            deltaLabel1.setStyleSheet('''
            border: 0px, solid, white;
            color: rgba(39, 222, 11, 1);
            font-size: 20px;
            font-style: bold;
            ''')
        else:
            deltaLabel1.setStyleSheet('''
            border: 0px, solid, white;
            color: red;
            font-size: 20px;
            font-style: bold;
            ''') 

        #CURRENCY
        currencyLabel = QLabel(self.currency, trackerSlot)
        currencyLabel.setGeometry(354, 22, 200, 50)
        currencyLabel.setStyleSheet('''
        border: 0px, solid, white;
        color: lightgrey;
        font-size: 20px;
        font-style: bold;
        ''')
        trackerSlot.show()
        self.currentTrackers.append(trackerSlot)
        self.yPos += 65
    
    def OnClickDelete(self):
        if len(self.currentTrackers) > 0:
            self.currentTrackers[-1].deleteLater()
            self.currentTrackers[-1] = None
            self.currentTrackers.pop(-1)
            self.yPos -= 65

    def MarketInfo(self, crypto):
        t1 = dt.datetime.utcnow() - dt.timedelta(hours=24)
        start = t1.date()
        marketInfo = web.DataReader(crypto + '-USD', 'yahoo', start=start)
        marketOpen, marketNow = marketInfo['Open'][1], marketInfo['Adj Close'][1]
        priceDelta = (marketNow / marketOpen - 1) * 100
        self.marketPrice = str(format(round(marketNow, 2), '.2f'))
        self.priceDelta = round(priceDelta, 2)

def main():
    app = QApplication(sys.argv)
    win = MainWin()
    win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    win.show()
    sys.exit(app.exec_())
   
if __name__ == "__main__":
    main()    