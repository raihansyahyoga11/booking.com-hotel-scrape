import asyncio
import aiohttp
import re
import pandas as pd

# Function to read URLs from a text file


def read_urls_from_file(filepath):
    with open(filepath, 'r') as file:
        return [line.strip() for line in file]

# Asynchronous function to fetch page content


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            # Directly extract the highlighted_blocks value from the URL
            highlighted_blocks_match = re.search(
                r"highlighted_blocks=(\d+)", url)
            highlighted_blocks = highlighted_blocks_match.group(
                1) if highlighted_blocks_match else None

            page_content = await response.text()
            hotel_name_matches = re.findall(
                r"hotel_name: '(.*?[^\\])\'", page_content)
            hotel_name = hotel_name_matches[0].replace(
                "\\'", "'") if hotel_name_matches else None

            hotel_id_matches = re.findall(r"hotel_id: '(\d+)'", page_content)
            hotel_id = hotel_id_matches[0] if hotel_id_matches else None
            if hotel_id == '0':  # Note the comparison to '0' not 0
                hotel_id = highlighted_blocks[:-
                                              2] if highlighted_blocks else None
            return {"URL": url, "Hotel Name": hotel_name, "Hotel ID": hotel_id, "Highlighted Blocks": highlighted_blocks}
        else:
            print(f"Failed to retrieve content from {url}")
            return {"URL": url, "Hotel Name": None, "Hotel ID": None, "Highlighted Blocks": None}

# Asynchronous function to scrape data


async def scrape_data(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Main process


async def main():
    file_path = 'urls.txt'  # Your file path here
    urls = read_urls_from_file(file_path)
    scraped_data = await scrape_data(urls)

    # Convert to DataFrame and export to Excel
    df = pd.DataFrame(scraped_data)
    df.index = df.index + 1
    df.to_excel('scraped_data.xlsx', index_label='No')
    print("Data exported to scraped_data.xlsx successfully.")

# Run the main process
if __name__ == '__main__':
    asyncio.run(main())
