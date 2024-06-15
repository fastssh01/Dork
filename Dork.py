import os
import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_shoe_urls(dork):
    urls = []

    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    auth = requests.auth.HTTPProxyAuth(*proxy_auth.split(':'))

    google_search_url = f"http://www.google.com/search?q={dork}&num=100"
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36'} 

    try:
        response = requests.get(google_search_url, proxies=proxies, auth=auth, headers=headers, timeout=15)
        status_code = response.status_code

        if status_code != 200:
            print(f"Error fetching URLs. Status Code: {status_code}")
            return urls

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            if href and href.startswith('/url?q=') and not 'webcache' in href:
                actual_url = href.split('?q=')[1].split('&sa=U')[0]
                if 'google.com' not in actual_url and not actual_url.startswith('/search'):
                    urls.append(actual_url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URLs: {str(e)}")

    return urls

# Example dork input (replace with your dork logic)
input_dork = input("Enter dork (e.g., inurl:shoes): ")

if not input_dork.strip():
    print("Dork cannot be empty. Exiting.")
    sys.exit()

# Generate shoe URLs based on the dork
shoe_urls = generate_shoe_urls(input_dork)

# Print or use shoe_urls as needed
print("Generated Shoe URLs:")
for url in shoe_urls:
    print(url)

def configure_proxy(proxy_file):
    if not os.path.exists(proxy_file):
        clear_screen()
        input_proxy = input("Proxy (IP:PORT): ").strip()
        if ':' not in input_proxy:
            print("Invalid input format. Please follow the format")
            time.sleep(1.75)
            return configure_proxy(proxy_file)
        if input_proxy:
            input_proxy_auth = input("Proxy (USER:PASS): ").strip()
            if ':' not in input_proxy_auth:
                print("Invalid input format. Please follow the format")
                time.sleep(1.75)
                return configure_proxy(proxy_file)
            if input_proxy_auth:
                with open(proxy_file, 'w') as f:
                    f.write(input_proxy + '\n' + input_proxy_auth)
            else:
                print("Proxy USER:PASS cannot be empty. Please provide valid credentials.")
                time.sleep(1.75)
                return configure_proxy(proxy_file)
        else:
            print("Proxy IP:PORT cannot be empty. Please provide a valid proxy.")
            time.sleep(1.75)
            return configure_proxy(proxy_file)

configure_proxy(proxy_file)


if not os.path.exists(bot_telegram_file):
    clear_screen()
    input_bot_id = ""
    input_chat_id = ""
    print("Telegram bot to notify you if the code is Done this is (Optional)")
    input_bot_id = input("Bot Token: ").strip()
    if input_bot_id:
        input_chat_id = input("Chat ID: ").strip()
    with open(bot_telegram_file, 'w') as f:
        f.write(input_bot_id + '\n' + input_chat_id)


if os.path.isfile(bot_telegram_file) and os.path.getsize(bot_telegram_file) > 0:
    with open(bot_telegram_file, 'r') as f:
        lines = f.readlines()
        if len(lines) == 2:
            bot_id  = lines[0].strip()
            chat_id = lines[1].strip()


with open(proxy_file, 'r') as f:
    lines = f.readlines()
    if len(lines) == 2:
        proxy = lines[0].strip()
        proxy_auth = lines[1].strip()
    else:
        os.remove(proxy_file)
        rerun()

with open(dork_file, 'r') as file:
    dork = file.read()
    if not dork:
        os.remove(dork_file)
        rerun()


if not os.path.exists(word_file):
    clear_screen()
    response = input("Wordlist is empty. Create new? Type Y to continue: ")
    if response.lower() == 'y':
        if os.path.exists(main_wordlist):
            shutil.copy(main_wordlist, word_file)
            print("File copied successfully.")
        else:
            print("Source word file not found.")
            time.sleep(1)
            rerun()
    else:
        print("Source word file not found.")
        time.sleep(1)
        rerun()



def get_links(value):
    global dork
    global proxy
    global proxy_auth
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
            return f"Error Code: {status_code}"
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
            total_urls = len(urls)
            with open(output_file, "a") as input_to:
                for url in urls:
                    input_to.write(url + "\n")
            return((f"Total: {total_urls}"))
        else:
            return((f"Total: 0"))
    except requests.exceptions.RequestException as e:
        return ""


def read_urls_from_file(word_file):
    with open(word_file, 'r') as file:
        urls = [line.strip() for line in file.readlines()]
    return urls

def save_line_number(line_number):
    with open(counter_file, 'w') as file:
        file.write(str(line_number))

def save_err_link(url):
    with open(error_file, 'a') as file:
        file.write(url + '\n')

def process_url(url, line_number):
    global counter
    counter += 1
    if counter % 100 == 0:
        clear_screen()
    if url.strip():
        output = get_links(url)
        if output:
            print(f"{line_number} {url} {output}")
            save_line_number(line_number)
            return line_number
        else:
            save_err_link(url)
            print(f"{line_number} Empty output for: {url}")
    else:
        print(f"{line_number} Empty")


def start_processing():
    global counter
    start_line = 1
    if os.path.exists(counter_file):
        with open(counter_file, 'r') as file:
            start_line = int(file.read().strip())
    urls_list = read_urls_from_file(word_file)[start_line - 1:]

    batch_size = 50
    for i in range(0, len(urls_list), batch_size):
        batch_urls = urls_list[i:i + batch_size]
        start_time = time.time() 
        all_results = []
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            results = executor.map(process_url, batch_urls, range(start_line + i, start_line + i + len(batch_urls)))
        for result in results:
            all_results.append(result)
        if None not in all_results:
            largest_number = max(all_results)
            with open(backup_file, 'w') as f:
               f.write(str(largest_number))
        processing_time = time.time() - start_time
        if len(all_results) == batch_size and processing_time < 4:
            clear_screen()
            print("Processing too fast, potential errors.")
            response = input(f"Proxy might have a problem.\nRewrite Proxy? Type Y to continue:").strip()
            if response.lower() == 'y':
                remove_file(proxy_file)
                clear_screen()
                configure_proxy(proxy_file)
                rerun()
        remove_duplicate_lines(output_file)
        counter += batch_size
        clear_screen()

clear_screen()
start_processing()

remove_duplicate_lines(error_file)


remove_file(word_file)
remove_file(counter_file)
remove_file(backup_file)


if os.path.exists(error_file) and os.path.getsize(error_file) > 0:
    os.rename(error_file, word_file) if os.path.exists(error_file) else None
    with open(word_file, 'r') as f:
        lines = f.readlines()
        if len(lines) > 3:
           rerun()

print("All Done")
remove_file(dork_file)
remove_file(word_file)

if globals().get('bot_id', '') != "" and chat_id != "":
    response = requests.get(f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text=GoogleSearch completed successfully")
