## Using Machine Learning to Predict Stock Prices - Evaluating its effectiveness
*Cover image to insert for stocks![image](https://github.com/edowin25/)

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

Next, lag price features were created

