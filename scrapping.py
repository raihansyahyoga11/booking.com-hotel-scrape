import requests
import re
import pandas as pd

# Function to read URLs from a text file


def read_urls_from_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

# Function to scrape data


def scrape_data(urls):
    data = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            page_content = response.text
            hotel_id_matches = re.findall(r"hotel_id: '(\d+)'", page_content)

            # Assuming you want the first match or None if not found
            hotel_id = hotel_id_matches[0] if hotel_id_matches else None

            data.append(
                {"URL": url, "Hotel ID": hotel_id})
        else:
            print(f"Failed to retrieve content from {url}")
    return data


# Main process
file_path = 'urls.txt'  # Your file path here
urls = read_urls_from_file(file_path)
scraped_data = scrape_data(urls)

# Convert to DataFrame and export to Excel
df = pd.DataFrame(scraped_data)
df.to_excel('scraped_data.xlsx', index=False)

print("Data exported to scraped_data.xlsx successfully.")
