from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import json



def extract_article_details(article_link):
    driver = webdriver.Chrome()
    driver.get(article_link)

    # try:
    #     accept_button_xpath = '/html/body/div[1]/div[2]/div[2]/button[2]'
    #     WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, accept_button_xpath))).click()
    # except:
    #     pass

    # try:
    #     close_button_xpath = '/html/body/div[1]/div[2]/div[2]/button'
    #     WebDriverWait(driver, 7).until(EC.visibility_of_element_located((By.XPATH, close_button_xpath))).click()
    # except:
    #     pass

    title = ''
    pages = 0
    cites_papers = 0
    cites_patents = 0
    full_views = 0
    publisher = ''
    doi = ''
    date_publish = ''
    abstract = ''
    published_in = ''
    authors_list = []
    ieee_keywords_list = []
    author_keywords_list = []

    try:
        title_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span'
        title = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, title_xpath))).text
        print('title: ' + title)
    except:
        pass

    # TODO Number of Pages

    try:
        metrics = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'document-banner-metric-count')))
        
        cites_papers = metrics[0].text
        print('cites_papers: ' + str(cites_papers))

        cites_patents = metrics[1].text
        print('cites_patents: ' + cites_patents)

        full_views = metrics[2].text
        print('full_views: ' + full_views)
    except:
        pass

    try:
        publisher_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/div/div[1]/xpl-publisher/span/span/span/span[2]'
        publisher = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, publisher_xpath))).text
        print('publisher: ' + publisher)
    except:
        pass

    try:
        doi_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[3]/div[2]/div[1]/a'
        doi = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, doi_xpath))).text
        print('doi: ' + doi)
    except:
        pass

    try:
        date_publish = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, 'doc-abstract-confdate'))).text
        date_publish = date_publish[date_publish.index(':')+1:].strip()
        print('date_publish: ' + date_publish)
    except:
        pass

    try:
        abstract_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div/div'
        abstract = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, abstract_xpath))).text
        print('abstract: ' + abstract)
    except:
        pass

    try:
        published_in_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[2]/a'
        published_in = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, published_in_xpath))).text
        print('published_in: ' + published_in)
    except:
        pass

    try:
        authors_arrow_down_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[1]/div/div/i'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, authors_arrow_down_xpath))).click()
        authors = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'authors-accordion-container')))

        for i in range(len(authors)):
            author_name_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[1]/div[2]/div[' + str(i+1) + ']/xpl-author-item/div/div[1]/div/div[1]/a/span'
            author_name = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, author_name_xpath))).text

            author_from_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[1]/div[2]/div[' + str(i+1) + ']/xpl-author-item/div/div[1]/div/div[2]/div'
            author_from = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, author_from_xpath))).text
            authors_list.append(
                {'name': author_name, 'from': author_from}
            )
            print('author name: ' + author_name + ' from: ' + author_from)
    except:
        pass

    try:
        keywords_arrow_down_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[5]/div[1]/div/i'
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, keywords_arrow_down_xpath))).click()
        ieee_keywords = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[5]/div[2]/xpl-document-keyword-list/section/div/ul/li[1]/ul')))

        keywords = ieee_keywords.find_elements(By.CLASS_NAME, 'stats-keywords-list-item')
        for keyword in keywords:
            ieee_keywords_list.append(keyword.text)
            print(keyword.text)

        author_keywords = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/xpl-accordian-section/div/xpl-document-accordion/div[5]/div[2]/xpl-document-keyword-list/section/div/ul/li[3]/ul')))
        keywords = author_keywords.find_elements(By.CLASS_NAME, 'stats-keywords-list-item')
        for keyword in keywords:
            author_keywords_list.append(keyword.text)
            print(keyword.text)
    except:
        pass

    driver.quit()

    return {
        'title': title,
        'pages': int(pages),
        'Cites in Papers': int(cites_papers),
        'Cites in Patent': int(cites_patents),
        'Full Text Views': int(full_views),
        'Publisher': publisher,
        'DOI': doi,
        'Date of Publication': date_publish,
        'abstract': abstract,
        'Published in': published_in,
        'Authors': authors_list,
        'IEEE Keywords': ieee_keywords_list,
        'Author Keywords': author_keywords_list
    }


# def scrape_ieee_xplore(driver):
#     search_topic = 'Blockchain'

#     driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")

