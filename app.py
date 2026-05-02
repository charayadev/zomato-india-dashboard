import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
# library import



# page configration setup for titile 
st.set_page_config(page_title="Zomato Restaurant Analysis", layout="wide")

# header section basic CSS set up
st.markdown("""
<style>
.header{
    background-color:#E23744;
    border-radius:12px;
    padding:28px 36px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:25px;
}
.header-left{display:flex;align-items:center;gap:16px;}
.header-icon{width:42px;height:42px;border-radius:50%;background:rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;}
.header-title{color:white;font-size:1.5rem;font-weight:500;margin:0;}
.header-sub{color:rgba(255,255,255,0.75);font-size:0.85rem;margin:3px 0 0;}
.header-right{display:flex;gap:8px;}
.badge{background:rgba(255,255,255,0.15);border-radius:20px;padding:5px 16px;color:white;font-size:0.78rem;}
</style>
<div class="header">
    <div class="header-left">
        <div class="header-icon">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z" fill="white"/>
            </svg>
        </div>
        <div>
            <div class="header-title">Zomato Restaurant Analysis</div>
            <div class="header-sub">India </div>
        </div>
    </div>
    <div class="header-right">
        <span class="badge">India Only</span>
        <span class="badge">7,752 Restaurants</span>
    </div>
</div>
""", unsafe_allow_html=True) #header section HTML ends here

# load the data
df = pd.read_csv(r"C:\Users\HP\OneDrive\Desktop\Zomato_data_analysis\Zomato_data_clean.csv", encoding="latin1")
# data load check
# st.write(df.head())

# filters side bar 
st.sidebar.markdown("## Filters")

# Reset button approach to make new widgets keys on each click
if "reset_count" not in st.session_state:
    st.session_state.reset_count = 0

# Map working as slicer
if "map_city" not in st.session_state:
    st.session_state.map_city = "All"

# after reset sesseion state reset increase
rc = st.session_state.reset_count

# filters for various things 
# sorted citys
# City list
city_list = ["All"] + sorted(df["City"].dropna().unique().tolist())

# If map city is clicked pre-select it in dropdown
city_default = 0
if st.session_state.map_city != "All" and st.session_state.map_city in city_list:
    city_default = city_list.index(st.session_state.map_city)

city = st.sidebar.selectbox("City",
    city_list,
    index=city_default,
    key=f"city_{rc}")

# sorted cusines
cuisine = st.sidebar.selectbox("Cuisine",
    ["All"] + sorted(df["Cuisines"].dropna().unique().tolist()),
    key=f"cuisine_{rc}")

# online delivery
delivery = st.sidebar.selectbox("Online Delivery",
    ["All", "Yes", "No"],
    key=f"delivery_{rc}")

# table boookibg filter
table = st.sidebar.selectbox("Table Booking",
    ["All", "Yes", "No"],
    key=f"table_{rc}")

# rating bar filter
min_rating = st.sidebar.slider("Minimum Rating",
    min_value=0.0, max_value=5.0,
    value=0.0, step=0.5,
    key=f"min_rating_{rc}")

# Apply filters to the data
filtered_df = df.copy() # the new filtered  data makes the copy of the dataframe to apply the filter and seen on the page
# city filter apply
if city != "All":
    filtered_df = filtered_df[filtered_df["City"] == city]

# cuisine filter apply
if cuisine != "All":
    filtered_df = filtered_df[filtered_df["Cuisines"] == cuisine]

# online delivery filter apply
if delivery != "All":
    filtered_df = filtered_df[filtered_df["Has Online delivery"] == delivery]

# table booking filter apply
if table != "All":
    filtered_df = filtered_df[filtered_df["Has Table booking"] == table]
filtered_df = filtered_df[filtered_df["Aggregate rating"] >= min_rating]





# returns the total filtered values 
st.sidebar.markdown(f"**{len(filtered_df)} restaurants found**")

# know when we click the above state for the seeion reset count increases as button is at the last
if st.sidebar.button("Reset All Filters"):
    st.session_state.reset_count += 1
    st.session_state.map_city = "All"
    st.rerun()


# KPI cards markdown for the HTML and CSS
st.markdown("<br>", unsafe_allow_html=True)

# the rating must be greater than 0 as practially it will be
rated_df = filtered_df[filtered_df["Aggregate rating"] > 0]

# major KPI Values And calculations
# total reasurent in the data
total = len(filtered_df)

