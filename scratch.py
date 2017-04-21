import pandas as pd
import numpy as np
from datetime import date

date_range = pd.date_range('2016-01-01', date.today())
print(date_range)