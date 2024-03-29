#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import time
from providers.hostvds import HostvdsHandler
from python_app_logger import get_logger


APP_NAME = os.getenv('APP_NAME', 'metrics-exporter-job-billing-hosting')
APP_VERSION = os.getenv('APP_VERSION', '0.0.0')
APP_ENVIRONMENT = os.getenv('APP_ENVIRONMENT', 'none')
LOGLEVEL = os.getenv('LOGLEVEL', 'DEBUG')

METRICS_STORAGE_URL = os.getenv('METRICS_STORAGE_URL')
METRICS_STORAGE_USERNAME = os.getenv('METRICS_STORAGE_USERNAME')
METRICS_STORAGE_PASSWORD = os.getenv('METRICS_STORAGE_PASSWORD')
METRICS_NAME = os.getenv('METRICS_NAME', 'billing_hosting')

PROVIDER = os.getenv('PROVIDER')
HOSTVDS_URL = os.getenv('HOSTVDS_URL', None)
HOSTVDS_ACCOUNT = os.getenv('HOSTVDS_ACCOUNT', None)
HOSTVDS_PASSWORD = os.getenv('HOSTVDS_PASSWORD', None)

SCRAPE_MAX_TRIES = 3
SCRAPE_TRY_INTERVAL = 10


logger = get_logger(
    app_name=APP_NAME,
    app_version=APP_VERSION,
    app_environment=APP_ENVIRONMENT,
    logger_name='root',
    loglevel=LOGLEVEL
)


if __name__ == "__main__":
    metrics_value = None
    scrape_try = 0

    if PROVIDER == 'hostvds.com':
        Handler = HostvdsHandler
        url = HOSTVDS_URL
        account = HOSTVDS_ACCOUNT
        password = HOSTVDS_PASSWORD

    while scrape_try < SCRAPE_MAX_TRIES:
        metrics = Handler(
            url=url,
            logger_data={
                'app_name': APP_NAME,
                'app_version': APP_VERSION,
                'app_environment': APP_ENVIRONMENT
            },
            loglevel=LOGLEVEL
        )
        metrics_value = metrics.getSiteData(account=account, password=password)
        if not metrics_value:
            scrape_try += 1
            logger.warning(f'Did not get the remote site ({url}) data. Next try: {scrape_try}/{SCRAPE_MAX_TRIES}.')
            del metrics
            time.sleep(SCRAPE_TRY_INTERVAL)
        else:
            logger.info(f'Successfully got remote site ({url}) data. Metrics_value is: {metrics_value}.')
            break

    if metrics_value:
        metrics.pushMetricsToStorage(
            metrics_value=metrics_value,
            metrics_name=METRICS_NAME,
            metrics_storage_url=METRICS_STORAGE_URL,
            metrics_storage_username=METRICS_STORAGE_USERNAME,
            metrics_storage_password=METRICS_STORAGE_PASSWORD,
            metrics_label_account=account
        )
    else:
        logger.critical(f'Did not get the remote site ({url}) data.')
