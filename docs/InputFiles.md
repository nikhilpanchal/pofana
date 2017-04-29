# Input File Readers

The portfolio analytics project takes in various kinds of files for which there are multiple
types of readers and processors. Each of these will be described here.


## Positions

Simple reader of the positions in the portfolio. The input file contains a list of symbols and
market-value pairs, that is read in and returned as an array of `Position` objects.

Each `Position` object holds the symbol and the market-value to represent a position.

## Reference Data Lookup

Takes in a list of symbols and their reference data points that are the following

 * Some number that looks like an index
 * Company Name
 * Sector
 * Country of Incorporation
 * Currency of Trade
 * Some 8 digit number that's converted to a String and truncated to 7
 characters that's probably the market cap

Each of the above data points are stored in an Object[] array, and the reader returns back
a map of symbol -> Object[]   (symbol -> Reference data)

## Product Scenarios

Takes in an input file that has a list of symbol and five price points for each symbol

 1. The Price
 1. The Price * (1.01)
 1. The Price * (0.99)
 1. The Price * (1.05)
 1. The Price * (0.95)

Returns a map of symbol -> double[] Array of the 5 numbers described above.

## Historical Product Scenarios

 * Takes in the list of symbols in the S&P and their individual prices over a range of time.
 There is a year's worth of price information for each symbol.
 * It then calculates the daily return for each symbol based on these prices like so
   * return[i] = ((price[day_i+1] / price[day_i]) - 1)
   * The returns array length will be of one less than the price array
 * It returns a map of symbol -> daily_returns_for_a_year

There are a bunch of other numbers in the input excel sheet, my guess is these are probably
other prices (open_price, highest_price, trade_price, etc.). This reader just deals with the
first price for each day and then calculates the return across days.

An interesting point to note, is the historical returns are stored in an object of the
`VarProductScenariosDatabaseCache` class, which holds another map of the symbol and the sorted
returns. This map is used for the VAR calculation later in the program.


*The thing to note, is the price that's in the Product Scenarios file is **not** the same as
the one in the Historical Product scenarios one. The price numbers for each symbol appear to
be at different times*
