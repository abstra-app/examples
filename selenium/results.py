from abstra.workflows import get_stage
import pandas as pd

stage = get_stage()

# Get workflow variables
name = stage["name"]
email = stage["email"]

# Get dataframe from workflow variables
if stage["headlines_df"]:
    headlines = stage["headlines_df"]
    df = pd.DataFrame.from_dict(headlines)
elif stage["stocks_df"]:
    stocks = stage["stocks_df"]
    df = pd.DataFrame.from_dict(stocks)
else:
    print("no saved headlines or stocks found")

# Create dataframe from dict in stage['df']
print(df)
