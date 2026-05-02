import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

for page in range(1, 4):
    url = f"https://quotes.toscrape.com/page/{page}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    for q in quotes:
        name = q.find('small').text
        text = q.find('span', class_='text').text

        data.append({
            "Name": name,
            "Info": text,
            "Location": "Unknown"
        })

# ✅ Step 1: Create DataFrame
df = pd.DataFrame(data)

# ✅ Step 2: Clean data
df.drop_duplicates(inplace=True)
df.fillna("Not Available", inplace=True)

# ✅ Step 3: Generate Email
def generate_email(name):
    name = name.lower().replace(" ", "")
    return f"{name}@company.com"

df["Email"] = df["Name"].apply(generate_email)

# ⭐ Step 4: ADD YOUR NEW LINES HERE
df.rename(columns={
    "Name": "Full Name",
    "Info": "Description"
}, inplace=True)

df = df.sort_values(by="Full Name")

# ✅ Step 5: Save to Excel
df.to_excel("leads.xlsx", index=False)

print("✅ Leads generated and saved to leads.xlsx")