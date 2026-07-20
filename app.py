import streamlit as st
import pandas as pd
from logic import save_data, load_data, add_info, create_stats, sort_stats_percentage, get_daily_stats


attempts = load_data()
stats = {}

st.title(f"SAT Tracker")

# add new attempt form
st.header(f"Add a new attempt:")
with st.form(key='attempt_form', clear_on_submit=True):
    topic = st.text_input("Enter topic:")
    subtopic = st.text_input("Enter subtopic:")
    correct = st.checkbox("Was the answer correct?")
    
    submit_button = st.form_submit_button(label='Add Attempt')

if submit_button:
    attempts = add_info(attempts, topic, subtopic, correct)
    save_data(attempts)
    

stats = create_stats(stats, attempts)
stats_sorted = sort_stats_percentage(stats)

# creating tabs for attempts and stats
tab_attempts, tab_stats, tab_analytics = st.tabs(['attempts', 'stats', 'analytics'])

#attempts output in a tab/table
with tab_attempts:    
    st.header(f"Your attempts:")
    st.dataframe(attempts, use_container_width=True)


#stats output in a tab/table
with tab_stats:
    st.header(f"Your attempts' stats:")
    new_stat = [{"topic": topic, "total": stats[topic]["total"], "correct": stats[topic]["correct"], "percentage": stats[topic]["percentage"]} for topic in stats_sorted]
    st.dataframe(new_stat, use_container_width=True)


#only god understand what is happening here, but it works    
with tab_analytics:
    st.header('Your analytics:')
    
    unique_topics = list(set([item['topic'] for item in attempts]))
    
    if unique_topics:
        selected_topic = st.selectbox('Select a topic to analyze:', unique_topics)
        
        df_chart = get_daily_stats(attempts, selected_topic)
        
        if not df_chart.empty:
            import altair as alt
            
            df_reset = df_chart.reset_index()
            df_reset['date'] = pd.to_datetime(df_reset['date']).dt.strftime('%Y-%m-%d').astype(str)
            
            chart = alt.Chart(df_reset).mark_line(
                point=True,
                strokeWidth=3
            ).encode(
                x=alt.X('date:N', title='Date', sort=None),
                y=alt.Y('Success Rate (%):Q', scale=alt.Scale(domain=[0, 100]), title='Success Rate (%)')
            ).properties(
                height=350
            )
            
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(df_chart, width='stretch')
        else:
            st.info("No data available for this topic yet.")
        
    else:
        st.info("Do your homework first! You have no attempts yet.")