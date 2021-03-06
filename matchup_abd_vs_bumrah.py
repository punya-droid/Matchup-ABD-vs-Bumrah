# -*- coding: utf-8 -*-
"""Matchup: ABD vs Bumrah

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17lcH69WHnd4npBBkru3HB1faAZz3Keot
"""

import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', None)

df = pd.read_csv('IPL_ball_by_ball_updated.csv')
df.head(1)

df.innings.unique()

df = df[(df.innings == 1) | (df.innings == 2)]
df.innings.unique()

df[df.bowling_team == 'Mumbai Indians']['bowler'].unique() # To extract the bowler's name i.e. JJ Bumrah

df[df.batting_team == 'Royal Challengers Bangalore']['striker'].unique() # To extract striker's name i.e. AB de Villiers

req_df = df[(df.striker == 'AB de Villiers') & (df.bowler == 'JJ Bumrah')]
req_df.head()

# Parameters to be taken care of while doing the matchup:
# Runs scored
# Balls faced
# No. of dismissals
# Strike Rate

# Runs Scored
sum(req_df.runs_off_bat)

# Balls faced
len(req_df)

# No. of dismissals
len(req_df[req_df.player_dismissed == 'AB de Villiers'])

# strike Rate
sum(req_df.runs_off_bat)/len(req_df)*100

# Comparing the data of all the batsmen that bumrah has bowled to

bumrah_df = df[df.bowler == 'JJ Bumrah']

# Runs scored by different batmen against Bumrah
bdf1 = pd.DataFrame(bumrah_df.groupby('striker')['runs_off_bat'].sum()).reset_index()

# Balls faced by different batmen against Bumrah
bdf2 = pd.DataFrame(bumrah_df.groupby('striker')['ball'].count()).reset_index()

bdf3 = bdf1.merge(bdf2, on = 'striker', how = 'left')

# Adding the strike rate of different batmen against Bumrah to our dataframe
bdf3['strike_rate'] = bdf3.runs_off_bat/bdf3.ball*100
for i in bdf3['strike_rate']:
  bdf3['strike_rate'].replace(i, round(i, 2), inplace = True)       ####### imp
bdf3.head()

bdf3 = bdf3[bdf3.ball >=30] # condition that the batman must have played minimum 30 balls
bdf3.head()

abd_df = df[df.striker == 'AB de Villiers']

# Runs scored by AB de Villiers against different bowlers
adf1 = pd.DataFrame(abd_df.groupby('bowler')['runs_off_bat'].sum()).reset_index()

# Balls faced by AB de Villiers against different bowlers
adf2 = pd.DataFrame(abd_df.groupby('bowler')['ball'].count()).reset_index() 
adf2.head()

adf3 = adf1.merge(adf2, on = 'bowler', how = 'left')
adf3.head()

# Adding the strike rate of AB de Villiers against different bowlers
adf3['strike_rate'] = adf3.runs_off_bat/adf3.ball*100
for i in adf3['strike_rate']:
  adf3['strike_rate'].replace(i, round(i, 2), inplace = True)
adf3.head()

adf3 = adf3[adf3.ball >=30] # condition that the batman must have played minimum 30 balls
adf3.head()

bdf3.reset_index(inplace = True, drop = True)
adf3.reset_index(inplace = True, drop = True)

bdf3.sort_values('strike_rate', ascending = False).head() #Batmen with best strike rate against Bumrah
bdf3.head()

adf3.sort_values('strike_rate', ascending = False).head() #Ab's favorite bowlers(in terms of strike rate)
adf3.head()

plt.figure(figsize = (16,8))
plt.scatter(bdf3.strike_rate, bdf3.runs_off_bat)
 
for i in range(len(bdf3)):
    if bdf3.striker[i] == 'V Kohli':
        plt.text(bdf3.strike_rate[i] - 10, bdf3.runs_off_bat[i] - 1, bdf3.striker[i])
    elif bdf3.striker[i] == 'AB de Villiers':
        plt.text(bdf3.strike_rate[i] + 3, bdf3.runs_off_bat[i] - 3, bdf3.striker[i])
    elif (bdf3.striker[i] == 'S Dhawan') | (bdf3.striker[i] == 'KL Rahul') | (bdf3.striker[i] == 'JP Duminy') | (bdf3.striker[i] == 'MK Pandey'):
        plt.text(bdf3.strike_rate[i] + 1, bdf3.runs_off_bat[i] - 1, bdf3.striker[i])

plt.axvline(120, ls= '--', color = 'grey') # ls means line style
plt.axhline(60, ls= '--', color = 'grey')       
plt.title('Batman aginst bumrah in IPL(min 30 balls faced)', fontsize = 20)
plt.xlabel('Strike Rate')
plt.ylabel('Runs Scored')
plt.show()

plt.figure(figsize = (16,8))
plt.scatter(adf3.strike_rate, adf3.runs_off_bat)
 
for i in range(len(adf3)):
  if adf3.bowler[i] == 'HH Pandya':
    plt.text(adf3.strike_rate[i] -2 , adf3.runs_off_bat[i] + 1, adf3.bowler[i])
  elif adf3.bowler[i] == 'AD Russell':
    plt.text(adf3.strike_rate[i] - 8, adf3.runs_off_bat[i] - 3, adf3.bowler[i])
  elif (adf3.bowler[i] == 'Harbhajan Singh') | (adf3.bowler[i] == 'JJ Bumrah') | (adf3.bowler[i] == 'Sandeep Sharma') | (adf3.bowler[i] == 'SL Malinga'):
    plt.text(adf3.strike_rate[i] + 1, adf3.runs_off_bat[i] - 1, adf3.bowler[i])

plt.axvline(120, ls= '--', color = 'grey') # ls means line style
plt.axhline(80, ls= '--', color = 'grey')       
plt.title('Favorite Bowlers of AB de Villiers (min 30 balls faced)', fontsize = 20)
plt.xlabel('Strike Rate')
plt.ylabel('Runs Scored')
plt.show()

# Conclusion
# Clearly if we look at the first visualization, AB de Villiers is amongst the 6 best batsman against Bumrah in terms of the runs scored and the strike rate.
# And in the second visualization, Bumrah is amongst the top 6 favorite bowlers of AB de Villiers
# so AB clearly wins the battle