from selenium import webdriver

# Kies de webbrowser die je wilt gebruiken en geef het pad naar de driver op
browser = webdriver.Chrome('/pad/naar/chromedriver')

# Open de zoekpagina van de webbrowser
browser.get('https://www.google.com')

# Zoek naar het zoekvak op de pagina en typ 'goedkope appels' in het zoekvak
search_box = browser.find_element_by_name('q')
search_box.send_keys('goedkope appels')

# Zoek naar de zoekknop op de pagina en klik erop
search_button = browser.find_element_by_xpath("//div[@class='FPdoLc tfB0Bf']//input[@name='btnK']")
search_button.click()


from datetime import datetime
from django.utils import timezone
from Login.models import Leerling, Sessie,Begeleider,User,Vak,Klas,Niveau,School
# Assuming you have already retrieved the Leerling instance for "Sam Aalders"
leerling = Leerling.objects.get(naam="sam")
begeleider_test=User.objects.get(username='Iris')
school_test=School.objects.get(naam='vo')

# Create 20 sessions for Sam Aalders
for i in range(1, 21):
    # Create a new Sessie instance
    sessie = Sessie.objects.create(
        
        datum=timezone.now(),  # Use the current datetime as the session date
        inzicht=  2,  # Set a different inzicht value for each session
        kennis= 3,  # Set a different kennis value for each session
        werkhouding= 4,  # Set a different werkhouding value for each session
        extra=f"In this updated code, we are using the Table class from ReportLab to create a table for the session information. We define the table data as a list of lists, where each sublist represents a row in the table. The table is styled using the TableStyle class to set background colors, text colors, alignment, font size, and padding. Finally, we add the table to the content and build the PDF document. styled using the TableStyle class to set background colors, text colors, alignment, font size, and padding. Finally, we add the table to the content and build the PDF document. styled using the TableStyle class to set background colors, text colors, alignment, font size, and padding. Finally, we add the table to the content and build the PDF document.",
        Leerling=leerling,  # Assign the session to Sam Aalders
        begeleider=begeleider_test,
        school=school_test,
        vak=Vak.objects.get(naam='Frans'),
    )
    # Save the session
    sessie.save()

print("Sessions created successfully.")