import os
import requests
from bs4 import BeautifulSoup

def get_video_urls(page_url):
    try:
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        video_urls = []

        # 查找 a 标签
        for link  in soup.find_all('a') :
            href = link.get('href')
            video_urls.append(page_url+href)
        return video_urls
    except Exception as e:
        print(f"Error fetching video URLs from {page_url}: {e}")
        return []




def download_segmented_video(segment_urls, output_path):
    try:
        # 创建输出目录（如果不存在）
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 逐个下载分段视频
        with open(output_path, 'wb') as f_out:
            for segment_url in segment_urls:
                response = requests.get(segment_url, stream=True)
                response.raise_for_status()  # 如果请求失败，抛出异常
                
                # 逐个写入分段视频数据
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # 过滤掉空的chunk
                        f_out.write(chunk)
        
        print(f"Downloaded segmented video to: {output_path}")
    except Exception as e:
        print(f"Error downloading segmented video: {e}")


