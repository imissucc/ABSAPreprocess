from SemEval2014 import SemEval2014_AspectTerm
from SemEval2015 import SemEval2015_AspectTerm

if __name__ == "__main__":

    # SemEval 2014
    se14_file_name = {
        "14restaurant_train": "datasets/SemEval2014/Train/Restaurants_Train_v2.xml", # 3041
        "14laptop_train": "datasets/SemEval2014/Train/Laptop_Train_v2.xml", # 3045
    }
    se15_file_name = {
        "15restaurant_train": "datasets/SemEval2015/Train/ABSA-15_Restaurants_Train_Final.xml", # 1315
        "15restaurant_test": "datasets/SemEval2015/Test/ABSA15_Restaurants_Test.xml" # 685
    }

    se16_file_name = {
        "16restaurant_train": "datasets/SemEval2016/Train/ABSA16_Restaurants_train_SB1_v2.xml" # 2000
    }

    SemEval2014_AspectTerm(file_name=se14_file_name, rm_none_aspect=False)
    SemEval2015_AspectTerm(file_name=se15_file_name, rm_none_aspect=False)
    SemEval2015_AspectTerm(file_name=se16_file_name, rm_none_aspect=False)

