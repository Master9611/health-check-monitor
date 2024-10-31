import requests
import yaml
import time
import sys

# Parse YAML file for configuration
def load_config(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

# Health check for an endpoint
def check_health(endpoint):
    try:
        response = requests.request(
            method=endpoint.get('method', 'GET'),
            url=endpoint['url'],
            headers=endpoint.get('headers'),
            data=endpoint.get('body')
        )
        latency = response.elapsed.total_seconds() * 1000  # Convert to milliseconds
        if 200 <= response.status_code < 300 and latency < 500:
            return "UP"
    except requests.RequestException:
        pass
    return "DOWN"

# Log the availability of each domain
def log_availability(availability_stats, total_checks):
    for domain, stats in availability_stats.items():
        percentage = round(100 * stats['up'] / total_checks[domain])
        print(f"{domain} has {percentage}% availability")

# Main function
def main(filepath):
    config = load_config(filepath)
    availability_stats = {}
    total_checks = {}

    while True:
        for endpoint in config:
            domain = endpoint['url'].split('/')[2]
            if domain not in availability_stats:
                availability_stats[domain] = {'up': 0, 'down': 0}
                total_checks[domain] = 0

            status = check_health(endpoint)
            if status == "UP":
                availability_stats[domain]['up'] += 1
            else:
                availability_stats[domain]['down'] += 1
            total_checks[domain] += 1

        log_availability(availability_stats, total_checks)
        time.sleep(15)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python health_check.py <config_file.yaml>")
    else:
        main(sys.argv[1])


