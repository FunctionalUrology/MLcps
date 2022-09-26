#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:20:50 2022
@author: akshay
"""

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
from rpy2.robjects import pandas2ri,conversion
from rpy2.robjects.vectors import StrVector
utils = importr('utils')

pandas2ri.activate()


#load or install packages
try:
    radarchart=importr("radarchart")
except:
    utils.install_packages("radarchart",repos="https://cloud.r-project.org",type="source")
    radarchart=importr("radarchart")

try:
    tibble=importr("tibble")
except:
    utils.install_packages("tibble",repos="https://cloud.r-project.org",type="source")
    tibble=importr("tibble")

try:
    dplyr=importr("dplyr")
except:
    utils.install_packages("dplyr",repos="https://cloud.r-project.org",type="source")
    dplyr=importr("dplyr")


#define getArea function
robjects.r(''' getArea<-function(metrics_score)
    {
     metrics_score<-as.data.frame(t(metrics_score))
      metrics_score= lapply(metrics_score, function(x) as.numeric(x))
      metrics_score_tbl <- metrics_score%>% as_tibble()

      # PLOT THE CHART
      chartJSRadar(scores=metrics_score_tbl,
                   labs=rownames(metrics_score),
                   maxScale = 100,
                   labelSize=12,
                   addDots=TRUE,
                   height=8,
                   width=8,
                   showToolTipLabel=TRUE,
                   polyAlpha=0.3,
                   colMatrix= grDevices::col2rgb(c("green", "grey","red", "pink")),
                   scaleStepWidth=20,                             #Spacing between rings on radar
                   scaleStartValue=0
                  )

      # Function to calculate the Area
      babooneh <- function(vec)
      {
        sinAngles <- sin(360/length(vec)*pi/180)             # Calculate sine once as radar angles are equal
        vec <- c(vec,vec[1])                                 # Append the 1st value at the end of the vector

        # NESTED RECURSIVE FUNCTION
        vecPairSum <- function(vec,i=1,rVec=c())
        {
          # If there is a next vector element (vec[i] is not the last)
          if(!is.na(vec[i+1]))
          {
            # Call self with this score x next score as return vector rVec
            vecPairSum(vec,i+1,c(rVec,(vec[i] * vec[i+1])))
          }

          # no more elements, return the return vector rVec
          else { return(rVec)}
        }
        distanceVec <- vecPairSum(vec)                      # initial call to vecPairSum with the scores vector
        return(sum(distanceVec * sinAngles)/2)              # sum every score distance and angle delta sin and divide by 2
      }

      #calculate area
      areaAlgorithms <-  apply(metrics_score_tbl[1:length(metrics_score_tbl)],2,babooneh)

      #create a dataframe
      areaAlgorithms <- as.data.frame(areaAlgorithms)
      colnames(areaAlgorithms) <- "Score"

      #add first column name as "ML_ResamplingAlgorithms"
      areaAlgorithms <- areaAlgorithms%>%
        rownames_to_column(var="Algorithms")%>% as_tibble()

      #sort based on areas
      areaAlgorithms <- areaAlgorithms %>%
        arrange(Score)
      return(areaAlgorithms)
  }
''')

getArea = robjects.r['getArea']

def calculate(metrics,weight={}):
    import pandas as pd

    #for gridsearchcv
    #if isinstance(metrics,sklearn.model_selection._search.GridSearchCV):
    if isinstance(metrics,pd.DataFrame)==False:
        result=metrics.cv_results_
        data={}
        for met in result.keys():
            if "mean_test_" in met:
                metName=met.replace("mean_test_","")
                data[metName]=list(result[met])

        data_df = pd.DataFrame(data)
        data_df.index =range(1,data_df.shape[0]+1)


        #add weightts if available
        if weight:
            for met in weight.keys():
                data_df[met]=data_df[met].mul(weight[met])


        data_df=pandas2ri.py2rpy_pandasdataframe(data_df)
        area=getArea(data_df)
        data_cps = conversion.rpy2py(area)

        data_cps = data_cps.astype({"Algorithms": int})
        data_cps=data_cps.sort_values(by='Algorithms')

        result["mean_test_MLcps"]=data_cps.iloc[:,1].to_numpy()
        result["rank_test_MLcps"]=data_cps['Score'].rank(method='dense',ascending=False).to_numpy().astype(int)
        metrics.cv_results_=result

        return metrics

    #for result df
    else:
        #add weightts if available
        if weight:
            for met in weight.keys():
                metrics[met]=metrics[met].mul(weight[met])

        metrics_df=pandas2ri.py2rpy_pandasdataframe(metrics)
        area=getArea(metrics_df)
        area_pandas = conversion.rpy2py(area)
        return area_pandas


import pandas as pd
import pickle
import pkg_resources

def sample_metrics():
    DATA_PATH = pkg_resources.resource_filename('MLcps', 'metrices.csv')
    return pd.read_csv(DATA_PATH, encoding='latin-1',index_col=0)

def sample_GridSearch_Object():
    DATA_PATH = pkg_resources.resource_filename('MLcps', 'GridSearchCV-object.pickle')
    return pickle.load(open(DATA_PATH,'rb'))
