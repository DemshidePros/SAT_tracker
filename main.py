from logic import save_data, load_data, add_info, create_stats, sort_stats_percentage

attempts = load_data()
stats = {}

#new attempt input
while True:
    topic = input("Enter topic: ")
    subtopic = input("Enter subtopic: ")
    correct = input("Was the answer correct? (y/n): ").lower() == "y"    


    attempts = add_info(attempts, topic, subtopic, correct)
    
    cont = input("Do you want to add another attempt? (y/n): ").lower()
    if cont != "y":
        break

stats = create_stats(stats, attempts)
stats_sorted = sort_stats_percentage(stats)
save_data(attempts)

# print attempts
for items in attempts:
    print(f"{items['topic']} - {items['subtopic']} - {items['correct']} - {items['date']}")

#print stats
for topic in stats_sorted:  # topic is a string key
    print(f"{topic} - {stats[topic]['percentage']}%")
