import os
import requests
from urllib.parse import urlparse, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_filename_from_url(url):
    """Extract filename from the given URL."""
    a = urlparse(url)
    return os.path.basename(unquote(a.path))

def download_file(url, base_path):
    """Download a file from a given URL to a specified path, with retry logic and existing file check."""
    filename = get_filename_from_url(url)
    file_path = os.path.join(base_path, filename)
    
    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"Skipped, already exist: {filename}")
        return 'skipped'  # Return 'skipped' if file exists
    
    attempts = 2  # Set number of attempts
    for _ in range(attempts):
        print(f"{bcolors.OKBLUE}Downloading: {filename}{bcolors.ENDC}")
        try:
            response = requests.get(url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"{bcolors.OKGREEN}Download Success: {filename}{bcolors.ENDC}")
                return 'downloaded'
            else:
                print(f"Retry Download {filename}")
        except Exception as e:
            print(f"Retry Download {filename}: {str(e)}")
    print(f"{bcolors.FAIL}Download Failed: {filename}{bcolors.ENDC}")
    return False

def download_files(urls, path):
    """Download multiple files into a specified subdirectory under 'downloads', ensuring the directory exists."""
    base_path = os.path.join('downloads', path)
    # Ensure the base_path directory exists
    if not os.path.exists(base_path):
        os.makedirs(base_path)

    failed_urls = []
    skipped_urls = []
    success_count = 0
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_url = {executor.submit(download_file, url, base_path): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if result == 'downloaded':
                success_count += 1
            elif result == 'skipped':
                skipped_urls.append(future_to_url[future])
            else:
                failed_urls.append(future_to_url[future])

    # Log failed downloads and skipped files
    with open(os.path.join(base_path, 'log.txt'), 'w') as log_file:
        if failed_urls:
            log_file.write("Failed URLs:\n")
            for url in failed_urls:
                log_file.write(f"{url}\n")
        if skipped_urls:
            log_file.write("Skipped URLs:\n")
            for url in skipped_urls:
                log_file.write(f"{url}\n")

    print(f"Download complete: Total: {len(urls)}, Success: {success_count}, Skipped: {len(skipped_urls)}, Failed: {len(failed_urls)}")
    return success_count, skipped_urls, failed_urls
