import statistics
import matplotlib.pyplot as plt
import numpy as np
import requests
import datetime
import threading
import time
import pandas as pd
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

with open('urls.txt', 'r') as f:
    urls = f.read().splitlines()
start_time = time.time()
num_requests = input("Enter the number of requests: ")

def send_requests(url, good_response_times, bad_response_times):
    try:
        for i in range(int(num_requests)):
            request_time = datetime.datetime.now()
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            response_time = end_time - start_time
            response_time_category = ''
            if response_time < 1:
                response_time_category = 'Low'
            elif response_time < 5:
                response_time_category = 'Medium'
            else:
                response_time_category = 'High'
            if response.status_code == 200:
                good_response_times.append(response_time)
                print(f'Good response time for {url} request {i+1} ({response_time_category}): {response_time:.2f} seconds')
            else:
                bad_response_times.append(response_time)
                print(f'Bad response time for {url} request {i+1} ({response_time_category}): {response_time:.2f} seconds')
    except Exception as e:
        print(f'Error occurred while sending request to {url}: {e}')


total_good_response_times = []
total_bad_response_times = []
threads = []
for url in urls:
    print(f'Testing URL: {url}')
    good_response_times = []
    bad_response_times = []
    for i in range(10):
        t = threading.Thread(target=send_requests, args=(url, good_response_times, bad_response_times))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    total_good_response_times.extend(good_response_times)
    total_bad_response_times.extend(bad_response_times)

num_good_requests = len(total_good_response_times)
num_bad_requests = len(total_bad_response_times)
avg_good_response_time = statistics.mean(total_good_response_times) if num_good_requests > 0 else 0
avg_bad_response_time = statistics.mean(total_bad_response_times) if num_bad_requests > 0 else 0
avg_response_time = statistics.mean(total_good_response_times + total_bad_response_times)
min_response_time = min(total_good_response_times + total_bad_response_times) if num_good_requests + num_bad_requests > 0 else 0
max_response_time = max(total_good_response_times + total_bad_response_times) if num_good_requests + num_bad_requests > 0 else 0



end_time = time.time()
duration = end_time - start_time
print(f'Testing completed in {duration:.2f} seconds.')
# Categorizing response times
low_response_times = [t for t in total_good_response_times + total_bad_response_times if t < 1]
medium_response_times = [t for t in total_good_response_times + total_bad_response_times if 1 <= t < 5]
high_response_times = [t for t in total_good_response_times + total_bad_response_times if t >= 5]

# Table for response time categories
response_time_table_data = {
    'Category': ['Low', 'Medium', 'High'],
    'Count': [len(low_response_times), len(medium_response_times), len(high_response_times)]
}
response_time_table = pd.DataFrame(response_time_table_data)

# Table for request response times
request_response_time_table_data = {
    'Count': [num_good_requests, num_bad_requests],
    'Average': [avg_good_response_time, avg_bad_response_time],
    'Minimum': [min_response_time],
    'Maximum': [max_response_time],
    'Overall Average': [avg_response_time]
}
request_response_time_table = pd.DataFrame(request_response_time_table_data, index=['Successful Requests', 'Failed Requests'])
request_response_time_table.index.name = 'Request Status'

# Set table styles
table_styles = [
    {'selector': 'th', 'props': [('background-color', '#f2f2f2'), ('color', '#333'), ('font-weight', 'bold'), ('border', '1px solid #ccc')]},
    {'selector': 'td', 'props': [('border', '1px solid #ccc')]},
    {'selector': 'table', 'props': [('border-collapse', 'collapse'), ('margin', '15px 0')]},
    {'selector': 'h2', 'props': [('font-size', '24px'), ('font-weight', 'bold'), ('margin', '25px 0 15px')]},
    {'selector': 'img', 'props': [('max-width', '100%'), ('height', 'auto')]}
]


# Create histogram of response times
plt.hist(total_good_response_times + total_bad_response_times, bins=10)
plt.xlabel('Response Time (s)')
plt.ylabel('Count')
plt.title('Response Time Distribution')
plt.savefig('response_time_distribution.png')

# Create HTML file
with open('tables.html', 'w') as f:
    f.write('<html>\n')
    f.write('<head>\n')
    f.write('<style>\n')
    for style in table_styles:
        f.write(f"{style['selector']} {{")
        for prop in style['props']:
            f.write(f"{prop[0]}:{prop[1]};")
        f.write("}\n")
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h2>Response Time Categories:</h2>\n')
    f.write(response_time_table.to_html(index=False, border=0, classes='table table-striped'))
    f.write('<h2>Request Response Times:</h2>\n')
    f.write(request_response_time_table.to_html(border=0, classes='table table-striped'))
    f.write('<h2>Response Time Distribution:</h2>\n')
    f.write(f'<img src="response_time_distribution.png" alt="Response Time Distribution">\n')
    f.write('</body>\n')
    f.write('</html>\n')
    f.write(f'Testing completed in {duration:.2f} seconds.')

# Display tables
print('Response Time Categories:\n')
print(response_time_table.to_string(index=False))
print('\n\nRequest Response Times:\n')
print(request_response_time_table.to_string())
