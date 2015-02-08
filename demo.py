#!/usr/bin/env python
#
# "SMT Demo"
# -----------------------------------------------------------------------------

from align import IBM1

if __name__ == '__main__':
	my_model = IBM1('/Users/clayton/Scripts/SMT/data/hansardstoy.f', \
					'/Users/clayton/Scripts/SMT/data/hansardstoy.e')
	my_model.em_train(10)
	print my_model['GOUVERNEMENT']['GOVERNMENT']