# news_verifier/utils.py
import requests
from bs4 import BeautifulSoup

def fetch_news():
    url = 'https://www.indiatoday.in/'  # Example URL (Make sure this is a news website you can legally scrape)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for item in soup.select('.news-item'):  # Adjust selector based on the actual website
        title = item.select_one('.news-title').get_text(strip=True)
        summary = item.select_one('.news-summary').get_text(strip=True)
        link = item.select_one('a')['href']
        image_url = item.select_one('img')['src'] if item.select_one('img') else 'https://via.placeholder.com/150'

        articles.append({
            'title': title,
            'summary': summary,
            'url': link,
            'image_url': image_url,
        })

    return articles

# import requests
# from bs4 import BeautifulSoup

# def verify_news(news_query):
#     """
#     Verifies a news article or headline by performing a Google search.
#     """
#     search_url = f"https://www.google.com/search?q={news_query.replace(' ', '+')}"
#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
#     }

#     response = requests.get(search_url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Find all the snippets and titles in the search results
#     results = [g.get_text() for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')]

#     # Simple logic to determine if the news is real or fake based on search results
#     if any(
#         keyword in result.lower()
#         for keyword in ["verified", "reliable", "fact-check", "news", "source"]
#         for result in results
#     ):
#         verdict = "Real"
#     else:
#         verdict = "Fake"

#     return verdict, results



# utils.py

# import requests
# from bs4 import BeautifulSoup
# import tinys3
# from PIL import Image
# import io
# import json

# # Function to perform reverse image search using TinEye API
# def reverse_image_search(image_path):
#     # This is a mock function. Replace it with actual API integration.
#     tineye_url = "https://api.tineye.com/rest/search/"
#     # Use API key and image search parameters
#     # response = requests.post(tineye_url, files={'image': open(image_path, 'rb')})
#     # return response.json()

#     # Mock result
#     return {"matches": [{"url": "https://example.com/matched_image"}]}

# # Function to verify video using InVID API
# def verify_video(video_path):
#     # This is a mock function. Replace it with actual API integration.
#     invid_url = "https://www.invid-project.eu/tools-and-services/invid-verification/"
#     # Use API key and video search parameters
#     # response = requests.post(invid_url, files={'video': open(video_path, 'rb')})
#     # return response.json()

#     # Mock result
#     return {"verdict": "Verified"}

# # Function to perform metadata analysis
# def analyze_metadata(image_or_video_path):
#     # Use exiftool or ffmpeg to extract metadata
#     # For simplicity, let's assume it's an image
#     image = Image.open(image_or_video_path)
#     return image._getexif()

# # Function to verify news by combining all methods
# def verify_news(news_query, image_path=None, video_path=None):
#     results = []
#     image_results = reverse_image_search(image_path) if image_path else None
#     video_verdict = verify_video(video_path) if video_path else None
#     metadata = analyze_metadata(image_path or video_path) if (image_path or video_path) else None
    
#     # Perform Google search as before
#     search_url = f"https://www.google.com/search?q={news_query.replace(' ', '+')}"
#     headers = {"User-Agent": "Mozilla/5.0"}
#     response = requests.get(search_url, headers=headers)
#     soup = BeautifulSoup(response.text, 'html.parser')
#     results = [g.get_text() for g in soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')]

#     # Combine all verification sources to determine the final verdict
#     if any(keyword in result.lower() for keyword in ["verified", "reliable"] for result in results):
#         verdict = "Real"
#     elif image_results or video_verdict:
#         verdict = "Real" if (image_results or video_verdict.get("verdict") == "Verified") else "Fake"
#     else:
#         verdict = "Fake"
    
#     return verdict, results, image_results, video_verdict, metadata
