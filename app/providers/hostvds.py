#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import time
import requests
from requests.auth import HTTPBasicAuth
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from python_app_logger import get_logger


class HostvdsHandler():

    SLEEP_INTERVAL = 5
    PROVIDER_NAME = 'hostvds.com'

    def __init__(self, url, logger_data, loglevel='DEBUG', debug=False):
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        self.driver = Chrome(options=options)
        self.url = url
        self.driver.get(url)
        self.debug = debug
        self.logger = get_logger(
            app_name=logger_data['app_name'],
            app_version=logger_data['app_version'],
            app_environment=logger_data['app_environment'],
            loglevel=loglevel
        )

    def _crawlSite(self, account, password):
        try:
            # Load auth page
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "input-dg")))
            if self.debug:
                self.driver.save_screenshot('1-page-auth.png')
            input_email = self.driver.find_element(By.XPATH, "//input[@type='email']")
            input_password = self.driver.find_element(By.XPATH, "//input[@type='password']")
            button_submit = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            # print(input_email.get_attribute('placeholder'), input_password.get_attribute('placeholder'), button_submit.text)

            # Fill credentials form and submit
            input_email.send_keys(account)
            input_password.send_keys(password)
            if self.debug:
                self.driver.save_screenshot('2-page-auth-fill-form.png')
            button_submit.click()

            # Follow Billing section
            time.sleep(self.SLEEP_INTERVAL)
            if self.debug:
                self.driver.save_screenshot('3-page-main.png')
            button_billing_section = self.driver.find_element(By.LINK_TEXT, 'Billing')
            button_billing_section.click()

            # Get balance from the page
            time.sleep(self.SLEEP_INTERVAL)
            if self.debug:
                self.driver.save_screenshot('4-page-billing.png')
            balance_text = self.driver.find_element(By.CLASS_NAME, "charges-info__balance")

            return balance_text.text
        except Exception as e:
            self.logger.critical(f'Raised exception while remote site ({self.url}) selenium crawling. Details: {e}')

    def getSiteData(self, account, password):
        value = None
        data = self._crawlSite(account, password)
        if data:
            pattern = re.compile(r'\d+.\d+')
            value = pattern.findall(data)[0]
        return value

    def pushMetricsToStorage(
            self,
            metrics_value,
            metrics_name,
            metrics_storage_url,
            metrics_storage_username,
            metrics_storage_password,
            metrics_label_account
        ):
        metric = '%s{account="%s",provider="%s"} %s' % (metrics_name, metrics_label_account, self.PROVIDER_NAME, metrics_value)
        self.logger.debug(f'The metric and value is: {metric}')

        response = requests.post(
            metrics_storage_url,
            data=metric,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            auth=HTTPBasicAuth(metrics_storage_username, metrics_storage_password)
        )
        self.logger.info(f'Pushed metric to remote metrics storage. Response status code is {response.status_code}.')
        return response.status_code
