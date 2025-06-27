import urllib3
from bs4 import BeautifulSoup
import requests
import re

def frequency_map():    
    freq_map = dict()
    number = int(input("Enter a number: "))
    while number > 0:
        digit = number % 10
        if digit in freq_map:
            freq_map[digit] += 1
        else:
            freq_map[digit] = 1
        number //= 10
    
    return freq_map
    
def staircase(n):
    step = 1
    stair = list()
    while len(n)> 0:
        if len(n) < step:
            raise ValueError("Not enough elements in the list")
        else:
            helper = list()
            for i in range(step):
                helper.append(n.pop())
            stair.append(helper)
            step += 1
            
    return stair


def secretMessageDecoder(url):
    # Accessing the Google Docs document
    request = urllib3.request('GET', url)
    data = request.data
    html = data.decode('utf-8')
    parser = BeautifulSoup(html, 'html.parser')
    
    # Extracting the coordinates and their respective characters from the document
    coordinates = dict()
    max_x = max_y = 0
    tables = parser.find_all('table')
    
    # If no tables are found, print a message and return
    if len(tables) == 0:
        print("No tables found in the document.")
        return
    
    # If more than one table is found, print a message and return
    else:
        for tr in tables[0].find_all('tr'):
            cell_values = tr.find_all('span')
            if 'x-coordinate' not in cell_values[0].text:
                # Getting the max x and y coordinates
                max_x = max(max_x, int(cell_values[0].text))
                max_y = max(max_y, int(cell_values[2].text))
                
                # Extracting the x-coordinate, character, and y-coordinate
                if coordinates.get(int(cell_values[2].text)) is None:
                    coordinates[int(cell_values[2].text)] = {int(cell_values[0].text): cell_values[1].text}
                else:
                    coordinates[int(cell_values[2].text)][int(cell_values[0].text)] = cell_values[1].text
        
        # Printing the charcaters in from higher y to lower y
        for y in range(max_y, -1, -1):
            row = ''
            for x in range(max_x + 1):
                if coordinates.get(y) is not None and coordinates[y].get(x) is not None:
                    row += coordinates[y][x]
                else:
                    row += ' '
            print(row)
        
    
    

secretMessageDecoder('https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub')
def draw_from_google_doc_table_format(url):
    # Convert Google Doc to plain text export URL
    if "docs.google.com/document/d/" in url:
        doc_id = url.split("/d/")[1].split("/")[0]
        url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.strip().splitlines()

    grid_data = {}
    max_x = max_y = 0

    # Skip header row and process the table
    for line in lines[1:]:  # Skip the header line
        # Use regex to extract columns
        match = re.match(r"\s*(\d+)\s+(\S+)\s+(\d+)", line)
        if match:
            x = int(match.group(1))
            char = match.group(2)
            y = int(match.group(3))

            grid_data[(x, y)] = char
            max_x = max(max_x, x)
            max_y = max(max_y, y)

    # Render the grid
    for y in range(max_y - 1, 0, -1):
        print(y)
        row = ''
        for x in range(max_x + 1):
            row += grid_data.get((x, y), ' ')
        print(row)
        
# draw_from_google_doc_table_format("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")