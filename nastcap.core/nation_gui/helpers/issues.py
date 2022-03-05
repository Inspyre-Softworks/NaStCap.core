import os
import requests
from pathlib import Path
from PIL import Image
from nation_gui.helpers.tools import download_image



URL_STUB = 'https://www.nationstates.net/images/newspaper/'

IMAGES_FP = Path('~/tmp/Inspyre-Softworks/nation-gui/').expanduser()


class ActiveIssues(object):
    def __init__(self, nation_obj):
        """
        
        A class that will handle a nation's active issues.
        
        Args:
            nation_obj (Nation):
                The Nation object which contains the issues (Nation().issues).
        """
        self.nation = nation_obj


class IssueImages(object):
    
    def __init__(self, nation_obj, images_fp=IMAGES_FP):
        
        self.nation_name = nation_obj.name
        
        self.issues = nation_obj.issues
        
        self.images_fp = Path(images_fp).expanduser().resolve()
        
        self.maintain_tmp()
        
        if len(self.issues) != 0:
            self.image_urls = self.collect_image_urls()
            self.jpg_paths = self.collect_images()
    
    def maintain_tmp(self):
        if not self.images_fp.exists():
            os.makedirs(self.images_fp)
        
        for issue in self.issues:
            issue_path = self.images_fp.joinpath(issue.id)
            os.makedirs(issue_path)
        
        # TODO:
        #   - Check here for the need to prune/compress any issue archives.
    
    def collect_image_urls(self):
        urls = []
        suffix = '-1.jpg'
        for issue in self.issues:
            url = URL_STUB + issue.pic1 + suffix
            urls.append(url)
        
        return urls
    
    def collect_images(self, image_urls=None):
        if image_urls is None:
            image_urls = self.image_urls
            
        downloaded_paths = [download_image(url, self.images_fp) for url in image_urls]
        return None if not downloaded_paths else downloaded_paths
    
    @staticmethod
    def convert_images(path_list, base_out_path=None):
        new_paths = []
        for path in path_list:
            p_str = str(path)
            img = Image.open(path)
            img_name = p_str.split('/')[-1].split('.')[0]
            
            out_path = path.parent.joinpath(img_name + '.png') if base_out_path is None else base_out_path
            
            img.save(out_path)
            
            new_paths.append(out_path)
        
        return new_paths
