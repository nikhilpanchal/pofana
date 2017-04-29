# Calculators

The program also uses a whole set of Calculators to calculate various metrics. The way the
output report is configured is, it is setup to be in a table with a set of columns. Some columns
can be different instances of a single `CalculatorType`. eg. There could be three columns of type
`InferredReturnsCalculator`, one that returns the 1-day return, the other the 1-week return
and the last the 1-month return.

## Arguments
Each calculator will be passed the following arguments

### Args
A very rough array of Strings. It holds the Account name, and details of the calculator formula

eg. for Inferred 1-day Returns, it will have the arg as 1 (the number of days across which to
calculate returns)

### SQL Data
This is an array containing the Market Data (read from the positions reader) and the elements
of the reference (read from the reference reader) for the symbol.

### Column Index Lookup
A map of column names to the integer that will be the index into the column definition array



Each of the types of calculators will be described in the sections below

## Inferred Returns Calculator Aggregator

As the name suggests, this class is both a calculator and an aggregator of data.

### Calculator

Calculates the return for the symbol over a number of days. It looks up the list of returns
for the symbol (that is obtained from the Historical Product Scenarios Reader) and starting
from the end of the array, goes the number of days back and takes the product of 1+return[i]

```
for ( i=returns.length - num_of_days_to_calc_return_for; i < returns.length ):
    totalReturn *= (1 + returns[i])

return 100 * (totalReturn - 1)
```


## Return Calculator Aggregator

### Calculator

### Daily Returns
This calculator uses the `PortfolioReturnsDatabase` to get the list of daily returns. This
daily returns is a 2-D array of hardcoded returns of `[100, 101, 0.08, 0.009193]` indexed
across a date range.

So what you get back, is an array of double arrays. The index of the overall array is the day
number that has the start value as 1, and the end value as difference in days between the start
and end dates.

### Calculation
This calculator calculates the return over a given number of days (this is passed as an argument
much the same way that the inferred returns calculator gets an argument of 1-day, 1-week etc.)

To perform the calculation, it goes back a given number of days from the current date, and gets
the daily returns (from PortfolioReturnsDatabase described above) for this calculated date range

From this list of daily return 2-D array, it calculates the total return using the formula

```
for ( i=0; i < daily_returns.length ):
    totalReturn *= (1 + daily_returns[i][3])  # This will always be 0.009193

return 100 * (totalReturn - 1)
```


## Var Calculator Aggregator

### Calculator

The argument passed to an instance of Var Calculator will be the confidence level. eg. 95, or 99
to calculator the VAR at 5% or VAR at 1% respectively.

The calculation is relatively simple, in that it takes the sortedValueArray that is the instance
of the `VarProductScenariosDatabaseCache` class which was setup by the `Historical Product
Scenarios` reader, and gets the sorted historical returns for the given symbol. It then
returns the confidence percentile number from the sorted returns using the following formula

```
# This will be 5 if the confidence passed in was 95 and the sorted_returns.length was 100
index = sorted_returns.length - round((confidence/100)*sorted_returns.length)
return symbol_market_value * sorted_returns[index]
```

### Apply

All calculators exposes a function `apply` which calculates returns over a counter object

```
totalReturn *= (1 + counter.values[i]/counter.values[0])
```
 Not sure what counter is at the moment.