import os
import subprocess
import time
import logging
import psutil
from dotenv import load_dotenv
from twilio.rest import Client
import google.generativeai as genai

# Logging configuration
logging.basicConfig(
    filename="/root/stress_test.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

load_dotenv()

API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

def fetch_logs():
    with open('stress_test.log', 'r') as file:
        lines = file.readlines()[-40:]
    return ''.join(lines)

def send_logs_to_api(logs):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"You are an SRE. You have to suggest troubleshooting steps based on the given logs in 200 words.\n{logs}")
    print(response.text)
    return response.text

def send_whatsapp_message(message_body):
    account_sid = os.environ["ACC_SID"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    sent_message = client.messages.create(
        body=message_body,
        from_=os.environ["from_whatsapp_number"],
        to=os.environ["to_whatsapp_number"]
    )
    print("WhatsApp message sent with SID:", sent_message.sid)
    return sent_message.sid

def memory_stress_test():
    logging.info("Starting Memory Stress Test...")
    print("Starting Memory Stress Test...")
    try:
        stress_process = subprocess.Popen(
            ["stress-ng", "--vm", "1", "--vm-bytes", "80%", "-t", "30s"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        start_time = time.time()
        while time.time() - start_time < 30:
            time.sleep(1)
            memory_usage = psutil.virtual_memory().percent
            if memory_usage > 80:
                logging.info(f"Memory usage stress test: {memory_usage}%")

        stdout, stderr = stress_process.communicate()

        if stderr:
            logging.error(f"Error during Memory stress test: {stderr.decode().strip()}")

    except Exception as e:
        logging.error(f"Exception occurred during Memory stress test: {str(e)}")

    print("Memory Stress Test Completed.")
    logging.info("Memory Stress Test Completed.")

def disk_stress_test():
    logging.info("Starting Disk Stress Test...")
    print("Starting Disk Stress Test...")
    try:
        stress_process = subprocess.Popen(
            ["stress-ng", "--iomix", "4", "--iomix-bytes", "90%", "--timeout", "30"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        start_time = time.time()
        while time.time() - start_time < 30:
            time.sleep(1)
            disk_usage = psutil.disk_usage('/').percent
            if disk_usage > 80:
                logging.info(f"Disk usage stress test: {disk_usage}%")

        stdout, stderr = stress_process.communicate()

        if stderr:
            logging.error(f"Error during Disk stress test: {stderr.decode().strip()}")

    except Exception as e:
        logging.error(f"Exception occurred during Disk stress test: {str(e)}")

    print("Disk Stress Test Completed.")
    logging.info("Disk Stress Test Completed.")

def network_stress_test():
    logging.info("Starting Network Stress Test...")
    print("Starting Network Stress Test...")
    try:
        result = subprocess.run(
            ['iperf3', '-c', '192.168.1.7', '-t', '30'],
            capture_output=True,
            text=True
        )
        print(result.stdout)

        if result.stderr:
            logging.error(f"Error during Network stress test: {result.stderr.strip()}")
        else:
            start_time = time.time()
            while time.time() - start_time < 30:
                time.sleep(1)
                bytes_sent = psutil.net_io_counters().bytes_sent
                bytes_recv = psutil.net_io_counters().bytes_recv
                total_bytes = (bytes_sent + bytes_recv) * 8 / (1024 * 1024)
                logging.info(f"Total network usage: {total_bytes:.2f} Mbps")

    except Exception as e:
        logging.error(f"Exception occurred during Network stress test: {str(e)}")

    print("Network Stress Test Completed.")
    logging.info("Network Stress Test Completed.")

def cpu_stress_test():
    logging.info("Starting CPU Stress Test...")
    print("Starting CPU Stress Test...")
    try:
        stress_process = subprocess.Popen(
            ["stress-ng", "--cpu", "4", "--cpu-load", "80", "-t", "60s"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        start_time = time.time()
        while time.time() - start_time < 60:  # Monitor for 60 seconds
            cpu_usage = psutil.cpu_percent(interval=1)
            logging.info(f"CPU Usage: {cpu_usage}%")

            if cpu_usage > 80:
                logging.warning(f"High CPU Usage Detected: {cpu_usage}%")

        stdout, stderr = stress_process.communicate()

        if stderr:
            logging.error(f"Error during CPU stress test: {stderr.decode().strip()}")

    except Exception as e:
        logging.error(f"Exception occurred during CPU stress test: {str(e)}")

    print("CPU Stress Test Completed.")

def mysql_stress_test():
    logging.info("Starting MySQL Stress Test...")
    vm2_ip = '192.168.1.7'
    process = subprocess.Popen([
        'sysbench',
        '--test=/usr/share/sysbench/oltp_read_only.lua',
        '--mysql-db=random',
        '--mysql-user=stress',
        '--mysql-password=password',
        f'--mysql-host={vm2_ip}',
        '--max-time=30',
        '--max-requests=0',
        '--threads=2',
        'run'
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
    )

    for line in iter(process.stdout.readline, ''):
        logging.info(line.strip())

    process.stdout.close()
    process.wait()

    if process.returncode == 0:
        logging.info("MySQL Stress Test Completed successfully.")
    else:
        error_message = process.stderr.read().strip()
        logging.error(f"MySQL Stress Test encountered an error: {error_message}")

    process.stderr.close()
    logging.info("MySQL Stress Test Completed.")

def main():
    while True:
        print("\nSelect an option for stress testing:")
        print("1. Memory Stress Testing")
        print("2. Disk Stress Testing")
        print("3. Network Stress Testing")
        print("4. CPU Stress Testing")
        print("5. MySQL Stress Testing")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            memory_stress_test()
        elif choice == "2":
            disk_stress_test()
        elif choice == "3":
            network_stress_test()
        elif choice == "4":
            cpu_stress_test()
        elif choice == "5":
            mysql_stress_test()
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

        logs = fetch_logs()
        analysis_result = send_logs_to_api(logs)
        #print(analysis_result)
        if analysis_result:
            send_whatsapp_message(analysis_result)

if __name__ == "__main__":
    main()
