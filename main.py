from downloader import download_files
from urllib.parse import urlparse
from scrapper.wikipedia import wiki

def domain_check(domain):
    if 'wikipedia.org' in domain:
        return 'wikipedia'
    elif 'google.' in domain:
        return 'google'
    else:
        return 'other'

def main():
    while True:
        url = input("Please enter a URL: ")
        if url == "":
            url = "https://en.wikipedia.org/wiki/London"
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()

        domain_type = domain_check(domain)
        
        if domain_type == 'wikipedia':
            images, clean_title = wiki(url)
            download_files(images, clean_title)
        else:
            print('Domain is not supported!')
            return
        
        repeat = input("Do you want to rerun? (y/n): ").strip().lower()
        if repeat != 'y':
            break

if __name__ == "__main__":
    main()
