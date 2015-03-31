#!/usr/bin/env python
# -----------------------------------------------------------------------------
# "IBM Model 1 Translation Modeling w/ Trigram Language Modeling for SMT"
#
# This script defines:
# 1. An IBM1 class for training a probablity distribution of p(s|t) values from 
# a parallel text of source (s) and target (t) languages. The IBM Model 1 is 
# basic and uses expectation maximization as its estimation method.
# 2. A LanguageModel class for training a trigram language model on an input 
# training text. 
#
# -----------------------------------------------------------------------------
# Copyright (c) 2015
#
# Authors: C. Clayton Violand <claytonvioland@gmail.com>
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

from sys import stderr
from collections import defaultdict
import re

class IBM1:
	"""
	Wraps a translation model representing a distribution for p(s|t) using
	IBM Model 1. Trains on a parallel bilinguial corpus.
	"""

	def __init__(self, source, target):
		self.source = source
		self.target = target
		self.teetable = defaultdict(lambda: defaultdict(float))
		self.ticker = 0
		# INITIALIZE CO-OCCURANCES AS TEETABLE KEYS #
		print "INITIALIZING TRANSLATION MODEL..."
		for (src, tar) in self._parallelize():
			for i in src:
				for j in tar:
					self.teetable[i][j] += 1
		for (src, tar) in self.teetable.iteritems():
			normalizer = sum(tar.values())
        	for i in tar:
        		tar[i] = tar[i] / normalizer

	def __getitem__(self, key):
		"""
		Returns the t-table probability of an alignment.
		"""
		return self.teetable[key]        		

	def em_train(self, steps):
		"""
		Dumbly estimates and recursively maximizes the probabilities of p(s|t).
		"""
		print "TRAINING TRANSLATION MODEL..."
		for i in range(steps):
			print >> stderr, 'iteration {0}...'.format(self.ticker+1)
			x = defaultdict(float)
			y = defaultdict(float)
			# EXPECTATION # 
			for (src,tar) in self._parallelize():
				for i in src:
					for j in tar:
						p = self.teetable[i][j]
						x[(i,j)] += p
						y[j] += p
			# MAXIMIZATION #
			for ((i,j),score) in x.iteritems():
				self.teetable[i][j] = score / y[j]
			for (src,tar) in self.teetable.iteritems():
				normalizer = sum(tar.values())
				for i in tar:
					tar[i] = tar[i] / normalizer
			# INCREMENT TICKER #
			self.ticker += 1
		self.ticker = 0

	def _parallelize(self):
		"""
		Creates a parallel text from a source and target file and yields one
		pair of sentences at a time to be passed on for training.
		"""
		source_raw = open(self.source, 'r')
		target_raw = open(self.target, 'r')
		for (src, tar) in zip(source_raw, target_raw):
			src = src.upper()
			tar = tar.upper()
			# ADD NULL WORD ON SOURCE SIDE #
			yield ([None] + src.strip().split(), tar.strip().split())

	def align_training_data(self):
		"""
		Outputs alignment results for the training data.
		"""
		for (src,tar) in self._parallelize():
			yield self._align(src,tar)

	def show_alignment(self, alignments):
		"""
		Outputs the contents of a generator object as strings.
		"""
		for i in alignments:
			for j in i:
				for k in j:
					print k,
				print

	def _align(self, source, target):
		"""
	   	Returns the optimal alignment given a source sentence and a target 
	   	sentence.
	   	"""
	   	print '----------ALIGNING PHRASE---------->'
		for i in source:
			top_prob = 0
			top_align = -1
	   		for (index, j) in enumerate(target):
   				prob = self.teetable[i][j]
	   			if prob > top_prob:
	   				top_prob = prob
	   				top_align = index	
	   		yield i, target[top_align]

class LanguageModel:
	"""
	Wraps a language model. Trains on plain text as input.
	"""

	def __init__(self, training_data):
		# CONVERT TRAINING DATA TEXT TO LIST OF TRIGRAMS #
		self.training_data = training_data
		self._get_trigrams()
		self._wrap_lm()

	def __getitem__(self, key):
		"""
		Returns.
		"""
		return self.lm[key]

	def _wrap_lm(self):
		print "INITIALIZING LANGUAGE MODEL..."
		self.lm = {}
		count = 0
		for i in self.trigrams:
			count += 1
			if i[0] in self.lm:
				if i[1] in self.lm[i[0]]:
					if i[2] in self.lm[i[0]][i[1]]:
						self.lm[i[0]][i[1]][i[2]] += 1
					else: 
						self.lm[i[0]][i[1]][i[2]] = 1
				else:
					self.lm[i[0]][i[1]] = {i[2] : 1}
			else:
				self.lm[i[0]] = {i[1] : {i[2]:1}}
		return self.lm

	def _get_trigrams(self):
		"""
		Parses training text into a list of trigrams.
		"""
		lines = [['<START>'] + re.sub(r'[^a-z ]+', '',						\
					i.lower())[0:-1].split() + ['<END>'] 					\
					for i in open(self.training_data, 'r').readlines()]
		self.trigrams = []
		for l in lines:
			self.trigrams.extend(self._trigram_it(l))
		return self.trigrams

	def _trigram_it(self, line):
		return [line[i:i+3] for i in range(len(line)-2)]

	def estimate_probs(self):
		print "ESTIMATING TRIGRAM PROBABILITIES..."
		for a, a_index in self.lm.items():
			for b, b_index in a_index.items():
				total = float(sum(b_index.values()))
				for c in b_index.keys():
					b_index[c] /= float(total)
		print "DONE.\n"
