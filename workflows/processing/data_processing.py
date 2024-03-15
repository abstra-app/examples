import pandas as pd
import abstra.common as ac
import abstra.workflows as aw
import plotly.graph_objects as go

ingestion_id = aw.get_data("ingestion_id")
ingestion_file = ac.get_persistent_dir() / f"{ingestion_id}.csv"
processed_file = ac.get_persistent_dir() / f"{ingestion_id}_processed.csv"

df = pd.read_csv(ingestion_file)
df["Date"] = pd.to_datetime(df["Date"])
df.drop(columns=["Volume"], inplace=True)
# and other processing
df.to_csv(processed_file, index=False)

candlestick = go.Candlestick(
    x=df["Date"],
    open=df["Open"],
    high=df["High"],
    low=df["Low"],
    close=df["Close"],
)

fig = go.Figure(data=[candlestick])
fig.write_image(ac.get_persistent_dir() / f"{ingestion_id}.png")

aw.set_data("assignee", "reyel@abstra.app")
