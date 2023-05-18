import requests
from selenium import webdriver


def ig_download(reel_url, doc_type):
    driver = webdriver.Chrome('C:\penguin\chromedriver_win32')
    # Navigate to the website
    driver.get(reel_url)
    # Locate the video element
    div = driver.find_elements(By.CSS_SELECTOR, 'div.x1i10hfl')
    driver.switch_to.frame(div)
    video = driver.find_elements(By.CSS_SELECTOR, 'video')
    # Extract the source URL of the video
    video_src = video.get_attribute('src')
    print(video_src)

    # Clean up and quit the WebDriver
    driver.quit()
