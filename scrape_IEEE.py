from selenium import webdriver

try:
    driver = webdriver.Chrome()
    search_bar_xpath=""
    driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")

except:
    print("ERROR")
finally:
    driver.quit()
