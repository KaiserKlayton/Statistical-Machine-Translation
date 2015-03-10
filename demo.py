#!/usr/bin/env python
#
# "SMT Demo"
# -----------------------------------------------------------------------------

from align import IBM1

if __name__ == '__main__':
	# TRAIN ALIGNMENT #
	my_model = IBM1('/Users/clayton/Scripts/SMT/data/hansardstoy.f', \
					'/Users/clayton/Scripts/SMT/data/hansardstoy.e')
	my_model.em_train(10)
#	print my_model['OUI']['YES']
#	print my_model['IL']['HE']
#	print my_model['IL']['IT']
#	print my_model['NATIONALE']['NATIONAL']
#	print my_model['CANADIENNE']['CANADIAN']
#	print my_model['CANADIEN']['CANADIAN']
#	print my_model['BILINGUISME']['BILINGUALISM']

	# TRAIN LANGUAGE MODEL #

	# DECODE #
	my_decoding = my_model.decode_training_data()
	my_model.show_decoding(my_decoding)
