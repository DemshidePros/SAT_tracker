import json
import os
import pandas as pd
from datetime import date



def save_data(data, filename = 'data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
        
        
def load_data(filename = 'data.json'):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return json.load(f)
    
def add_info(attempts, topic, subtopic, correct):   
    date_current = date.today()

    topic, subtopic = topic.lower(), subtopic.lower()
    
    attempts.append({
        "topic": topic,
        "subtopic": subtopic,
        "correct": correct,
        "date": str(date_current)
    }) 
    return attempts
    

def create_stats(stats, attempts):
    for items in attempts:
        topic = items["topic"]
        if stats.get(topic) is None:
            stats[topic] = {"total": 0, "correct": 0}

        stats[topic]["total"] += 1
        if items["correct"] is True:
            stats[topic]["correct"] += 1
    
    for topic in stats:
        stats[topic]['percentage'] = round(stats[topic]['correct']/stats[topic]['total']*100)


    return stats


def sort_stats_percentage(stats):
    stats_sorted = sorted(stats, key=lambda topic: stats[topic]["percentage"])
    return stats_sorted


def get_daily_stats(attempts, selected_topic):
    if not attempts:
        return pd.DataFrame()
        
    df = pd.DataFrame(attempts)
    
    df_filtered = df[df['topic'] == selected_topic]
    
    if df_filtered.empty:
        return pd.DataFrame()
    
    daily_grouped = df_filtered.groupby('date')['correct'].agg(
        lambda x: round((x.sum() / x.count()) * 100, 2)
    ).to_frame(name='Success Rate (%)')
    
    
    daily_grouped = daily_grouped.sort_index()
    
    return daily_grouped