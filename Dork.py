# GOOGLE SEARCHER
# CREATED BY HASHIEEEEE
# NOT FOR SALE
# https://t.me/hashshinrinyoku
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import shutil
import sys
import time

output_file = "output.txt"
error_file = "error.txt"
dork_file = "dork.txt"
proxy_file = "proxy.txt"
bot_telegram_file = "bot_telegram.txt"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

clear_screen()

def get_links(value):
    with open(dork_file, 'r') as file:
        dork = file.read().strip()

    with open(proxy_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 2:
            proxy = lines[0].strip()
            proxy_auth = lines[1].strip()
        else:
            return ""

    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    auth = requests.auth.HTTPProxyAuth(*proxy_auth.split(':'))
    query = f"{dork} {value}"
    google_search_url = f"http://www.google.com/search?q={query}&num=100"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36'} 

    try:
        response = requests.get(google_search_url, proxies=proxies, auth=auth, timeout=15)
        status_code = response.status_code

        if status_code != 200:
            with open(error_file, "a") as input_to:
                input_to.write(value + "\n")
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        urls = []
        for link in links:
            href = link.get('href')
            if href and href.startswith('/url?q=') and not 'webcache' in href:
                actual_url = href.split('?q=')[1].split('&sa=U')[0]
                if 'google.com' not in actual_url and not actual_url.startswith('/search'):
                    urls.append(actual_url)
        
        if urls:
            with open(output_file, "a") as output:
                for url in urls:
                    output.write(url + "\n")
    except requests.exceptions.RequestException as e:
        return ""

def read_urls_from_file(word_file):
    # Stub function, as we are not using a wordlist
    return []

def process_url(url, line_number):
    get_links(url)

def start_processing():
    urls_list = read_urls_from_file("data/word.txt")

    batch_size = 50
    for i in range(0, len(urls_list), batch_size):
        batch_urls = urls_list[i:i + batch_size]
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            executor.map(process_url, batch_urls, range(i + 1, i + 1 + len(batch_urls)))

start_processing()

remove_file(output_file)
remove_file(error_file)

if os.path.exists(error_file) and os.path.getsize(error_file) > 0:
    os.rename(error_file, "data/word.txt") if os.path.exists(error_file) else None

print("All Done")
remove_file(dork_file)
remove_file("data/word.txt")
remove_file(proxy_file)

if os.path.isfile(bot_telegram_file) and os.path.getsize(bot_telegram_file) > 0:
    with open(bot_telegram_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 2:
            bot_id  = lines[0].strip()
            chat_id = lines[1].strip()

            if bot_id != "" and chat_id != "":
                requests.get(f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text=GoogleSearch completed successfully")
                