#     # accept_button_xpath = '/html/body/div[1]/div[2]/div[2]/button[2]'
#     # WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, accept_button_xpath))).click()
    
#     search_bar_xpath = "/html/body/div[5]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input"
#     search_bar = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
#     search_bar.send_keys(search_topic)
#     search_bar.send_keys(Keys.ENTER)

#     articles_data = []
#     results_filter = ["Conferences"]
#     for text in results_filter:
#         filter_element = WebDriverWait(driver, 20).until(
#             EC.element_to_be_clickable((By.ID, f'refinement-ContentType:{text}'))
#         )
#         filter_element.click()
#     apply_filter_sel = '.facet-ctype-apply-container > button:nth-child(1)'
#     apply_filter_button = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((By.CSS_SELECTOR, apply_filter_sel))
#     )
#     apply_filter_button.click()

#     for i in range(1, 6):
#         print(f"Processing page {i}")

#         article_elements = WebDriverWait(driver, 35).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.result-item a.fw-bold'))
#         )

#         for article_element in article_elements:
#             article_link = article_element.get_attribute('href')
#             print(article_link)
#             article_details = extract_article_details(article_link)
#             if article_details:
#                 print(article_details)
#                 articles_data.append(article_details)
#             time.sleep(5)

#         next_button_sel= '#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > xpl-paginator > div.pagination-bar.hide-mobile.text-base-md-lh > ul > li.next-btn > button'
#         next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_sel)))
#         next_button.click()

#     with open(f'ieee_articles_{search_topic}.json', 'w') as f:
#         json.dump(articles_data, f, indent=4)

def scrape_ieee_xplore_newest(driver):
    search_topic = 'Blockchain'

    driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")

    # accept_button_xpath = '/html/body/div[1]/div[2]/div[2]/button[2]'
    # WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, accept_button_xpath))).click()
    
    search_bar_xpath = "/html/body/div[5]/div/div/div[3]/div/xpl-root/header/xpl-header/div/div[2]/div[2]/xpl-search-bar-migr/div/form/div[2]/div/div[1]/xpl-typeahead-migr/div/input"
    search_bar = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, search_bar_xpath)))
    search_bar.send_keys(search_topic)
    search_bar.send_keys(Keys.ENTER)

    time.sleep(5)

    # Click on the dropdown menu for sorting
    sort_dropdown_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[2]/xpl-select-dropdown/div/button'
    sort_dropdown = WebDriverWait(driver, 25).until(EC.element_to_be_clickable((By.XPATH, sort_dropdown_xpath)))
    sort_dropdown.click()
    


    # Select the "newest" option from the dropdown
    newest_option_xpath = '/html/body/div[5]/div/div/div[3]/div/xpl-root/main/div/xpl-search-results/div/div[2]/div[2]/xpl-results-list/div[2]/xpl-select-dropdown/div/div/button[2]'
    newest_options = WebDriverWait(driver, 25).until(EC.visibility_of_all_elements_located((By.XPATH, newest_option_xpath)))

    for option in newest_options:
        if option.text.lower() == 'newest':
            option.click()
            break

    time.sleep(5)


    articles_data = []
    results_filter = ["Conferences"]
    for text in results_filter:
        filter_element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, f'refinement-ContentType:{text}'))
        )
        filter_element.click()
    apply_filter_sel = '.facet-ctype-apply-container > button:nth-child(1)'
    apply_filter_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, apply_filter_sel))
    )
    apply_filter_button.click()

    for i in range(1, 6):
        print(f"Processing page {i}")

        article_elements = WebDriverWait(driver, 35).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.result-item a.fw-bold'))
        )

        for article_element in article_elements:
            article_link = article_element.get_attribute('href')
            print(article_link)
            article_details = extract_article_details(article_link)
            if article_details:
                print(article_details)
                articles_data.append(article_details)
            time.sleep(5)

        next_button_sel= '#xplMainContent > div.ng-SearchResults.row.g-0 > div.col > xpl-paginator > div.pagination-bar.hide-mobile.text-base-md-lh > ul > li.next-btn > button'
        next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_button_sel)))
        next_button.click()

    with open(f'ieee_articles_{search_topic}_NEWEST.json', 'w') as f:
        json.dump(articles_data, f, indent=4)


if __name__ == "__main__":
    try:
        driver = webdriver.Chrome()
        scrape_ieee_xplore_newest(driver)
        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()