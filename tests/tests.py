# -*- coding: utf-8 -*-
"""
Tests for the groove generator


Created on Fri Feb  4 15:10:07 2022

@author: olehe
"""
import unittest
import shutil
import tempfile
import groovegenerator as gg
import os



class TestSum(unittest.TestCase):
	

	def test_generate_random_pattern(self):
		randPattern = gg.generateRandomPattern()
		self.assertEqual(randPattern.shape, (3,32), 'Wrong shape of random pattern')
		
	def test_generate_constrained_pattern(self):
		constrainedPattern = gg.generateConstrainedPattern()
		self.assertEqual(constrainedPattern.shape, (3,32), 'Wrong shape of constrained pattern')
	
	def test_load_save_pattern(self):
		test_dir = tempfile.mkdtemp()
		savePath = test_dir
		self.saveName = savePath + '\\testPattern.csv'
		saved = gg.savePattern(gg.generateRandomPattern(), self.saveName, verbose=False)
		self.assertEqual(os.path.isfile(self.saveName), True, 'Pattern csv not saved succesfully')

		loaded = gg.loadPattern(self.saveName)
		self.assertEqual(loaded.shape, (3,32), 'Loading pattern from csv failed')
		
		shutil.rmtree(test_dir)
		

if __name__ == '__main__':
	unittest.main()
		