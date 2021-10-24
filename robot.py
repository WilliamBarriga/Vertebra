import os
import datetime
import time
import zipfile

from shutil import rmtree

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector


def create_driver(url, download_directory, actual_directory):
    prefs = {'download.default_directory': f'{download_directory}'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', prefs)
    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities['userDataDir'] = f'{actual_directory}'
    driver = webdriver.Remote(command_executor='127.0.0.1:4444',
                              desired_capabilities=DesiredCapabilities.CHROME,
                              options=options)
    driver.file_detector = LocalFileDetector()
    driver.get(url)
    driver.maximize_window()
    return driver


def find_information(driver, word):
    q = driver.find_element(
        By.XPATH, '/html/body/div[2]/div/div[1]/header/div[1]/div[1]/div/div/div/form/input')
    q.clear()
    q.send_keys(f"{word}")
    q.send_keys(Keys.ENTER)


def found_links(driver):
    pages = driver.find_elements(By.CLASS_NAME, 'browse2-result-name-link')
    links = []
    for page in pages:
        url = page.get_attribute('href')
        links.append(url)

    return links


def open_links(driver, url, download_directory):

    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(url)
    download_csv(driver, download_directory)
    driver.close()
    driver.switch_to.window(original_window)


def download_csv(driver, download_directory):

    try:
        exportar = driver.find_element(By.CSS_SELECTOR, '.download')
        exportar.click()
        csv = driver.find_element(By.LINK_TEXT, 'CSV')
        csv.click()
        wait_for_downloads(download_directory)

    except Exception as e:
        print(f'a ocurrido el error {e}')

    else:
        pass


def text_file(download_directory, now):
    directory_files = os.listdir(download_directory)
    file = open(f'{download_directory}\downloaded_files_{now}.txt', 'w')
    for downloaded_file in directory_files:
        file.write(f'{downloaded_file}\n')


def wait_for_downloads(download_directory):
    print('Waiting for downloads\n')
    while any([filename.endswith('.crdownload') for filename in
               os.listdir(download_directory)]):
        time.sleep(2)
        print('.', end='')
    print("done\n")


def ziping(download_directory):
    ziped_file = zipfile.ZipFile(f'{download_directory}.zip', 'w')

    for folder, subfolders, files in os.walk(download_directory):
        for file in files:
            if file.endswith('.csv') or file.endswith('.txt'):
                ziped_file.write(os.path.join(folder, file),
                                 file, compress_type=zipfile.ZIP_DEFLATED)

    ziped_file.close()
    clear_files(download_directory)
    return ziped_file

def clear_files(download_directory):
    rmtree(download_directory)



def flujo(word, url):
    now = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    new_dir = f'downloads_{now}'
    os.mkdir(new_dir)
    actual_directory = os.getcwd()
    download_directory = f'{actual_directory}\{new_dir}'

    driver = create_driver(url, download_directory, actual_directory)

    find_information(driver, word)
    links = found_links(driver)

    for link in links:
        open_links(driver, link, download_directory)

    driver.quit()

    text_file(download_directory, now)
    ziping(download_directory)

    return f'{download_directory}.zip'


if __name__ == '__main__':

    flujo('numeros', 'https://datos.gov.co')