# avg rating in the restaurent
avg_rating = round(rated_df["Aggregate rating"].mean(), 1) if len(rated_df) > 0 else 0.0

# avg cost spend by two
avg_cost = int(filtered_df["Average Cost for two"].fillna(0).mean()) if len(filtered_df) > 0 else 0

# delivery % shown
delivery_pct = round(filtered_df[filtered_df["Has Online delivery"] == "Yes"].shape[0] / max(total, 1) * 100)

# table booking % shown 
table_pct = round(filtered_df[filtered_df["Has Table booking"] == "Yes"].shape[0] / max(total, 1) * 100)

#CSS for the KPI 
st.markdown(f"""
<style>
.kpi-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 14px;
    margin-bottom: 28px;
}}
.kpi-card {{
    background: white;
    border-radius: 10px;
    padding: 14px 16px;
    border-left: 3px solid #E23744;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: pointer;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.kpi-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 6px 16px rgba(226,55,68,0.15);
}}
.kpi-label {{
    font-size: 10px;
    color: #999;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-weight: 500;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.kpi-value {{
    font-size: 22px;
    font-weight: 600;
    color: #E23744;
    line-height: 1;
}}
.kpi-sub {{
    font-size: 11px;
    color: #bbb;
    margin-top: 6px;
}}
</style>
            

<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Total Restaurants</div>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-sub">Across all cities</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avg Rating</div>
        <div class="kpi-value">{avg_rating}</div>
        <div class="kpi-sub">Out of 5.0</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Avg Cost for Two</div>
        <div class="kpi-value">₹{avg_cost:,}</div>
        <div class="kpi-sub">Per visit</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Online Delivery</div>
        <div class="kpi-value">{delivery_pct}%</div>
        <div class="kpi-sub">Offer delivery</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Table Booking</div>
        <div class="kpi-value">{table_pct}%</div>
        <div class="kpi-sub">Accept bookings</div>
    </div>
</div>
 """, unsafe_allow_html=True)     #  HTML for the KPI


# know lets begin with the visualization charts to understand the data

# a line to divide the chart and KPI and UI Looking
st.markdown("---")
col1, col2 = st.columns(2) # two charts in the 2 columns 

# Chart 1 — top  cities with most resasurents
with col1:
    city_count = filtered_df["City"].value_counts().head(10).reset_index() # this counts th  particluar in that city and shows the top 10 city 
    city_count.columns = ["City", "Count"] # total count in that city
    
    # here the chart is set up and css is added for that
    fig1 = px.bar(city_count, x="Count", y="City",
        orientation="h",
        title="Top 10 Cities by Restaurants",
        color="Count",
        color_continuous_scale=["#FFE0E3","#E23744"],
        text="Count")
    
    
    # css for the chart
    fig1.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        showlegend=False, coloraxis_showscale=False,
        height=420,
        yaxis=dict(categoryorder="total ascending",
                   tickfont=dict(size=12), title=""),
        xaxis=dict(showgrid=True, gridcolor="#f5f5f5",
                   tickfont=dict(size=11),
                   title="Number of Restaurants"),
        title_font=dict(size=15, color="#1a1a1a"),
        margin=dict(t=55, b=40, l=20, r=60),
        font=dict(family="Arial"))
    fig1.update_traces(textposition="outside",
        textfont=dict(size=11, color="#333"),
        marker_line_width=0)
    
    # hcart is shown here
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2 — Rating Distribution to see most common rating with count of reasturent
with col2:
    rated = filtered_df[filtered_df["Aggregate rating"] > 0] # takes the rating that is greater than 0  only
    rating_counts = rated["Aggregate rating"].value_counts().sort_index().reset_index() # than count that ratings how many in each
    rating_counts.columns = ["Rating", "Count"] # see the rating and count

    # chart setup and CSS for the chart
    fig2 = px.area(rating_counts, x="Rating", y="Count",
        title="Rating Distribution",
        color_discrete_sequence=["#E23744"])
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=420,
        xaxis=dict(showgrid=False, tickfont=dict(size=11),
                   title="Rating", dtick=0.5),
        yaxis=dict(showgrid=True, gridcolor="#f5f5f5",
                   tickfont=dict(size=11),
                   title="Number of Restaurants"),
        title_font=dict(size=15, color="#1a1a1a"),
        margin=dict(t=55, b=40, l=20, r=20),
        font=dict(family="Arial"))
    fig2.update_traces(
        line=dict(width=2.5),
        fillcolor="rgba(226,55,68,0.15)")
    # chart is shown here
    st.plotly_chart(fig2, use_container_width=True)



