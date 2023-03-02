# Load-testing
This code appears to be a script for testing the response times of a list of URLs. The script prompts the user to enter the number of requests to be made to each URL and then sends requests to each URL in a separate thread. For each request, the script measures the response time and categorizes it as "Low," "Medium," or "High" based on its duration. The script also categorizes the response times into "Low," "Medium," and "High" categories and generates a histogram of the distribution of response times.

Additionally, the script generates two tables in an HTML file, one for the number of requests in each response time category and one for the statistics of the response times for successful and failed requests. These tables include information such as the average response time, the minimum and maximum response times, and the overall average response time.

Overall, this script could be useful for testing the response times of a list of URLs and determining if there are any issues with the response times of these URLs. The generated tables and histogram could help provide insights into the performance of the URLs and identify any issues that need to be addressed.


#Usage 

create a file called urls.txt

#To run

python ltest.py

![response_time_distribution](https://user-images.githubusercontent.com/59091676/222424706-cf57bb7a-3f63-4b9f-803f-5e3ea7220de2.png)
