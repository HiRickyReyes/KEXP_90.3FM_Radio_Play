# import libraries and packages
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from PIL import Image

# set streamlit page config
st.set_page_config(layout="wide")
st.markdown(
    "<style>div.block-container{padding-top:1rem;}</style>", unsafe_allow_html=True
)

# reading in data
filepath = "/Users/ricky/data_viz/the_project/kexp/KEXP_Playlist.csv"
df = pd.read_csv(filepath, low_memory=False)
df = df.sample(n=5000, random_state=42)

# load logo
logo_filepath = "/Users/ricky/data_viz/the_project/kexp/kexp_logo.png"
image = Image.open(logo_filepath)

# create columns for the logo and title
col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.image(image, width=100)

html_title = """
    <center><h1>KEXP Tastemakers: The DJs and Artists Shaping the Airwaves</h1></center>
"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Section Divider
st.markdown("---")

# calculating top artists
artist_count = df["Artist"].value_counts().reset_index()
artist_count.columns = ["Artist", "Plays"]
artist_count = artist_count[artist_count["Artist"] != "(Various Artists)"]
artist_count = artist_count.sort_values(by="Plays", ascending=False)
top_artists = artist_count.head(10)

# calculating top hosts introducing new artists
# data preparation for stacked bar chart

# normalize artist info
df["Artist"] = df["Artist"].str.strip().str.lower()
# filter out hosts with commas, except 'Larry Mizell, Jr.'
df = df[~df["Host"].str.contains(",", na=False) | (df["Host"] == "Larry Mizell, Jr.")]
# convert datetime to fit format and year & extract year from DateTime column
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce", utc=True)
df["Year"] = df["DateTime"].dt.year
# ensure unique artist plays per year and host
unique_artist_host = df[
    ["Artist", "Host"]
].drop_duplicates()  # select unique artist plays per year and host
# group by year, host, and artist
artist_counts = unique_artist_host.groupby("Host")["Artist"].nunique().reset_index()
artist_counts.rename(columns={"Artist": "New Artists"}, inplace=True)
# find top 10 hosts with most new artists
top_hosts = artist_counts.nlargest(10, "New Artists")["Host"]
# filter data to only include top 10
filtered_df = df[df["Host"].isin(top_hosts)]
filtered_df = unique_artist_host[unique_artist_host["Host"].isin(top_hosts)]
filtered_df = df[
    ["Year", "Artist", "Host"]
].drop_duplicates()  # only unique host/artist combinations - prevents carrying across years
filtered_df = filtered_df[filtered_df["Host"].isin(top_hosts)]  # only top 10 hosts
yearly_counts = filtered_df.groupby(["Year", "Host"])["Artist"].nunique().reset_index()
yearly_counts.rename(columns={"Artist": "New Artists"}, inplace=True)
top_hosts_df = (
    artist_counts.groupby("Host")["New Artists"].sum().nlargest(10).reset_index()
)

# display tables side by side with centered text and left-aligned headers
col1, col2 = st.columns([0.5, 0.5])

with col1:
    st.markdown(
        "<center><h4>Top 10 Most Played Artists on KEXP</h4></center>",
        unsafe_allow_html=True,
    )
    # center-align text in the dataframe but left-align headers
    st.dataframe(
        top_artists.style.set_properties(**{"text-align": "center"}).set_table_styles(
            [{"selector": "th", "props": [("text-align", "left")]}]
        ),
        width=400,
        height=400,
    )

with col2:
    st.markdown(
        "<center><h4>Top 10 Hosts Introducing New Artists</h4></center>",
        unsafe_allow_html=True,
    )
    # center-align text in the dataframe but left-align headers
    st.dataframe(
        top_hosts_df.style.set_properties(**{"text-align": "center"}).set_table_styles(
            [{"selector": "th", "props": [("text-align", "left")]}]
        ),
        width=400,
        height=400,
    )

# Section Divider
st.markdown("---")

# Chart 2: Stacked Bar Chart for Hosts Introducing New Artists
fig2 = px.bar(
    yearly_counts,
    x="Year",
    y="New Artists",
    color="Host",
    labels={"New Artists": "Number of New Artists"},
    color_discrete_sequence=px.colors.sequential.Viridis,
)

fig2.update_layout(
    xaxis=dict(rangeslider=dict(visible=True), type="linear"),
    legend=dict(title="Host"),
    xaxis_title="Year",
    yaxis_title="Number of New Artists",
)

st.markdown(
    "<center><h4>KEXP Top 10 Hosts: Champions of New Artist Introductions</h4></center>",
    unsafe_allow_html=True,
)
st.plotly_chart(fig2, use_container_width=True)

# Section Divider
st.markdown("---")

# Chart 1: Top Artists Over Time
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce", utc=True)
df.dropna(subset=["DateTime"], inplace=True)
df["DateTime"] = df["DateTime"].dt.tz_localize(None)
df = df[df["Artist"] != "(Various Artists)"]
df["Month"] = df["DateTime"].dt.to_period("M")

artist_play_count = df.groupby(["Month", "Artist"]).size().reset_index(name="Plays")

all_months = pd.date_range(
    start=df["DateTime"].min(), end=df["DateTime"].max(), freq="M"
).to_period("M")
all_artists = artist_play_count["Artist"].unique()
all_combinations = pd.MultiIndex.from_product(
    [all_months, all_artists], names=["Month", "Artist"]
)
artist_play_count = (
    artist_play_count.set_index(["Month", "Artist"])
    .reindex(all_combinations, fill_value=0)
    .reset_index()
)

artist_play_count = artist_play_count.sort_values(by="Month")
artist_play_count["TotalPlaysToDate"] = (
    artist_play_count.groupby("Artist")["Plays"]
    .expanding()
    .sum()
    .reset_index(level=0, drop=True)
)

top10_per_month = pd.DataFrame()
for month in sorted(artist_play_count["Month"].unique()):
    cumulative_data = artist_play_count[artist_play_count["Month"] <= month]
    cumulative_totals = (
        cumulative_data.groupby("Artist")["TotalPlaysToDate"].max().reset_index()
    )
    cumulative_totals["Month"] = month
    top10_this_month = cumulative_totals.sort_values(
        by="TotalPlaysToDate", ascending=False
    ).head(10)
    top10_this_month["Rank"] = range(1, len(top10_this_month) + 1)
    top10_per_month = pd.concat([top10_per_month, top10_this_month], ignore_index=True)

top10_per_month["PlaySize"] = top10_per_month["TotalPlaysToDate"]

fig = px.scatter(
    top10_per_month,
    x="Rank",
    y="TotalPlaysToDate",
    size="PlaySize",
    color="Artist",
    animation_frame="Month",
    animation_group="Artist",
    text="Artist",
    labels={"TotalPlaysToDate": "Cumulative Plays by Artist", "Rank": "Rank"},
    height=800,
    width=1200,
    size_max=65,
)

fig.update_layout(
    xaxis=dict(tickmode="linear", dtick=1, range=[0.5, 10.5]),
    yaxis=dict(range=[0, top10_per_month["TotalPlaysToDate"].max() + 100]),
)

st.markdown(
    "<center><h4>Who Dominated the KEXP Airwaves? Top 10 Artists Over Time</h4></center>",
    unsafe_allow_html=True,
)
st.plotly_chart(fig, use_container_width=True)

# Section Divider
st.markdown("---")

# Source Information
st.markdown(
    """
    **Source:** This visualization is based on exploratory analysis of the KEXP playlist dataset. 
    The original analysis and dataset usage guide can be found at 
    [this Kaggle notebook](https://www.kaggle.com/code/eric27n/kexp-fm-play-analysis). 
    """,
    unsafe_allow_html=True,
)

# Last Updated Section
last_updated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(
    f"""
    **Last Updated:** {last_updated}
    """,
    unsafe_allow_html=True,
)