# again separator for the next two charts and better Ui experince
st.markdown("---")
col3, col4 = st.columns(2) #two chart in 2 columns

# Chart 3 — Lollipop Chart resurent count of the cusine
with col3:
    cuisine_count = filtered_df["Cuisines"].value_counts().head(10).reset_index() # counts the cuisines only top 10
    cuisine_count.columns = ["Cuisine", "Count"] # cussines and count
    cuisine_count = cuisine_count.sort_values("Count", ascending=True) # sort the according to the count


    #  for this we will use go  to make the lollipop chart
    fig3 = go.Figure()

    # Lines of the cusines with CSS
    for i, row in cuisine_count.iterrows():
        fig3.add_shape(
            type="line",
            x0=0, x1=row["Count"],
            y0=row["Cuisine"], y1=row["Cuisine"],
            line=dict(color="#FFE0E3", width=3))

    # Dots whhich shows the count with CSS
    fig3.add_trace(go.Scatter(
        x=cuisine_count["Count"],
        y=cuisine_count["Cuisine"],
        mode="markers+text",
        marker=dict(
            color="#E23744",
            size=14,
            line=dict(color="white", width=2)),
        text=cuisine_count["Count"],
        textposition="middle right",
        textfont=dict(size=11, color="#333"),
        hovertemplate="<b>%{y}</b><br>Restaurants: %{x}<extra></extra>"))

# CSS for the chart 
    fig3.update_layout(
        title="Top 10 Cuisines",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        title_font=dict(size=15, color="#1a1a1a"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f5f5f5",
            tickfont=dict(size=11),
            title="Number of Restaurants",
            range=[0, cuisine_count["Count"].max() * 1.25]),
        yaxis=dict(
            tickfont=dict(size=11, color="#444"),
            title=""),
        margin=dict(t=55, b=40, l=20, r=60),
        font=dict(family="Arial"),
        showlegend=False)

    # show the chart 
    st.plotly_chart(fig3, use_container_width=True)




