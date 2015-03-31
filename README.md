# Statistical-Machine-Translation
Statistical machine translation with IBM Model 1.

This package includes:

**----- align.py -----**

Contains:

The **IBM1** class:

* The **em_train( )** method: Aligner training using expectation maximization.

* The **align_training_data( )** method: Tests functionality of aligner using training corpus itself.

* The **show_alignment( )** method: Prints the alignment to screen.

The **LanguageModel** class:

* The **estimate_probs( )** method: Estimates the probability of a trigram.

----- demo.py -----

Demos the functionality of the aligner (translation modeling and language modeling).

**----- data -----**

Hansards and Hansards toy.
