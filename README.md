For 'subject percentiles to ATAR' file:
C is computer science, M is mathematics methods, L is chemistry, S is specialists, P is physics,
0.35,0.65,0.45,0.68,0.35 means U are in the at the 35th percentile (top 65%) for computer science in WA, 65th percentile (top 35%) for methods in WA ...

example usage:

%Run 'subject percentiles to ATAR.py'
what percentile are you in each subject in the order of C,M,L,S,P? 0.35,0.65,0.45,0.68,0.35
53.5
278.5
C:
  total n = 332
  percentile * n = 116.19999999999999
  best index (1-based) = 35
  cumulative at best index = 112
  subject value without scaling = 53.5
  difference = 4.199999999999989

M:
  total n = 4205
  percentile * n = 2733.25
  best index (1-based) = 59
  cumulative at best index = 2784
  subject value without scaling = 69.5
  difference = 50.75

L:
  total n = 4508
  percentile * n = 2028.6000000000001
  best index (1-based) = 49
  cumulative at best index = 2032
  subject value without scaling = 61.5
  difference = 3.3999999999998636

S:
  total n = 1311
  percentile * n = 891.48
  best index (1-based) = 54
  cumulative at best index = 908
  subject value without scaling = 75.5
  difference = 16.519999999999982

P:
  total n = 2711
  percentile * n = 948.8499999999999
  best index (1-based) = 46
  cumulative at best index = 943
  subject value without scaling = 57.5
  difference = 5.849999999999909

[61.5, 69.5, 75.5, 57.5]
TEA components: [76.45, 61.5, 83.05, 57.5]
278.5
ATAR = 92.1657
>>>

xample usage:

92.1657 is the ATAR you would receive if 0.35,0.65,0.45,0.68,0.35 were the values showing the percentile for each subject for all of WA.
if 0.35,0.65,0.45,0.68,0.35 were the values showing the percentile for each subject for just CCGS, then your input to this file should be 92.1657, and you will get an output of 97.0957.

However, It's just a rough approximation, but it's better than nothing (no website online figures out the scaling for CCGS or any specific school) because I haven't actually gotten the data for CCGS scaling

