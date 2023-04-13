from selenium import webdriver

# Kies de webbrowser die je wilt gebruiken en geef het pad naar de driver op
browser = webdriver.Chrome('/pad/naar/chromedriver')

# Open de zoekpagina van de webbrowser
browser.get('https://www.google.com')

# Zoek naar het zoekvak op de pagina en typ 'goedkope appels' in het zoekvak
search_box = browser.find_element_by_name('q')
search_box.send_keys('goedkope appels')

# Zoek naar de zoekknop op de pagina en klik erop
search_button = browser.find_element_by_xpath("//div[@class='FPdoLc tfB0Bf']//input[@name='btnK']")
search_button.click()
