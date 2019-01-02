# ABSA Data Preprocessor

A simple way for ABSA(Aspect Base Sentiment Analysis) research data preprocessing.

### Dataset Include

* SemEval 2014
* SemEval 2015

### Demo Output:

**SemEval 2014**
```text
>>> datafile: restaurants-trial.xml
-size: 100
-datas[0] demo:
	-.id: 813
	-.text: All the appetizers and salads were fabulous, the steak was mouth watering and the pasta was delicious!!!
	-.aspect_terms: [('appetizers', 'positive', (8, 18)), ('salads', 'positive', (23, 29)), ('steak', 'positive', (49, 54)), ('pasta', 'positive', (82, 87))]
	-.aspect_categories: [('appetizers', 'positive', (8, 18)), ('salads', 'positive', (23, 29)), ('steak', 'positive', (49, 54)), ('pasta', 'positive', (82, 87))]
```

**SemEval 2015**
```text
>>> datafile: data/absa-2015_restaurants_trial.xml
-size: 10
-datas[0] demo:
	-.id (review id): 1004293
	-.sentences: [<__main__.SemEval15Sentence object at 0x100640e10>, <__main__.SemEval15Sentence object at 0x100712cc0>, <__main__.SemEval15Sentence object at 0x100640e48>, <__main__.SemEval15Sentence object at 0x100635278>, <__main__.SemEval15Sentence object at 0x10074ab00>, <__main__.SemEval15Sentence object at 0x10074a898>]
	-sentences size: 6
	-sentences[0] demo:
		-.id (sentence id): 1004293:0
		-.text: Judging from previous posts this used to be a good place, but not any longer.
		-.opinions: [('place', 'RESTAURANT#GENERAL', 'negative', ('51', '56'))]
```