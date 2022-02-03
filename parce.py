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

'''Функция ищет на странице нужную информацию и записывает ее в базу'''
def get_data(driver, type_zno):
    el_contract = driver.find_elements(By.CLASS_NAME, 'b-contract-number')

    el_sla_date = driver.find_elements(By.XPATH, '//div[text()="Срок SLA:"]')
    print(el_sla_date[0].text[19:])
    print(el_contract[0].text)




'''Получаем и добавляем в базу необработанные ЗНО'''
driver.get('https://sd.atm72.ru/?filtr_department_atm_id=67680525&filtr_wf_current_contract=-1')


'''Получаем и добавляем в базу назначеные ЗНО'''
driver.get('https://sd.atm72.ru/?state=in_progress&filtr_notModernization=true')
get_data(driver)

'''Получаем и добавляем в базу закрытые ЗНО'''
#driver.get('https://sd.atm72.ru/?state=closed&filtr_notModernization=false')
#el_start_date = driver.find_element(By.XPATH, '//input[@cid="date_from"]')
#el_start_date.send_keys(datetime.date.today().strftime('%d.%m.%Y'))
#sleep(30)












""""
    if i == 96:
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Передана инженеру:"]')
    elif i == 209:
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')
    elif i == 184:
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')
    elif i == 217:
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')
    elif i == 201:              
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')
    elif i == 118:
        el_number = driver.find_elements(By.CLASS_NAME, f'table-external-id-{i}')
        el_created_date = driver.find_elements(By.XPATH, '//div[text()="Получена:"]')

    el_sla_date = driver.find_elements(By.XPATH, '//div[text()="Срок SLA:"]')


    for j in range(len(el_created_date)):
        if el_number[j].text:
            x = el_number[j].text
        else:
            y = 'NO'
        try:
            y = el_sla_date[j].text[10:]
        except Exception:
            y = 'NO'
        if i == 96:
            z = el_created_date[j].text[16:]
        else:
            z = el_created_date[j].text[10:]

        try:
            a_dt = datetime.datetime.strptime(y, '%H:%M:%S %d.%m.%Y')
            print(a_dt)
            b_dt = datetime.datetime.strptime(str(datetime.datetime.now(tz_yek))[:-13], '%Y-%m-%d %H:%M:%S')
            print(b_dt)
            delta = a_dt - b_dt
            if str(delta)[0] == '-':
                expired = 1
            else:
                expired = 0
        except ValueError:
            expired = 0

        add_zno(x, i, z, y, 0, expired)
"""











sleep(2)
driver.close()
