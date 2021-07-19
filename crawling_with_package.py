# kewords = ["칠성사이다,생수병,손소독제,볼펜,마우스,테이크아웃 커피잔", "잼,와인잔,유리", "카스,참치캔,스위트콘", "신문지,책,과자 박스,색종이", "뽁뽁이,검은비닐,비닐"]
# kewords = [
#     "칠성사이다",
#     "생수병",
#     "손소독제",
#     "볼펜",
#     "마우스",
#     "테이크아웃 커피잔",
#     "잼",
#     "와인잔",
#     "유리",
#     "카스",
#     "참치캔",
#     "스위트콘",
#     "신문지",
#     "책",
#     "과자 박스",
#     "색종이",
#     "뽁뽁이",
#     "검은비닐",
#     "비닐",
# ]

kewords = ["치킨박스", "피자박스", "음료수캔"]

# * Google, 360 ~ 380개가 최대로 보임.
# from google_images_download import google_images_download
# from urllib.parse import quote_plus

# response = google_images_download.googleimagesdownload()

# # creating list of arguments
# for keword in kewords:
#     arguments = {
#         "keywords": quote_plus(keword),
#         "limit": 1000,
#         "print_urls": True,
#         "chromedriver": "C:/Github Projects/2021-Software-Contest/chromedriver",
#     }

#     paths = response.download(arguments)
#     print(paths)


# * Bing, 정말 2000개의 이미지가 검색되는지는 모르겠지만, 중복으로 갯수를 채우는 듯하므로 최대 500개 정도로 제한할 것.
# import os
# from bing_image_downloader import downloader

# # query_string : String to be searched.
# # limit : (optional, default is 100) Number of images to download.
# # output_dir : (optional, default is 'dataset') Name of output dir.
# # adult_filter_off : (optional, default is True) Enable of disable adult filteration.
# # force_replace : (optional, default is False) Delete folder if present and start a fresh download.
# # timeout : (optional, default is 60) timeout for connection in seconds.
# # verbose : (optional, default is True) Enable downloaded message.


# for query_string in kewords:
#     limit = 2000 - len(os.listdir("./downloads/" + query_string))
#     downloader.download(query_string, limit=limit, output_dir="downloads")