# Chart 4 — Two Donuts for the deliveru and booking % shown
with col4:
    
    yes_del = filtered_df[filtered_df["Has Online delivery"]=="Yes"].shape[0] # count the  yes for thje delivery

    no_del = filtered_df[filtered_df["Has Online delivery"]=="No"].shape[0] # count the  No for the delivery

    yes_tbl = filtered_df[filtered_df["Has Table booking"]=="Yes"].shape[0] # count the yes fro table booking

    no_tbl = filtered_df[filtered_df["Has Table booking"]=="No"].shape[0] # count the no fro table booking

    total = max(len(filtered_df), 1) #count the data filter

    fig4 = make_subplots( # makes the two subplots for the donut chart  
        rows=1, cols=2,
        specs=[[{"type":"pie"},{"type":"pie"}]], # type given
        subplot_titles=["",""])

    # first chart for the delivery
    fig4.add_trace(go.Pie(
        labels=["Yes","No"],
        values=[yes_del, no_del],
        hole=0.68,
        pull=[0.06, 0],
        marker=dict(
            colors=["#F00D20","#a23d3d"],
            line=dict(color="white", width=4)),
        textinfo="none",
        name="Delivery",
        showlegend=True,
        sort=False,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"),
        row=1, col=1) 

# second chart for the table booking
    fig4.add_trace(go.Pie(
        labels=["Yes","No"],
        values=[yes_tbl, no_tbl],
        hole=0.68,
        pull=[0.06, 0],
        marker=dict(
            colors=["#F00D20","#a23d3d"],
            line=dict(color="white", width=4)),
        textinfo="none",
        name="Table",
        showlegend=False,
        sort=False,
        hovertemplate="<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>"),
        row=1, col=2) 

# CSS for the chart
    fig4.update_layout(
        title=dict(
            text="Delivery & Table Booking",
            font=dict(size=15, color="#1a1a1a"),
            x=0, xanchor="left"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        annotations=[
            dict(text=f"<b>{round(yes_del/total*100)}%</b><br>Delivery",
                 x=0.18, y=0.5,
                 font=dict(size=16, color="#E23744", family="Arial"),
                 showarrow=False),
            dict(text=f"<b>{round(yes_tbl/total*100)}%</b><br>Booking",
                 x=0.82, y=0.5,
                 font=dict(size=16, color="#E23744", family="Arial"),
                 showarrow=False),
            dict(text="Online Delivery",
                 x=0.18, y=1.05,
                 font=dict(size=12, color="#888", family="Arial"),
                 showarrow=False),
            dict(text="Table Booking",
                 x=0.82, y=1.05,
                 font=dict(size=12, color="#888", family="Arial"),
                 showarrow=False)],
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.12,
            xanchor="center", x=0.5,
            font=dict(size=12),
            itemsizing="constant"),
        margin=dict(t=65, b=40, l=20, r=20),
        font=dict(family="Arial"))

# show the chart
    st.plotly_chart(fig4, use_container_width=True)


# again markdwin for the seprator and better UI
st.markdown("---")
col5, col6 = st.columns(2)


## Chart 5 — Cost vs Rating — Top 10 Restaurants by Votes
with col5:
    top10_df = filtered_df[filtered_df["Aggregate rating"] > 0].nlargest(10, "Votes").reset_index(drop=True) # filter the avg rating based 10 resurents based on the votes



# the chart is set up and css for the style
    fig5 = px.scatter(top10_df,
        x="Average Cost for two",
        y="Aggregate rating",
        size="Votes",
        color="Rating text",
        title="Top 10 Restaurants — Cost vs Rating vs Popularity",
        color_discrete_map={
            "Excellent": "#1a9641",
            "Very Good": "#74b72e",
            "Good": "#fdae61",
            "Average": "#E23744",
            "Poor": "#d7191c"},
        size_max=45)

    fig5.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        title_font=dict(size=15, color="#1a1a1a"),
        xaxis=dict(
            showgrid=True,
            gridcolor="#f5f5f5",
            tickfont=dict(size=11),
            title="Average Cost for Two (₹)"),
        yaxis=dict(
            showgrid=True,
            gridcolor="#f5f5f5",
            tickfont=dict(size=11),
            title="Rating",
            range=[3.2, 5.3]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.28,
            xanchor="center", x=0.5,
            font=dict(size=11),
            title=""),
        margin=dict(t=55, b=80, l=20, r=20),
        font=dict(family="Arial"))

    # on hover too tip in clean fromat with data
    fig5.update_traces(
        marker=dict(
            opacity=0.75,
            line=dict(width=2, color="white")),
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "City: %{customdata[1]}<br>"
            "Rating: %{y}<br>"
            "Cost for Two: ₹%{x}<br>"
            "Votes: %{customdata[2]}<br>"
            "<extra></extra>"),
        customdata=top10_df[["Restaurant Name","City","Votes"]].values)

# chart shown
    st.plotly_chart(fig5, use_container_width=True)




# Chart 6 — Funnel Chart for % total resurent accroding to the rating segments
with col6:
    funnel_df = filtered_df[filtered_df["Aggregate rating"] > 0] # only values avg ratintg greater than 0
    rating_order = ["Excellent","Very Good","Good","Average","Poor"] # categories based on the rating
    funnel_counts = funnel_df["Rating text"].value_counts() #counts the value based on the rating text
    funnel_data = pd.DataFrame({
        "Stage": [r for r in rating_order if r in funnel_counts.index], # takles rating text
        "Count": [funnel_counts[r] for r in rating_order if r in funnel_counts.index] # counts the value for the rating
    })

# the go figure used is set up with the values and css
    fig6 = go.Figure(go.Funnel(
        y=funnel_data["Stage"],
        x=funnel_data["Count"],
        textinfo="value+percent initial",
        textfont=dict(size=12, color="white"),
        marker=dict(
            color=["#1a9641","#a6d96a","#fdae61","#E23744","#d7191c"],
            line=dict(width=2, color="white")),
        connector=dict(
            line=dict(color="white", width=2))))

    fig6.update_layout(
        title="Restaurant Rating Funnel",
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=420,
        title_font=dict(size=15, color="#1a1a1a"),
        margin=dict(t=55, b=40, l=20, r=20),
        font=dict(family="Arial"))

    st.plotly_chart(fig6, use_container_width=True)

# again markdown for seprator
st.markdown("---")
st.markdown("###  Restaurant Distribution — India Map")

