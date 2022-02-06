import os
import datetime
import pytz

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from base import add_zno, clear

clear()
tz_yek = pytz.timezone('Asia/Yekaterinburg')

login = os.environ.get('LOGIN')
password = os.environ.get('PASSWORD')

driver = webdriver.Chrome()

driver.get('https://sd.atm72.ru/')

el_login = driver.find_element(By.CLASS_NAME, 'login_input')
el_login.send_keys(login)

el_password = driver.find_element(By.CLASS_NAME, 'password_input')
el_password.send_keys(password)

btn_login = driver.find_element(By.CLASS_NAME, 'btn-login')
btn_login.click()

btn_count_zno_in_page = driver.find_element(By.XPATH, '//a[@pc="100"]')
btn_count_zno_in_page.click()

'''Функция ищет на странице нужную информацию и записывает ее в базу. Получает экземпляр страницы и тип ЗНО (0 - 
необработанная, 1 - в работе, 2 - закрыта.'''
def get_data(driver, type_zno):
    el_contract = driver.find_elements(By.CLASS_NAME, 'b-contract-number')
    el_closed_date = driver.find_elements(By.XPATH, '//div[text()="Выполнена:"]')

    el_sla_date_div = driver.find_elements(By.XPATH, '//div[text()="Срок SLA:"]')
    el_sla_date_b = driver.find_elements(By.XPATH, '//b[text()="Срок SLA:"]')

    el_date_of_receipt_heson = driver.find_elements(By.XPATH, '//div[text()="Создана Хессон:"]')
    el_date_of_receipt_others = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')

    el_sla_date = []
    i_sla_date_div, i_sla_date_b = 0, 0

    el_date_of_receipt = []
    i_el_date_of_receipt_heson, i_el_date_of_receipt_others = 0, 0

    for i in range(len(el_contract)):
        if el_contract[i].text == 'АТМ Nautilus Сбербанк':
            el_date_of_receipt.append(el_date_of_receipt_heson[i_el_date_of_receipt_heson].text[16:])
            i_el_date_of_receipt_heson += 1
            el_sla_date.append(el_sla_date_div[i_sla_date_div])
            i_sla_date_div += 1
        else:
            el_sla_date.append(el_sla_date_b[i_sla_date_b])
            i_sla_date_b += 1
            el_date_of_receipt.append(el_date_of_receipt_others[i_el_date_of_receipt_others].text[10:])
            i_el_date_of_receipt_others += 1


    if type_zno == 2:
        zno_closed = 1
    else:
        zno_closed = 0
    for i in range(len(el_contract)):
        try:
            a_dt = datetime.datetime.strptime(el_sla_date[i].text[10:], '%H:%M:%S %d.%m.%Y')
            b_dt = datetime.datetime.strptime(str(datetime.datetime.now(tz_yek))[:-13], '%Y-%m-%d %H:%M:%S')

            if zno_closed == 0:
                delta = a_dt - b_dt
            else:
                delta = a_dt - datetime.datetime.strptime(el_closed_date[i].text[11:], '%H:%M:%S %d.%m.%Y')
            if str(delta)[0] == '-':
                expired = 1
            else:
                expired = 0
        except ValueError:
            expired = 0
        add_zno(el_contract[i].text, el_sla_date[i].text[10:], el_date_of_receipt[i], zno_closed, expired)

'''Получаем и добавляем в базу необработанные ЗНО'''
driver.get('https://sd.atm72.ru/?filtr_department_atm_id=67680525&filtr_wf_current_contract=-1')
get_data(driver, 0)

'''Получаем и добавляем в базу назначеные ЗНО'''
driver.get('https://sd.atm72.ru/?state=in_progress&filtr_notModernization=true')
get_data(driver, 1)

'''Получаем и добавляем в базу закрытые ЗНО'''
driver.get('https://sd.atm72.ru/?state=closed&filtr_notModernization=false')
el_start_date = driver.find_element(By.XPATH, '//input[@cid="date_from"]')
el_start_date.send_keys(datetime.date.today().strftime('%d.%m.%Y'))
sleep(25)
get_data(driver, 2)


sleep(2)
driver.close()
