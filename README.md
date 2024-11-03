# Stress Testing and Monitoring System with Ansible, Docker, Kubernetes, Prometheus, and Grafana

This project sets up a scalable and monitored stress-testing system across multiple virtual machines (VMs) using **Ansible**, **Prometheus**, **Grafana**, **Docker**, and **Kubernetes**. The application provides a menu-based Python script for performing stress tests on memory, CPU, disk, network, and MySQL resources. This README guides you through setup, usage, and deployment.

## Project Overview

The project automates VM setup, configures monitoring tools, and provides stress-testing capabilities on:

- **VM_0**: Hosts Prometheus, Grafana, and Alertmanager.
- **VM_1**: Runs the Python script, Jenkins for CI/CD Pipeline, Node Exporter and MySQL Exporter for monitoring.
- **VM_2**: Hosts MySQL Server .

Ansible is used to automate installations and configurations across the VMs.

## Prerequisites

- Three VMs running a Linux distribution (e.g., CentOS 9).
- Ansible installed on the host machine.
- Passwordless SSH access set up for the VMs.

## Setup Instructions

### Step 1: Clone Virtual Machines

1. Clone three VMs (`vm_0`, `vm_1`, and `vm_2`) and configure hostnames and firewall settings.
2. Run `systemctl set-hostname <name>` to set hostnames.
3. Stop the firewall on all VMs using:
   ```bash
   systemctl stop firewalld
   ```

### Step 2: Configure Ansible

1. Create an Ansible inventory and configuration files for automation.
2. Define roles and playbooks for Prometheus, Grafana, Alertmanager, MySQL, Node Exporter, and MySQL Exporter installations.

### Step 3: Install Monitoring Tools

Run the provided Ansible playbooks to automate installation and configuration:
- **VM_0**: Prometheus, Grafana, Alertmanager
- **VM_1**: Node Exporter, MySQLD Exporter
- **VM_2**: MySQL Server

### Step 4: Configure Prometheus

- Access Prometheus at `http://<vm0_IP>:9090`.
- Configure Prometheus to scrape metrics from Node Exporter and MySQLD Exporter.

### Step 5: Set Up Grafana

1. Access Grafana at `http://<vm0_IP>:3000` with username and password as `admin`.
2. Add Prometheus as a data source and import relevant dashboards for MySQL and Node Exporter.

## Running Stress Tests

1. SSH into **VM_1**.
2. Run the `main.py` Python script, which provides options for memory, disk, network, CPU, and MySQL stress tests.
   ```bash
   python3 main.py
   ```

### Docker and Kubernetes Deployment

1. **Containerize** the application by building a Docker image with the provided `Dockerfile`.
   ```bash
   docker build -t <image_name> .
   ```
2. Deploy on **Kubernetes**:
   ```bash
   kubectl apply -f deployment.yml
   ```

### Alerts and Notifications

1. Configure **Alertmanager** on `vm_0` to send alerts via email.
2. Modify `alertmanager.yml` with SMTP settings for email notifications on threshold breaches.

## Logging and Analysis

Logs are saved in `stress_test.log` and can be analyzed for insights. Integrate with Google Generative AI or Twilio for automated log analysis and sending suggestions via WhatsApp.

## CI/CD Setup with Jenkins and GitHub Webhooks

1. Install Jenkins on **VM_1** and configure webhooks for GitHub repository.
2. Use `ngrok` to expose Jenkins for webhook communication.

