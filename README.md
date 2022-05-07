## Using Machine Learning to Predict Stock Prices - Evaluating its effectiveness

<p align="center">
  <img width="800" height="400" src="https://user-images.githubusercontent.com/50400038/167254883-850f77b8-847f-436b-aeb7-0af2a93dab83.png">
</p>

### Brief Introduction
This project is to use machine learning model to predict stock prices to aid in my options trading. Past stock prices as well as values of technical indicators like Bollinger Band width, MACD, RSI and MFI will be engineered from the price data and will be used as features for my prediction.

<!-- TABLE OF CONTENTS -->
<details open>
  <summary><b><font size=12>Table of Contents</font size></b></summary>
  <ol>
    <li><a href="#project-context">Project Context</a></li>
    <li><a href="#datasets">Datasets</a></li>
    <li><a href="#lines-of-enquiry">Lines of Enquiry</a></li>
    <li><a href="#the-process">The Process</a></li>
      <ul>
        <li><a href="#feature-engineering">Feature Engineering</a></li>
        <li><a href="#model-selection">Model Selection</a></li>
      </ul>
  </ol>
</details>

<!-- PROJECT CONTEXT -->
## Project Context
The idea is to use the predicted future prices to help me decide what kind of options trade to do by comparing the predicted price(s) with other indicators like trend and IV percentile. Currently, I am only able to guess if price will go up or down based on current data and indicators but I am always hesistant to execute the trade as I am always unsure how big is the move, up or down or when I should enter or exit the trade.

I hope that by having the price prediction I am able to make a clearer decision when to enter and exit the trade or if I should make the trade at all depending on the magnitude of the price movement.

The TA used as features are the common indicators that traders used to forecast possible price movement. For example:
- Hitting the upper and lower bands of the Bollinger Bands usually may indicate and upcoming movement in the opp direction
- RSI/MFI going above the 30/70 mark usually mean oversold/overbought pressure respectively and price may move in the direction to relieve the pressure
- Bullish/Bearish Divergences when comparing RSI/MACD chart trends with price trends also indicate certain price movement

Some of these can be seen in the image below:

<p align="center">
  <img width="800" height="450" src="images/Price_chart_TA.png">
</p>

Thus, these are used as features as it seems they are correlated to stock prices.

<!-- DATASETS -->
## Datasets
For this analysis, the datasets were obtained from the Yahoo! Finance API and generated using the python TA library

The datasets used are as follow:
1. **Daily Stock Data** 
   - Provides ***_Open, High, Low, Close, Adjusted Close and Volume_*** data
   - Date range specified to be from 2016 to current as this period shows a more consistent price movement.
   - Before 2016, there were little price movement which skew the data
  
2. **TA Library** 
   - Provides the formula to calculate the indicators data
      
<!-- LINES OF ENQUIRY -->
## Lines of Enquiry
To analyse and create the model for prediction, there are some lines of enquiry to guide us through the analysis.

1. What are the technical indicators to use?
2. How many days ahead do i want to predict?
3. How many days of past data do i want to use for training?
4. What are the best multivariate models to predict prices?
5. What metrics do i use to evaluate the model?
6. What are some challenges that I will faced?
7. Whta kind of processing needs to be done for the data?

 
<!-- THE PROCESS -->
## The Process

<!-- FEATURE ENGINEERING -->
### Feature Engineering
You may refer to the following notebooks for this step in the process:

1. DS105FP_ProjectScript_EdwinWan_1featureeng_final.ipynb
2. DS105FP_ProjectScript_EdwinWan_1featureeng_initial.ipynb

AAPL data was first generated from Yahoo! Finance for the required period and the adjusted close price was filtered for further processing.

<p align="center">
  <img width="650" height="320" src="https://user-images.githubusercontent.com/50400038/167246577-ea93f582-6dc4-4640-b760-461ee156dc2a.png">
  <img width="150" height="320" src="https://user-images.githubusercontent.com/50400038/167246803-65bcf069-42f8-4d50-b3b3-f321c8a5a275.png">
</p>

Next, a function was defined to create up to day minus 3 for lag price. Input the parameters into the function to get the dataset with the lag price data.

<p align="center">
  <img width="450" height="200" src="https://user-images.githubusercontent.com/50400038/167247156-a13f298f-42d0-4b61-830d-4f118613d4bf.png">
</p>

Following that, the TA library will be used to engineer the data for MACD, RSI/MFI, Bollinger Band Width. At this point, there will be null data up to the first 20 to 30 dates which we will drop.

<p align="center">
  <img width="500" height="100" src="https://user-images.githubusercontent.com/50400038/167252761-46324e5b-c16b-46ef-93f3-1cb1b8835e21.png">
</p>

With this data, a train-validation-test split is done to the data via slicing with the proportion as such:

- Train set: first 85% of data
- Validation set: next 7% of data
- Test set: last 8% of data

<p align="center">
  <img width="500" height="150" src="https://user-images.githubusercontent.com/50400038/167252820-5487cda7-1f63-4c6d-8e4f-109ff689d15a.png">
</p>

This proportion is used such that the train set will capture a recent volatile set of price movement (ard March 2022 to Apr 2022 period) for the ML models to learn.

With the splits, the data is processed with different treatments and run through a base LSTM model to see how the model performs with the treated set of data.

<p align="center">
  <img width="450" height="200" src="https://github.com/edowin25/stockprediction/blob/798c59cfb2a97c7fab1073022960818204161002/images/feature_treatment.png">
</p>

The best performing treated data was to use scaling with percent change transformation for prices, which also input into a Linear Regression and XGBoost model and the coefficients/feature importance was checked. It was found that MFI/RSI, and MACD data had little impact on the predictions as such these are dropped. Only lag price and Bband data were remained. 

<p align="center">
  <img width="450" height="200" src="https://github.com/edowin25/stockprediction/blob/798c59cfb2a97c7fab1073022960818204161002/images/feat_impt.png">
</p>

The correlation between the final feature was also checked and it was found that there were relatively independent from one another, which makes them ideal for the machine learning prediction.

<p align="center">
  <img width="450" height="150" src="https://github.com/edowin25/stockprediction/blob/798c59cfb2a97c7fab1073022960818204161002/images/feat_corr.png">
</p>

<!-- MODELS SELECTION -->
### Model Selection

With the final engineered data, it was run through 5 base models.

1. LSTM
2. XGBoost
3. Linear Regression
4. Ridge Regression
5. Lasso Regression

To see how well the model performs, we will be using the following metrics.

1. RMSE (this will be priority as we want the deviation from the actual price to be as low as possible)
2. MAPE
3. R2

The performance was recorded and we find that the top models is LSTM, XGBoost and Lasso Regression

<p align="center">
  <img width="450" height="200" src="https://github.com/edowin25/stockprediction/blob/798c59cfb2a97c7fab1073022960818204161002/images/model_select.png">
</p>

However, Lasso Regression was omitted as we found that the coefficients of the model was zero.

As such, LSTM and XGBoost was to be hypertuned to see if we can improve performance

<!-- HYPERPARAMETERS TUNING -->
### Hyperparameters Tuning

**LSTM**
- multiple sets of hyperparameters was input into a params dict
- for loop created to run through all sets of parameters and performance was recorded in a dataframe
- performance was then sorted with lowest RMSE at the top





