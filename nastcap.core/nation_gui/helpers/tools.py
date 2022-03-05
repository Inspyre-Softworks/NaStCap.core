import requests
from pathlib import Path


def download_image(url, fp):
    data = requests.get(url).content
    
    file_name = url.split('/')[-1]
    
    fp = Path(fp)
    
    image_path = fp.joinpath(file_name)
    
    with open(image_path, 'wb') as f:
        f.write(data)
    
    return image_path


def get_nation_win_colors(img_path=None, img_url=None, ):
    if img_path is None and img_url is None:
        raise ValueError("You must provide a value for either 'img_path' or 'img_url")
    
    if img_url is not None:
        img_path = download_image(img_url)
        
    