# fampous cities coordinates for the map
city_coords = {
    "New Delhi": [28.6139, 77.2090],
    "Gurgaon": [28.4595, 77.0266],
    "Noida": [28.5355, 77.3910],
    "Faridabad": [28.4089, 77.3178],
    "Ghaziabad": [28.6692, 77.4538],
    "Lucknow": [26.8467, 80.9462],
    "Guwahati": [26.1445, 91.7362],
    "Bhubaneshwar": [20.2961, 85.8245],
    "Amritsar": [31.6340, 74.8723],
    "Ahmedabad": [23.0225, 72.5714],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Hyderabad": [17.3850, 78.4867],
    "Kolkata": [22.5726, 88.3639],
    "Pune": [18.5204, 73.8567],
    "Jaipur": [26.9124, 75.7873],
    "Surat": [21.1702, 72.8311],
    "Indore": [22.7196, 75.8577],
    "Agra": [27.1767, 78.0081]
}

# counts the citites
city_counts = filtered_df["City"].value_counts().reset_index()

# city as well counts
city_counts.columns = ["City", "Count"]


# avg rating for the city with greater tha 0
city_avg_rating = filtered_df[filtered_df["Aggregate rating"] > 0].groupby(
    "City")["Aggregate rating"].mean().round(1).reset_index()

city_counts = city_counts.merge(city_avg_rating, on="City", how="left")

# latitude and longitude set up
city_counts["lat"] = city_counts["City"].map(
    lambda x: city_coords.get(x, [None, None])[0])

city_counts["lon"] = city_counts["City"].map(
    lambda x: city_coords.get(x, [None, None])[1])


city_counts = city_counts.dropna(subset=["lat", "lon"])

# chart shown
fig_map = go.Figure()

for _, row in city_counts.iterrows():
    size = max(20, min(70, row["Count"] / 70))
    rating = row["Aggregate rating"] if pd.notna(row["Aggregate rating"]) else 0

    if rating >= 4.0:
        color = "#E23744"
        opacity = 0.9
    elif rating >= 3.5:
        color = "#FF6B7A"
        opacity = 0.75
    else:
        color = "#FFAAB0"
        opacity = 0.6

    fig_map.add_trace(go.Scattermapbox(
        lat=[row["lat"]],
        lon=[row["lon"]],
        mode="markers",
        marker=dict(
            size=size,
            color=color,
            opacity=opacity),
        customdata=[row["City"]],
        hovertemplate=(
            f"<b style='font-size:14px'>{row['City']}</b><br>"
            f"─────────────────<br>"
            f"Restaurants: <b>{int(row['Count'])}</b><br>"
            f"Avg Rating: <b>{rating} ⭐</b><br>"
            "<extra></extra>"),
        showlegend=False))

    # City name label
    fig_map.add_trace(go.Scattermapbox(
        lat=[row["lat"] + 0.4],
        lon=[row["lon"]],
        mode="text",
        text=[row["City"]],
        textfont=dict(size=11, color="white"),
        hoverinfo="skip",
        showlegend=False))

# Legend traces
for label, color in [
    ("High Rating 4.0+", "#E23744"),
    ("Good Rating 3.5–4.0", "#FF6B7A"),
    ("Average below 3.5", "#FFAAB0")]:
    fig_map.add_trace(go.Scattermapbox(
        lat=[None], lon=[None],
        mode="markers",
        marker=dict(size=12, color=color),
        name=label,
        showlegend=True))

fig_map.update_layout(
    mapbox=dict(
        style="carto-darkmatter",
        center=dict(lat=22, lon=80),
        zoom=4.2),
    height=600,
    title=dict(
        text="City wise Restaurant Distribution",
        font=dict(size=15, color="#1a1a1a"),
        x=0, xanchor="left"),
    margin=dict(t=55, b=10, l=10, r=10),
    paper_bgcolor="white",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.02,
        xanchor="center",
        x=0.5,
        font=dict(size=11, color="white"),
        bgcolor="rgba(0,0,0,0.55)",
        bordercolor="rgba(255,255,255,0.15)",
        borderwidth=1),
    font=dict(family="Arial"))

selected_map = st.plotly_chart(fig_map,
    use_container_width=True,
    on_select="rerun",
    key="map_chart")

#  the segments is that our map must behave like the slicer
if selected_map and selected_map.get("selection", {}).get("points"):
    point = selected_map["selection"]["points"][0]
    clicked_city = point.get("customdata")
    if clicked_city and str(clicked_city).strip():
        st.session_state.map_city = str(clicked_city).strip()
        st.session_state.reset_count += 1
        st.rerun()


