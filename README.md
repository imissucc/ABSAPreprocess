# ABSA Data Preprocessor

A simple way for ABSA(Aspect Base Sentiment Analysis) research data preprocessing.

### Dataset Include

* [SemEval 2014](http://alt.qcri.org/semeval2014/task4/)
* [SemEval 2015](http://alt.qcri.org/semeval2015/task12/)
* [SemEval 2016](http://alt.qcri.org/semeval2016/task5/)

### Demo

```text
>>> 14restaurant_train
	- size: 3041
	- sample: ['But the $BNEG$ was so horrible to us', 'O O BNEG O O O O O', 'staff', 'service']

>>> 14laptop_train
	- size: 3045
	- sample: ['I charge it at night and skip taking the $BNEU$ with me because of the good $BPOS$ $IPOS$', 'O O O O O O O O O BNEU O O O O O O BPOS IPOS', 'cord,battery life', None]

>>> 15restaurant_train
	- size: 1315
	- sample: ['Judging from previous posts this used to be a good $BNEG$ but not any longer', 'O O O O O O O O O O BNEG O O O O', 'place', 'RESTAURANT#GENERAL']

>>> 15restaurant_test
	- size: 685
	- sample: ['Love $BPOS$ $IPOS$ $IPOS$', 'O BPOS IPOS IPOS', 'Al Di La', 'RESTAURANT#GENERAL']

>>> 16restaurant_train 
	- size: 2000
	- sample: ['Judging from previous posts this used to be a good $BNEG$ but not any longer', 'O O O O O O O O O O BNEG O O O O', 'place', 'RESTAURANT#GENERAL']
```