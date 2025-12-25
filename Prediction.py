from copyreg import pickle

import pandas as pd
import streamlit as st
import pickle
teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open("pipe.pkl","rb"))
st.title("IPL Win Predictor")

team_options = ["Select Team"] + sorted(teams)

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox(
        "Batting Team",
        team_options,
        index=0
    )

with col2:
    bowling_team = st.selectbox(
        "Bowling Team",
        team_options,
        index=0
    )


selected_city = st.selectbox("Select host city",sorted(cities))

target = st.number_input(
    "Target",
    min_value=0,
    value=0,
    step=1
)


col3,col4,col5 = st.columns(3)

with col3 :
    score = st.number_input(
        "Score",
        min_value=0,
        value=0,
        step=1
    )

with col4 :
    overs = st.number_input(
        "Overs completed",
        min_value=0.0,
        value=0.0,
        step=0.1
    )

with col5 :
    wickets = st.number_input(
        "Wicket Left",
        min_value=0,
        max_value=10,
        value=0,
        step=1
    )

if batting_team == "Select Team" or bowling_team == "Select Team":
    st.warning("Please select both batting and bowling teams")
    st.stop()

if batting_team == bowling_team:
    st.warning("Batting and Bowling teams cannot be the same")
    st.stop()

whole_overs = int(overs)
balls = int(round((overs - whole_overs) * 10))

if balls >= 6:
    whole_overs += 1
    balls = 0



if st.button("Predict Probability"):

    runs_left = target - score

    balls_bowled = whole_overs * 6 + balls
    balls_left = 120 - balls_bowled

    wickets_left = 10 - wickets

    crr = score / balls_bowled if balls_bowled > 0 else 0
    rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

    input_df = pd.DataFrame({
        "batting_team": [batting_team],
        "bowling_team": [bowling_team],
        "city": [selected_city],
        "runs_left": [runs_left],
        "Ball_left": [balls_left],     # ✅ fixed
        "wickets": [wickets_left],
        "total_runs_x": [target],
        "crr": [crr],
        "rrr": [rrr]
    })

    st.table(input_df)

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    st.header(f"{batting_team}: {round(win*100)}%")
    st.header(f"{bowling_team}: {round(loss*100)}%")
