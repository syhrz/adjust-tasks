# Task 1

## Task Description

Please write a simple CLI application in the language of your choice that does the following:
- Print the numbers from 1 to 10 in random order to the terminal.
- Please provide a README, that explains in detail how to run the program on MacOS and Linux.

## Thinking Process

I will add a few assumtions:
- The numbers type is in integer so it will limit the scope to print array of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] in random order.
- There are a few possible solutions.

At first I think to just create an array with size of 10 with bollean type, but seems will make the process more complicated, after a few moment I think the best solution is to store the data in a list. get a random number based on the size of current list (let's say 'x') then print the value of index x and take out the number from the list, it will reduce the list size, repeat until list size become 0.

For implementation I will use python since it's already exist by defaut in  unix machines.

## Implementation

Code will be written in `task01.py`

To run the program simply execute from terminal

```
python task1.py	

```


