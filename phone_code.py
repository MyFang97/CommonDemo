from selenium import webdriver
import time

def main():
    b = webdriver.Chrome()
    b.get('https://810.workarea2.live/view_video.php?viewkey=8714edb9125ad18fbde2&page=&viewtype=&category=')
    # time.sleep(5)
    # b.quit()

if __name__ == '__main__':
    main()
