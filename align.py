#!/usr/bin/env python
# -----------------------------------------------------------------------------
# "IBM Model 1 Translation Modeling for SMT"
#
# This script defines the IBM1 class for training a probablity distribution of
# p(s|t) values from a parallel text of source (s) and target (t) languages. The
# IBM1 model one class is basic and uses expectation maximization as its 
# estimation method.
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

class IBM1:
	"""
	Initializes a translation model representing a distribution for p(s|t).
	"""

	def __init__(self, source, target):
		self.source = source
		self.target = target
		self.teetable = defaultdict(lambda: defaultdict(float))
		self.ticker = 0
		# INITIALIZE CO-OCCURANCES AS TEETABLE KEYS #
		print "initializing translation model..."
		for (src, tar) in self._parallelize():
			for i in src:
				for j in tar:
					self.teetable[i][j] += 1
		for (src, tar) in self.teetable.iteritems():
			normalizer = sum(tar.values())
        	for i in tar:
        		tar[i] = tar[i] / normalizer

	def __getitem__(self, key):
		return self.teetable[key]        		

	def em_train(self, steps):
		"""
		Dumbly estimates and recursively maximizes the probabilities of p(s|t).
		"""
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
