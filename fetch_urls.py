import datetime
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager


def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root


if __name__ == '__main__':
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    shadow = Shadow(driver)
    shadow.set_implicit_wait(5)

    site_url = "https://www.uradprace.cz/web/en/vacancies-search"
    driver.get(site_url)

    total_vacancies_urls = 0

    while True:
        vacancies_url =[]        

        vacancies_links = shadow.find_elements('ag-link[class="with-icon smaller no-print-href"]')

        for link in vacancies_links:
            shadow_section = expand_shadow_element(link)
            url = shadow_section.find_element_by_tag_name('a').get_attribute('href')
            vacancies_url.append(url)

        
        total_vacancies_urls += len(vacancies_links)
        print(f'{str(datetime.datetime.now())} - fetched {total_vacancies_urls} links')
        
        with open("cz_vacancies_url.txt", "a") as text_file:
            print(*vacancies_url, file=text_file, sep="\n")

        next_page = shadow.find_element('a[aria-label="Následující"]') or shadow.find_element('a[aria-label="Next"]')
        
        if not next_page.is_displayed():
            break
        
        driver.execute_script("arguments[0].click()", next_page)
        
    driver.close()