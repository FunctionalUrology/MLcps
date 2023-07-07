- [Summary](#summary)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Binder environment for MLcps](#binder-environment-for-mlcps)
- [Usage](#usage)
     - [Quick Start](#quick-start)
     - [Example 0.1](#example-01)
     - [Example 1](#example-1)
     - [Example 2](#example-2)
     - [Example 3](#example-3)
- [Links](#links)

# Summary
**MLcps: Machine Learning cumulative performance score** is a novel evaluation metric proposed for assessing the performance of machine learning models in classification problems. MLcps integrates multiple pre-computed evaluation metrics into a unified score, enabling a comprehensive assessment of the model's strengths and weaknesses. MLcps was tested on four publicly available datasets, demonstrating its ability to evaluate the overall performance and robustness of the models. By utilizing MLcps, researchers and practitioners can save valuable time and effort by relying on a single value to assess their model's performance, rather than comparing multiple individual metrics. The MLcps metric is available as a Python package, and examples of its usage can be found below. 
 
#### ***Note***:  

If you want to use MLcps without installing it on your local machine, please follow [Binder environment for MLcps](#binder-environment-for-mlcps) section. 

# Prerequisites 

1. Python >=3.8
2. R >=4.0. R should be accessible through terminal/command prompt.
3. ```radarchart, tibble,``` and ```dplyr``` R packages. MLcps can install all these packages at first import if unavailable, but we highly recommend installing them before using MLcps. The user could run the following R code in the R environment to install them:
```
## Install the unavailable packages
install.packages(c('radarchart','tibble','dplyr'),dependencies = TRUE,repos="https://cloud.r-project.org")                         
 ```

# Installation
```
pip install MLcps
```

# Binder environment for MLcps

As an alternative, we have built a binder computational environment where all the requirements for MLcps are pre-installed.
It allows the user to ***use MLcps without any installation***.

Please click here [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/FunctionalUrology/MLcps.git/main) to launch the Jupyterlab server where you can run the already available example Jupyter notebook for MLcps analysis. It may take a while to launch! You can also upload your data or notebook to perform the analysis.


# Usage

### **Quick Start**
```python
#import MLcps
from MLcps import getCPS

#calculate Machine Learning cumulative performance score
cps=getCPS.calculate(object)
```  
> * ***object***: A pandas dataframe where rows are different metrics scores and columns are different ML models. **Or** a GridSearchCV object.
> * ***cps***: A pandas dataframe with models name and corresponding MLcps. **Or** a GridSearchCV object.

### **Example 0.1**
Create Input dataframe for MLcps

```python
import pandas as pd
metrics_list=[]

#Metrics from SVC model (kernel=rbf)
acc = 0.88811 #accuracy
bacc = 0.86136 #balanced_accuracy
prec = 0.86 #precision
rec = 0.97727 #recall
f1 = 0.91489 #F1
mcc = 0.76677 #Matthews_correlation_coefficient
metrics_list.append([acc,bacc,prec,rec,f1,mcc])

#Metrics from SVC model (kernel=linear)
acc = 0.88811
bacc = 0.87841
prec = 0.90
rec = 0.92045
f1 = 0.91011
mcc = 0.76235
metrics_list.append([acc,bacc,prec,rec,f1,mcc])

#Metrics from KNN
acc = 0.78811
bacc = 0.82841
prec = 0.80
rec = 0.82
f1 = 0.8911
mcc = 0.71565
metrics_list.append([acc,bacc,prec,rec,f1,mcc])

metrics=pd.DataFrame(metrics_list,index=["SVM rbf","SVM linear","KNN"],
                     columns=["accuracy","balanced_accuracy","precision","recall",
                              "f1","Matthews_correlation_coefficient"])
print(metrics)
```

### **Example 1**
Calculate MLcps for a pandas dataframe where rows are different metrics scores and columns are different ML models.

```python
#import MLcps
from MLcps import getCPS

#read input data (a dataframe) or load an example data
metrics=getCPS.sample_metrics()

#calculate Machine Learning cumulative performance score
cpsScore=getCPS.calculate(metrics)
print(cpsScore)

#########################################################
#plot MLcps
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
pio.renderers.default = 'iframe' #or pio.renderers.default = 'browser'

fig = px.bar(cpsScore, x='Score', y='Algorithms',color='Score',labels={'MLcps Score'},
             width=700,height=1000,text_auto=True)

fig.update_xaxes(title_text="MLcps")
plot(fig)
fig
```


### **Example 2**
Calculate MLcps using the mean test score of all the metrics available in the given GridSearch object and return an updated GridSearch object. Returned GridSearch object contains ```mean_test_MLcps``` and ```rank_test_MLcps``` arrays, which can be used to rank the models similar to any other metric.

```python
#import MLcps
from MLcps import getCPS

#load GridSearch object or load it from package
gsObj=getCPS.sample_GridSearch_Object()

#calculate Machine Learning cumulative performance score
gsObj_updated=getCPS.calculate(gsObj)

#########################################################
#access MLcps
print("MLcps: ",gsObj_updated.cv_results_["mean_test_MLcps"])

#access rank array based on MLcps
print("Ranking based on MLcps:",gsObj_updated.cv_results_["rank_test_MLcps"])
```  

### **Example 3**
Certain metrics are more significant than others in some cases. As an example, if the dataset is imbalanced, a high F1 score might be preferred to higher accuracy. A user can provide weights for metrics of interest while calculating MLcps in such a scenario. Weights should be a dictionary object where keys are metric names and values are corresponding weights. It can be passed as a parameter in ```getCPS.calculate()``` function.

  * **3.a)**

```python
#import MLcps
from MLcps import getCPS

#read input data (a dataframe) or load an example data
metrics=getCPS.sample_metrics()

#define weights
weights={"Accuracy":0.75,"F1": 1.25}

#calculate Machine Learning cumulative performance score
cpsScore=getCPS.calculate(metrics,weights)
print(cpsScore)

#########################################################
#plot weighted MLcps
import plotly.express as px
from plotly.offline import plot
import plotly.io as pio
pio.renderers.default = 'iframe' #or pio.renderers.default = 'browser'

fig = px.bar(cpsScore, x='Score', y='Algorithms',color='Score',labels={'MLcps Score'},
             width=700,height=1000,text_auto=True)

fig.update_xaxes(title_text="MLcps")
plot(fig)
fig
```  
  * **3.b)**
```python
#import MLcps
from MLcps import getCPS

#########################################################
#load GridSearch object or load it from package
gsObj=getCPS.sample_GridSearch_Object()

#define weights
weights={"accuracy":0.75,"f1": 1.25}

#calculate Machine Learning cumulative performance score
gsObj_updated=getCPS.calculate(gsObj,weights)

#########################################################
#access MLcps
print("MLcps: ",gsObj_updated.cv_results_["mean_test_MLcps"])

#access rank array based on MLcps
print("Ranking based on MLcps:",gsObj_updated.cv_results_["rank_test_MLcps"])

```  

# Links
<!--* For a general introduction of the tool and how to setting up MLcps:
  * Please watch  MLcps **[Setup video tutorial]()** (coming soon).  
  *  Please watch MLcps **[Introduction video tutorial]()** (coming soon).
-->
* MLcps source code and a Jupyter notebook with sample analyses is available on the **[MLcps GitHub repository](https://github.com/FunctionalUrology/MLcps/blob/main/Example-Notebook.ipynb)** and binder [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/FunctionalUrology/MLcps.git/main).
* Please use the  **[MLcps GitHub](https://github.com/FunctionalUrology/MLcps/issues)** repository to report all the issues.

<!--# Citations Information
If **MLcps** in any way help you in your research work, please cite the MLcps publication.
***-->
