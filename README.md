# gensite
Can be found at: http://jordand777.pythonanywhere.com

Web App for valuing numbers by uploading csv with a column of phone numbers. Patterns are recognised using regex expressions and then a csv file is returned
providing a masked number and the pattern that was found.

Business Problem:
During my placement year I started a small business selling phone numbers on ebay. This involved sorting through 1000's of numbers to find ones that may be valuable, specifically numbers with repeating digits or patterns of digits that would be easy to remember to look good to read on websites or advertising. At first we used excel to find numbers with patterns using various formulas, this worked but was sluggish and we still had to manually price the numbers and prepare advertisements to list the numbers. This issue became exponentially worse as the business began to grow.

Solution:
As I was starting to get more interested into computer science, I decided to attempt to solve this business problem by creating a web app. This would allow any of us at the business to automatically price and prepare as many numbers as we need. To do this i used python to read through a csv of the phonenumbers, for each number I would use regex to recognise patterns in the numbers. As each number could match several different patterns, to return only the most valuable pattern, I used a formula (repeat_amount * log10(len(number_group)). This allowed the number of repeats to be valued higher than the length of the pattern, which fit our model for valuing numbers. The result would be a new csv file that would include the phone number, a masked version of the number, which is just the same phone number with non pattern numbers masked by an '*'. The pattern was also included, which would allow us to easily change the price of each pattern in excel after we had gotten the patterns for the numbers.
