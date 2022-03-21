# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 16:21:53 2021

@author: olehe
"""


import sys
import os
import time
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import groovegenerator as gg

# some style

import qtmodern.styles
import qtmodern.windows

from pathlib import Path

root = Path()
if getattr(sys, 'frozen', False):
    root = Path(sys._MEIPASS)
    qtmodern.styles._STYLESHEET = root / 'qtmodern/resources/style.qss'
    qtmodern.windows._FL_STYLESHEET = root / 'qtmodern/resources/frameless.qss'



#%% Some global variables to start off with

stepNumbers = 32
bars = 2
stepChannels = 3

class GrooveGenerator(QWidget):
	
	def __init__(self):
		super().__init__()
		
		self.initUI()
		self.report_status('Ready.')

		
	
	
	def initUI(self):
		main_grid = QGridLayout()
		metro_grid = QGridLayout()
		top_grid = QGridLayout()
		
		statusLabel = QLabel('Status: ')
		top_grid.addWidget(statusLabel, 1, 1)
		self.statusBox = QLabel('Ready.')
		top_grid.addWidget(self.statusBox, 1, 2, 1, 3)
		
		#thanksLabel = QLabel('Heggli - 2021')
		#top_grid.addWidget(thanksLabel, 1, 6)

		
		main_grid.addLayout(top_grid, 1, 1, 1, 6)

		
		# grouping the pattern buttons
		self.metro_group = QButtonGroup()
		self.metro_group.setExclusive(False)
		# create the buttons
		# remember add a text field as well.
		instrLabels = ['Beat', 'Hihat', 'Snare', 'Kick']
		
		# also add some sort of bar at the top.
		# 2 bars x 16 events
		tickLabels = ['1.1', '', '', '', '1.2', '', '', '','1.3', '', '', '','1.4', '', '', '',
				'2.1', '', '', '', '2.2', '', '', '','2.3', '', '', '','2.4', '', '', '']
		
		count=0
		for i in range(0,stepChannels+1):
			thisLabel = QLabel(str(instrLabels[i]))
			metro_grid.addWidget(thisLabel, i, 0)
			for j in range(1,stepNumbers+1):
				if i == 0:
					thisLabel = QLabel(str(tickLabels[j-1]))
					metro_grid.addWidget(thisLabel, i, j)
				else:
					thisCheck = QCheckBox()
					thisCheck.clicked.connect(self.calculate)
					self.metro_group.addButton(thisCheck)
					self.metro_group.setId(thisCheck, count)
					metro_grid.addWidget(thisCheck,i,j)
					count+=1
		
		# insert into main grid
		main_grid.addLayout(metro_grid, 2, 1, 1, 6)
		
		
		
	
		
		
		tempoLabel = QLabel('BPM:')
		main_grid.addWidget(tempoLabel, 3, 1)
		
		self.tempoField = QSpinBox()
		self.tempoField.setRange(30, 300)
		self.tempoField.setValue(120)
		main_grid.addWidget(self.tempoField, 3, 2)
		
		
		loopLabel = QLabel('Loops:')
		main_grid.addWidget(loopLabel, 3, 3)
		# loop selection buttons
		self.loopButton = QSpinBox()
		self.loopButton.setRange(1, 100)
		self.loopButton.setValue(1)
		main_grid.addWidget(self.loopButton, 3, 4)
		
		#self.outputName = QLineEdit('SaveName')
		#main_grid.addWidget(self.outputName, 4, 1, 1, 2)
		
		eventLabel = QLabel('nEvents:')
		main_grid.addWidget(eventLabel, 3, 5)
		
		self.eventCount = QLabel('')
		main_grid.addWidget(self.eventCount, 3, 6)
		
		# hihat button
		
		insertFillLabel = QLabel('Autofill:')
		main_grid.addWidget(insertFillLabel, 4, 1)
		
		hihatButton = QPushButton('Hihat')
		hihatButton.clicked.connect(self.hihat_on)
		main_grid.addWidget(hihatButton, 4, 2)
		
		kickButton = QPushButton('Kick')
		kickButton.clicked.connect(self.kick_on)
		main_grid.addWidget(kickButton, 4, 3)
		
		snareButton = QPushButton('Snare')
		snareButton.clicked.connect(self.snare_on)
		main_grid.addWidget(snareButton, 4, 4)
		
		clearButton = QPushButton('Reset')
		clearButton.clicked.connect(self.clear)
		main_grid.addWidget(clearButton, 4, 5)
		
		
		
		
		
		# load button
		loadButton = QPushButton('Load pattern')
		loadButton.clicked.connect(self.loadPattern)
		main_grid.addWidget(loadButton, 5, 1)
		
		# save button
		saveButton = QPushButton('Save pattern')
		saveButton.clicked.connect(self.savePattern)
		main_grid.addWidget(saveButton, 5, 2)
		
		SIlabelH = QLabel('Hoesl\'s SI:')
		main_grid.addWidget(SIlabelH, 5, 3)
		self.SIcalcH = QLabel('N/A')
		main_grid.addWidget(self.SIcalcH, 5, 4)
		SIlabelW = QLabel('Witek\'s SI:')
		main_grid.addWidget(SIlabelW, 5, 5)
		self.SIcalcW = QLabel('N/A')
		main_grid.addWidget(self.SIcalcW, 5, 6)
		
		
		
		# generate button
		generateButton = QPushButton('Generate pattern')
		generateButton.clicked.connect(self.generateRandomPattern)
		main_grid.addWidget(generateButton, 6, 1)
		
		# search pattern button
		searchButton = QPushButton('Search pattern')
		searchButton.clicked.connect(self.searchPattern)
		main_grid.addWidget(searchButton, 6, 2)
		
		calcButton = QPushButton('Recalculate SI')
		calcButton.clicked.connect(self.calculate)
		main_grid.addWidget(calcButton, 6, 3)
		
		# process pattern
		runButton = QPushButton('Process pattern')
		runButton.clicked.connect(self.processPattern)
		main_grid.addWidget(runButton, 6, 5, 1, 2)
		
		
		self.setLayout(main_grid)
		self.setWindowTitle("Groove Generator")
		self.setGeometry(50,50,200,200)
		self.setWindowIcon(QIcon('icon.ico'))
		#self.show()
	
	
	
	
	def getPattern(self):
		# gets the pattern as numpy array
		eventArray = []
		for n, button in enumerate(self.metro_group.buttons()):
			event = button.isChecked()
			eventArray.append(int(event))
		output_array = np.reshape(eventArray, (stepChannels, stepNumbers))
		
		return output_array
	
	
	def savePattern(self):
		pattern = self.getPattern()
		
		
		name = QFileDialog.getSaveFileName(self, 'Save File', filter='*.csv')
		#print(name)
		
		gg.savePattern(pattern, name[0], verbose=False)
		self.report_status('Saved pattern')
		
		return
		
		
	def loadPattern(self):
		# this is probably going to fail in many cases, since I don't care to write checks for weird formatting issues
		name = QFileDialog.getOpenFileName(self, 'Load File', filter='*.csv')
		print(name[0])
		try:
			pattern = gg.loadPattern(name[0], asArray=True)
			#print(pattern)
			pattern = pattern.flatten()
			
			assert len(pattern) == stepNumbers * stepChannels
			
			for n, button in enumerate(self.metro_group.buttons()):
				button.setChecked(bool(pattern[n]))
			self.report_status('Loaded pattern')
			self.calculate()
		except:
			#print('Loading file failed')
			self.report_status('Loading pattern failed')
			return
	
	def countEvents(self, hihats=False):
		pattern = self.getPattern()
		
		if hihats:
			events = sum(pattern.flatten())
			#print(events)
		else:
			snares = pattern[1,]
			kicks = pattern[2,]
			both = np.array([snares, kicks]).flatten()
			events = sum(both)
		
		
		return events
	
	
	def generateRandomPattern(self, verbose=True):
		# just a simple random pattern with some contraints
		
		maxEvents = 20
		minEvents = 10
		
		patternGen = gg.generateRandomPattern(minEvents, maxEvents)
		
		pattern = patternGen.flatten()
		for n, button in enumerate(self.metro_group.buttons()):
			button.setChecked(bool(pattern[n]))
		
		
		if verbose:
			self.report_status('Generated pattern')
		self.calculate()
		return pattern
	
	
	def searchPattern(self):
		self.report_status('Searching for pattern')
		
		# first get which measure
		measure, ok = QInputDialog.getItem(self, 'Select', 'Select SI measure:', ['Hoesl\'s', 'Witek\'s'], 0, False)
		
		if not ok:
			return
		
		if measure == 'Hoesl\'s':
			defaultValue = 0.1
			minValue = 0.0
			maxValue = 150.0
			decimals = 3
			steps = 0.01
			select = 0
		elif measure == 'Witek\'s':
			defaultValue = 10.0
			minValue = 0.0
			maxValue = 150.0
			decimals = 1
			steps = 0.05
			select = 1
		
		
		
		
		target, ok = QInputDialog.getDouble(self, 'Search for SI', 'Target SI:', defaultValue, minValue, maxValue, decimals, Qt.WindowFlags(), steps)
		
		if not ok:
			return
		
		target = float(target)
		measureCode = measure[0]
		
		pattern, success = gg.searchPattern(measureCode, 
						  target=target,
						  timeout=60,
						  minEvents=10,
						  maxEvents=30,
						  verbose=False)
		if success:
			patternFlat = pattern.flatten()
		else:
			self.report_status('Failed to find pattern.')
			self.calculate()
			return
		for n, button in enumerate(self.metro_group.buttons()):
			button.setChecked(bool(patternFlat[n]))
			
		if success:
			self.report_status('Pattern found.')
			self.calculate()
		else:
			self.report_status('Failed to find pattern.')
			self.calculate()
		
		return
			
	
	
	def calculate(self, verbose=True):
		# Calculates and reports the SI
		
		pattern = self.getPattern()
		patternA = pattern[1,] # snare
		patternB = pattern[2,] # kick
		
		hSI, wSI = gg.calculate(pattern)
		

		self.SIcalcH.setText(str(round(hSI,3)))
		self.SIcalcW.setText(str(round(wSI,3)))
		
		events = self.countEvents()
		self.eventCount.setText(str(events))
		
		
		return hSI, wSI
		
	def clear(self):
		#print('Clearing.')
		for n, button in enumerate(self.metro_group.buttons()):
			button.setChecked(False)
		
		self.calculate()
		return
			
			
	def hihat_on(self):
		#print('Hihatting.')
		step=True
		for n, button in enumerate(self.metro_group.buttons()):			
			if n<32:
				if step:
					button.setChecked(True)
					step = False
				else:
					step = True
		
		self.calculate()
		return
				
	def kick_on(self):
		#print('kicking.')
		step = True
		count = 0
		for n, button in enumerate(self.metro_group.buttons()):
			if n>63:
				if step:
					button.setChecked(True)
					count = 0
					step = False
				else:
					count += 1
				if count > 2:
					step = True
		self.calculate()
		return
					
	def snare_on(self):
		#print('kicking.')
		step = False
		count = 0
		for n, button in enumerate(self.metro_group.buttons()):
			if n>32 and n<64:
				if step:
					button.setChecked(True)
					count = -4
					step = False
				else:
					count += 1
				if count > 2:
					step = True
		self.calculate()
		return
			
	def report_status(self, status):
		self.statusBox.setText(status)
		#print(status)
	
	def processPattern(self):
		self.report_status('Generating...')
		
		# get savename here
		text, ok = QInputDialog().getText(self, "Process",
                                     "Input name of pattern:", QLineEdit.Normal)
		if not ok:
			return
		text.replace(' ', '')
		
		
		pattern = self.getPattern()
		
		tempo = int(self.tempoField.text())
		loops = int(self.loopButton.value())
		print('Doing ' + str(loops) + ' loops.')
		
		gg.processPattern(pattern, text, tempo, loops)
		
		self.report_status('Done! Ready.')
		
		return
	
	
	
	
	
		
  

if __name__ == '__main__':
	
	if not os.path.isdir('stimsMidi'):
		os.mkdir('stimsMidi')
	if not os.path.isdir('stimsWAV'):
		os.mkdir('stimsWAV')
	
	
	app = QApplication(sys.argv)
	qtmodern.styles.dark(app)

	window = GrooveGenerator()
	mw = qtmodern.windows.ModernWindow(window)
	mw.show()
	
	
	sys.exit(app.exec_())