# again the seprator for the next section
st.markdown("---")
st.markdown("### Key Insights")

# section for the insights
st.markdown("""
<style>
.insight-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
    margin-bottom: 30px;
}
.insight-card {
    background: white;
    border-radius: 12px;
    padding: 20px 22px;
    border-left: 4px solid #E23744;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
}
.insight-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 16px rgba(226,55,68,0.12);
}
.insight-number {
    font-size: 11px;
    font-weight: 600;
    color: #E23744;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.insight-title {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 8px;
    line-height: 1.4;
}
.insight-body {
    font-size: 13px;
    color: #666;
    line-height: 1.6;
}
.insight-stat {
    display: inline-block;
    background: #fff0f1;
    color: #E23744;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-grid">
    <div class="insight-card">
        <div class="insight-number">Insight 01</div>
        <div class="insight-title">Delhi NCR Restaurants Struggle with Ratings</div>
        <div class="insight-body">Restaurants near New Delhi do not achieve an average rating above 4.0, suggesting high competition and inconsistent quality in the region.</div>
        <span class="insight-stat">Avg Rating below 4.0</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">Insight 02</div>
        <div class="insight-title">New Delhi Dominates Restaurant Count</div>
        <div class="insight-body">New Delhi has the highest number of restaurants across all Indian cities — making it the most competitive food market in India.</div>
        <span class="insight-stat">5,473 Restaurants</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">Insight 03</div>
        <div class="insight-title">Full Service Restaurants Are Rare</div>
        <div class="insight-body">Only 427 restaurants offer both table booking and online delivery — with an average rating of 3.6, showing full-service does not guarantee quality.</div>
        <span class="insight-stat">427 Restaurants · Avg 3.6</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">Insight 04</div>
        <div class="insight-title">Most Restaurants Offer No Convenience Features</div>
        <div class="insight-body">5,545 restaurants offer neither table booking nor online delivery — indicating a massive gap in digital adoption across India.</div>
        <span class="insight-stat">5,545 Restaurants</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">Insight 05</div>
        <div class="insight-title">North Indian is the Most Popular Cuisine</div>
        <div class="insight-body">North Indian cuisine leads with 936 restaurants but maintains only an average rating of 3.2 — popularity does not always align with satisfaction.</div>
        <span class="insight-stat">936 Restaurants · Avg 3.2</span>
    </div>
    <div class="insight-card">
        <div class="insight-number">Insight 06 — Funnel Chart</div>
        <div class="insight-title">Excellence is Extremely Rare in New Delhi</div>
        <div class="insight-body">The rating funnel reveals that 61.6% of New Delhi restaurants fall in the Average category while only 0.7% achieve Excellent status — a stark quality gap in India's largest food market.</div>
        <span class="insight-stat">61.6% Average · Only 0.7% Excellent</span>
    </div>
</div>
""", unsafe_allow_html=True)

# details of me
st.markdown("---")
st.markdown("""
<style>
.footer {
    background: #1a1a1a;
    border-radius: 12px;
    padding: 24px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 10px;
}
.footer-left {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.footer-name {
    color: white;
    font-size: 16px;
    font-weight: 500;
}
.footer-sub {
    color: #888;
    font-size: 12px;
}
.footer-links {
    display: flex;
    gap: 12px;
}
.footer-btn {
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 20px;
    padding: 8px 20px;
    font-size: 12px;
    text-decoration: none;
    border: 0.5px solid rgba(255,255,255,0.15);
    transition: background 0.2s;
}
.footer-btn:hover {
    background: #E23744;
    color: white;
}
.footer-right {
    color: #555;
    font-size: 11px;
    text-align: right;
}
</style>

<div class="footer">
    <div class="footer-left">
        <div class="footer-name">Dev Charaya</div>
        <div class="footer-sub">Data Analyst · Zomato India Dashboard</div>
    </div>
    <div class="footer-links">
        <a class="footer-btn" href="https://github.com/charayadev" target="_blank">GitHub</a>
        <a class="footer-btn" href="https://www.linkedin.com/in/dev-charaya-186b40314/" target="_blank">LinkedIn</a>
    </div>
    <div class="footer-right">
        Built with Streamlit & Plotly<br>
        Data Source: Zomato India
    </div>
</div>
""", unsafe_allow_html=True)