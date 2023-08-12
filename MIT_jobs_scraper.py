from bs4 import BeautifulSoup 
from requests import get as rget
from pandas import DataFrame, to_datetime, Timestamp, Series, concat

res = rget("https://mitec-club.org/job-openings").text
soup = BeautifulSoup(res, "html.parser")
today = Timestamp.now().date().strftime('%Y-%m-%d')

application_links = [atag['href'] for atag in soup.findAll("a")[43:-7]] # All applications links
jobs_df = DataFrame(columns = ["Company", "Position", "Deadline", "Apply link", "Keywords"])

all_para = soup.findAll("p", style="white-space:pre-wrap;")

# Take all the paras and remove the space.
all_para = [i.text for i in all_para[2:] if i.text != ""] # All paragraph tags
companies = all_para[::4] 
positions = all_para[1::4]
deadlines = all_para[2::4]	
keywords = all_para[3::4]

print(f"Companies: {len(companies)}, Positions: {len(positions)}, Deadlines: {len(deadlines)}, \
Links: {len(application_links)}, Keywords: {len(keywords)}") # Sanity check

# Filter application by deadlines
for i in range(len(deadlines)):
	temp = deadlines[i].split(":")[1][1:] # Text of each deadline
	if temp == "No Deadline": # Only considering if there is no deadline
		jobs_df = concat([jobs_df, DataFrame({"Company":[companies[i]], "Position": [positions[i]], "Deadline": [temp],
			"Apply link": [application_links[i]], "Keywords": ["".join(keywords[i].split(":")[1:])[1:]]})], ignore_index=True)
	elif (temp == "-") or (to_datetime(temp).date().strftime('%Y-%m-%d') < today): # Skip if the deadline is empty or passed
		continue
	else: # Any other conditions for future
		jobs_df = concat([jobs_df, DataFrame({"Company":[companies[i]], "Position": [positions[i]], "Deadline": [temp],
			"Apply link": [application_links[i]], "Keywords": ["".join(keywords[i].split(":")[1:])[1:]]})], ignore_index=True)
		
jobs_df.to_csv("MIT jobs.csv", index=False) # Saving the scraped data