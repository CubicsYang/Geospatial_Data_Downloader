import os
import requests

def download_file(url, output_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded file to {output_path}")
        else:
            print(f"Failed to download file, status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Failed to download file: {e}")
        
        
# download files
def download_files(urls, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for url in urls:
        filename = url.split('/')[-1]
        output_path = os.path.join(output_dir, filename)
        download_file(url, output_path)