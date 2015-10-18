# Statistical-Machine-Translation
Statistical machine translation with IBM Model 1.

This package includes:

**----- align.py -----**

The **IBM1** class:

* The **em_train( )** method: Aligner training using expectation maximization.

* The **align_training_data( )** method: Tests functionality of aligner using training corpus itself.

* The **show_alignment( )** method: Prints the alignment to screen.

The **LanguageModel** class:

* The **estimate_probs( )** method: Estimates the probability of a trigram.

**----- demo.py -----**

Demos the functionality of the aligner (translation modeling and language modeling).

**----- data -----**

Hansards.
Hansards Toy.

## Understanding the Demo Output

### Firstly, 
the alignment results are printed with the source language on the left and the target translation on the right:

SOCIÉTÉ SOCIETY

DISTINCTE DISTINCT

### Secondly, 
some translation model probabilities are printed for various example alignments. In the case of demo.py, these include (they are changeable from within the script):

['OUI']['YES']  0.966022834098

['IL']['HE']    0.397326281738

['IL']['IT']    0.0245976078319

['NATIONALE']['NATIONAL']   0.956317486814

['BILINGUISME']['BILINGUALISM'] 0.640228314125

### Thirdly, 
a dictionary of trigram probabilities from the language model is printed. In the case of demo.py, these include:

the START tag (in other words, word initial bigrams)
	
'he'
	
'radio'

Taking the example of 'radio', the results will look something like this:

{'and': {'print': 0.36363636363636365, 'television': 0.36363636363636365, 'film': 0.18181818181818182, 'existing': 0.09090909090909091}, 'stations': {'<END>': 1.0}, 'television': {'and': 1.0}, 'show': {'money': 1.0}, 'interviews': {'with': 1.0}, 'that': {'jacques': 1.0}, 'system': {'in': 1.0}, 'broadcasting': {'of': 0.6, 'the': 0.2, 'be': 0.2}, 'broadcast': {'was': 1.0}, 'station': {'<END>': 0.14285714285714285, 'that': 0.14285714285714285, 'is': 0.14285714285714285, 'which': 0.2857142857142857, 'in': 0.14285714285714285, 'the': 0.14285714285714285}, 'promoting': {'it': 1.0}, 'quebec': {'<END>': 0.5, 'was': 0.5}, 'marine': {'vcn': 1.0}, 'he': {'did': 1.0}}

The dictionary entry is the neighborhing word, with each imbedded dictionary giving the third word and the trigram probability.

## Method and Analysis
The IBM1 class defines a translation model based on the basic IBM1 algorithm. 

### First, 
_self.parallelize() is called within align_training_data() in order to create a parallel text between source and target language (French-English in the case of Hansards). 

### Secondly, 
the teetable is updated with the translation model probability. This is accomplished by training with em_train, a method which recursively maximizes the probability of p(s|t). The inherent very basic counting nature of this method is what gives IBM1 its inaccuracy. It is a basic algorithm which counts occurances and divides by a normalizer in the maximization step. It forms a good basis for implementing more complex methods.

### Thirdly
the language model is initialized. In this case of this program, this is a trigram model. First, trigram occurances are collected with _get_trigrams(), and then passed on to estimate_probs(), which returns traigram probabilities.

## For the Future
obviously, the IBM1 falls short in that it so dumbly maximizes probablities during the estimation-maximization loop. However, it still is very important for machine translation systems because it calculates p(target|source) which is used in other systems and serves as a basis for many othermore complex translation systems. To understand IBM1 is to understand the basis of the Noisy Model for machine translation.

