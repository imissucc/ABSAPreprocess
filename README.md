# ABSA Data Preprocessor

A simple way for ABSA(Aspect Base Sentiment Analysis) research data preprocessing.

### Dataset Include

* [SemEval 2014](http://alt.qcri.org/semeval2014/task4/)
* [SemEval 2015](http://alt.qcri.org/semeval2015/task12/)
* [SemEval 2016](http://alt.qcri.org/semeval2016/task5/)

### Demo

* **Aspect Term Extraction Task**

```text
>>> 14restaurant_train
	- origin size: 3041
	- verified size: 3041
	- pop count: 0
	- sample: ['But the staff was so horrible to us', 'O O B O O O O O', 'staff', 'service']

>>> 14laptop_train
	- origin size: 3045
	- verified size: 3045
	- pop count: 0
	- sample: ['I charge it at night and skip taking the cord with me because of the good battery life', 'O O O O O O O O O B O O O O O O B I', 'cord,battery life', None]

[WARN] ABNORMAL DATA: ['', 'O', None, 'RESTAURANT#GENERAL']
>>> 15restaurant_train
	- origin size: 1315
	- verified size: 1314
	- pop count: 1
	- sample: ['Judging from previous posts this used to be a good place but not any longer', 'O O O O O O O O O O B O O O O', 'place', 'RESTAURANT#GENERAL']

>>> 15restaurant_test
	- origin size: 685
	- verified size: 685
	- pop count: 0
	- sample: ['Love Al Di La', 'O B I I', 'Al Di La', 'RESTAURANT#GENERAL']

[WARN] ABNORMAL DATA: ['', 'O', None, 'RESTAURANT#GENERAL']
>>> 16restaurant_train
	- origin size: 2000
	- verified size: 1999
	- pop count: 1
	- sample: ['Judging from previous posts this used to be a good place but not any longer', 'O O O O O O O O O O B O O O O', 'place', 'RESTAURANT#GENERAL']
```

* **Open Domain ABSA Task**

```text
>>> 14restaurant_train
	- origin size: 3041
	- verified size: 3041
	- pop count: 0
	- sample: ['But the staff was so horrible to us', 'O O B-NEG O O O O O', 'staff']

>>> 14laptop_train
	- origin size: 3045
	- verified size: 3045
	- pop count: 0
	- sample: ['I charge it at night and skip taking the cord with me because of the good battery life', 'O O O O O O O O O B-NEU O O O O O O B-POS I-POS', 'cord,battery life']

[WARN] DROPED DATA: ['', 'O', None]
>>> 15restaurant_train
	- origin size: 1315
	- verified size: 1314
	- pop count: 1
	- sample: ['Judging from previous posts this used to be a good place but not any longer', 'O O O O O O O O O O B-NEG O O O O', 'place']

>>> 15restaurant_test
	- origin size: 685
	- verified size: 685
	- pop count: 0
	- sample: ['Love Al Di La', 'O B-POS I-POS I-POS', 'Al Di La']

[WARN] DROPED DATA: ['', 'O', None]
>>> 16restaurant_train
	- origin size: 2000
	- verified size: 1999
	- pop count: 1
	- sample: ['Judging from previous posts this used to be a good place but not any longer', 'O O O O O O O O O O B-NEG O O O O', 'place'] 
```