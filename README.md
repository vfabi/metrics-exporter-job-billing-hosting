# metrics-exporter-job-billing-hosting
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/vfabi/metrics-exporter-job-billing-hosting)
![GitHub last commit](https://img.shields.io/github/last-commit/vfabi/metrics-exporter-job-billing-hosting)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![Generic badge](https://img.shields.io/badge/hub.docker.com-vfabi/metrics_exporter_job_billing_hosting-<>.svg)](https://hub.docker.com/repository/docker/vfabi/metrics-exporter-job-billing-hosting)
![Docker Pulls](https://img.shields.io/docker/pulls/vfabi/metrics-exporter-job-billing-hosting)

Metrics exporter job to get billing info from hosting providers and push it to remote Prometheus/Victoriametrcs storage.  


## Features
- hostvds.com provider support


## Technology stack
- Python 3.8+
- Selenium


## Requirements and dependencies
Python requirements in requirements.txt


## Configuration
### Environment variables
| Name   |      Required     |  Required if | Values |Description|
|----------|:-------------:|------:|------:|:------|
|APP_NAME|False||default=metrics-exporter-job-billing-hosting|Application name.|
|APP_VERSION|False||default=0.0.0|Application version.|
|APP_ENVIRONMENT|False||default=none|Application environment.|
|LOGLEVEL|False||default=DEBUG; values=DEBUG,INFO,WARNING,CRITICAL|Logging level.|
|METRICS_STORAGE_URL|True||example=https://mon.example.com/victoriametrics/api/v1/import/prometheus|Remote metrics storage URL.|
|METRICS_STORAGE_USERNAME|True|||Remote metrics storage username.|
|METRICS_STORAGE_PASSWORD|True|||Remote metrics storage password.|
|METRICS_NAME|False||default=billing_hosting|Metric name.|
|PROVIDER|True||values=hostvds.com|Provider name.|
|HOSTVDS_URL|False|PROVIDER = hostvds.com||hostvds.com provider URL.|
|HOSTVDS_ACCOUNT|False|PROVIDER = hostvds.com||hostvds.com provider account.|
|HOSTVDS_PASSWORD|False|PROVIDER = hostvds.com||hostvds.com provider password.|


## Usage
Can be run as a standalone python application or as docker packed application.  
Kubernetes cronjob example you can find in [main.yaml](deployment/kubernetes/main.yaml)


## Docker
[![Generic badge](https://img.shields.io/badge/hub.docker.com-vfabi/metrics_exporter_job_billing_hosting-<>.svg)](https://hub.docker.com/repository/docker/vfabi/metrics-exporter-job-billing-hosting)


## Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!


## License
Apache 2.0