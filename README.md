# ABSA Data Preprocessor

A simple way for ABSA(Aspect Base Sentiment Analysis) research data preprocessing.

### Dataset Include

* [SemEval 2014](http://alt.qcri.org/semeval2014/task4/)
* [SemEval 2015](http://alt.qcri.org/semeval2015/task12/)

### Demo Output:

* **SemEval 2014**

```text
# SemEval14.py

>>> datafile: data/restaurants-trial.xml
-size: 100
-datas[0] demo:
	-.id: 813
	-.text: All the appetizers and salads were fabulous, the steak was mouth watering and the pasta was delicious!!!
	-.aspect_terms: [('appetizers', 'positive', (8, 18)), ('salads', 'positive', (23, 29)), ('steak', 'positive', (49, 54)), ('pasta', 'positive', (82, 87))]
	-.aspect_categories: [('food', 'positive')]
```
```text
# SemEval14PP.py, for ATE task

All the $BA$ and $BA$ were fabulous the $BA$ was mouth watering and the $BA$ was delicious,N N BA N BA N N N BA N N N N N BA N N,"appetizers,salads,steak,pasta",food
And really large $BA$,N N N BA,portions,food
The $BA$ $IA$ was excellent as was the $BA$ $IA$ and the $BA$ $IA$ but the $BA$ was forgettable,N BA IA N N N N N BA IA N N BA IA N N BA N N,"sweet lassi,lamb chettinad,garlic naan,rasamalai",food
$BA$ was quick,BA N N,Service,service
Oh don't even let me start with how expensive the $BA$ were,N N N N N N N N N N BA N,bills,price
```


* **SemEval 2015**

```text
# SemEval15.py
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
```text
# SemEval15PP.py, for ATE task

Judging from previous posts this used to be a good $BA$ but not any longer,N N N N N N N N N N BA N N N N,place,RESTAURANT#GENERAL
We there were four of us arrived at noon the place was empty and the $BA$ acted like we were imposing on them and they were very rude,N N N N N N N N N N N N N N N BA N N N N N N N N N N N N,staff,SERVICE#GENERAL
The $BA$ was lousy too sweet or too salty and the $BA$ tiny,N BA N N N N N N N N N BA N,"food,portions","FOOD#QUALITY,FOOD#STYLE_OPTIONS"
Avoid this $BA$,N N BA,place,RESTAURANT#GENERAL
Every time in New York I make it a point to visit $BA$ $IA$ on Smith Street,N N N N N N N N N N N N BA IA N N N,Restaurant Saul,RESTAURANT#GENERAL
```