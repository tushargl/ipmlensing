from PyQt5.QtWidgets import QApplication,QFileDialog, QMainWindow, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
# import fitparse

import fitdecode

import sys

from astroquery.gaia import Gaia
from astropy.table import Table, unique
import pyvo as vo


from datapipe import download_GAIA

class Window(QMainWindow):

	def loadData(self):
		download_GAIA()

	@pyqtSlot()
	def on_click(self):
		self.loadData()

	def open(self):
		path = QFileDialog.getOpenFileName(self, 'Open a file', '','All Files (*.*)')
		print(path[0])

		fitfile = path[0]
		
		print(fitfile)

		with open(fitfile,encoding="latin-1") as file:
			lines = file.readlines()
			print(lines)

	def __init__(self):
		super().__init__()

		self.setGeometry(300, 300, 600, 400)
		self.setWindowTitle("PyQt5 window")
		button = QPushButton('Download Data', self)
		button.setToolTip('This will download data from GAIA servers')
		button.move(100,70)


		button.clicked.connect(self.on_click)

		self.show()

app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
