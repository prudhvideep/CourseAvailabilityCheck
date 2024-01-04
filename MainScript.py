import time
import requests
from selenium import webdriver
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium.webdriver.common.by import By
import smtplib

# Course information
# ASU Course website URL for the specific course
asu_courses = {
    'CSE 546': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=33132-127813',  # Replace with the actual course URL
    'CSE 572': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=29546-104264', 
    'CSE 572': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=26559-104264',
    'CSE 598': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=20160-104278',
    'CSE 578': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=20687-128195'
    #'CSE 510': 'https://catalog.apps.asu.edu/catalog/classes/classlist?campusOrOnlineSelection=C&honors=F&level=grad&promod=F&searchType=all&subject=CSE&term=2241#detailsOpen=31404-104237'
    # Add more courses as needed
}

# Email server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'neilyoung.discography@gmail.com'
smtp_password = 'zidhwfimphonhxuv'
sender_email = 'neilyoung.discography@gmail.com'
receiver_email = 'prudhvideep1996@gmail.com'

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def check_course_availability(course_code, course_url):
    try:
        # Set up the Chrome webdriver (you'll need to have chromedriver installed and in your PATH)
        driver = webdriver.Firefox()

        # Open the ASU course website
        driver.get(course_url)

        # Wait for the page to load (adjust the sleep time as needed)
        time.sleep(5)

        table = driver.find_element(By.XPATH, "//table[@class='table table-sm reserved-seats']")
        
        # Specify the row and column indices (1-based) for the cell you want
        rows = table.find_elements(By.TAG_NAME, "tr") #last row
        row_index = len(rows)-1
        column_index = 1
        
        # Find the cell using XPath
        cell_xpath = f"//tr[{row_index}]/td[{column_index}]"
        cell = table.find_element(By.XPATH, cell_xpath)

        # Get the text value of the cell
        cell_value = cell.text
        seat_count_str = "".join(c for c in cell_value if c.isdigit())
        print(cell_value)
        print(seat_count_str)
        current_seat_count = int(seat_count_str)
        
        return current_seat_count

    except Exception as e:
        print(f"Error checking course availability: {e}")
        return None

    finally:
        # Close the browser window
        driver.quit()

def swap_course():
    try:
       driver = webdriver.Firefox()
       
       url = 'https://catalog.apps.asu.edu/catalog/classes/classlist?term=2241'
       
       driver.get(url)
    
    except Exception as e:
        print(f"Error checking course availability: {e}")
        return None

    finally:
        # Close the browser window
        driver.quit()
        

def main():
    for course_code, course_url in asu_courses.items():
        seat_count_change = check_course_availability(course_code, course_url)
        if seat_count_change > 0:
            update_message = f"The seat availability for {course_code} has changed. Current non reserved seat count: {seat_count_change}"
            send_email(f"ASU Course Update Notification - {course_code}", update_message)
            print(update_message)
            print(f"Update notification sent for {course_code}.")
        else:
            print(f"No changes in seat availability for {course_code}.")

if __name__ == "__main__":
    main()
