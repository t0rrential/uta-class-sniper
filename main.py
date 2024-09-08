from time import sleep

import credentials
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wd_wait


def setup():
    options = Options()
    
    options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=1')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    driver = webdriver.Chrome(options=options)
    
    return driver


def login(driver):

    print("[Sniper]: Logging in...")
    driver.get("https://mymav.uta.edu/guest/portal/index")
    
    wd_wait(driver, credentials.DELAY).until(
        EC.title_is("MyMav - Guests")
    )

    mymavButton = driver.find_element(By.CSS_SELECTOR, "[href='https://mymav.utshare.utsystem.edu/psp/ARCSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_LANDINGPAGE.GBL']")
    mymavButton.click()

    driver.switch_to.window(driver.window_handles[1])

    wd_wait(driver, credentials.DELAY).until(
        EC.title_is("Sign in to your account")
    )

    microsoftLogin = wd_wait(driver, credentials.DELAY).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[type='email']")
        )
    )
    microsoftLogin.click()
    microsoftLogin.send_keys(credentials.USERNAME)

    microsoftButton = driver.find_element(By.CSS_SELECTOR, "[type='submit']")
    microsoftButton.click()

    microsoftSignIn = wd_wait(driver, credentials.DELAY).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[type='password']")
        )
    )
    microsoftSignIn.click()
    microsoftSignIn.send_keys(credentials.PASSWORD)

    microsoftSubmit = driver.find_element(By.CSS_SELECTOR, "[type='submit']")
    microsoftSubmit.click()

    authCode = wd_wait(driver, credentials.DELAY).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[class='displaySign']")
        )
    ).text

    print(
        f"[Sniper]: Waiting on 2 factor authentication. Current method used is MICROSOFT_AUTHENTICATOR. Code on the screen is {authCode}."
    )

    wd_wait(driver, 120).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "[class='ps_box-staticimg nuihdr_logo']")
        )
    )

    print(f"[Sniper]: Sucessfully logged in using {credentials.USERNAME}.")

    del (
        mymavButton,
        microsoftButton,
        microsoftLogin,
        microsoftSignIn,
        microsoftSubmit,
        authCode,
    )

    return driver


def mymav(driver):
    manageClasses = wd_wait(driver, credentials.DELAY).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[src='/cs/ARCSPRD/cache/UTA_HPTILE_MANAGE_CLASSES_1.svg']")
        )
    )
    manageClasses.click()

    wd_wait(driver, credentials.DELAY).until(EC.title_contains("View My Classes"))
    searchButton = wd_wait(driver, credentials.DELAY).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[steplabel='Class Search and Enroll']")
        )
    )
    searchButton.click()

    newestTerm = wd_wait(driver, credentials.DELAY).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[id='SSR_CSTRMCUR_GRD$0_row_0']")
        )
    )
    newestTerm.click()

    while True:
        searchBar = wd_wait(driver, credentials.DELAY).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[placeholder='Enter keyword e.g. course, subject, class, topic']")
            )
        )
        searchBar.click()
        searchTerm = input(
            "[Sniper]: What class are you looking for? Please type out the course ID or course name.\n"
        )
        
        searchBar.send_keys(searchTerm)
        enterSearch = wd_wait(driver, credentials.DELAY).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[id='PTS_SRCH_BTN'][class='ps-button'][role='button']")
            )
        )
        
        enterSearch.click()

        backButton = wd_wait(driver, credentials.DELAY).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[aria-label='Back to page Class Search']")
            )
        )
        
        if len(driver.find_elements(By.CSS_SELECTOR, "div[class*='pts_info-areaerror']")) != 0:
            print("[Sniper]: Class not found. Returning to search")
            backButton.click()
            
        else:
            break
    
    courseSelection = wd_wait(driver, credentials.DELAY).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div[id='win0divPTS_RSLTS_LISTgridc$0']")
        )
    )
    
    courses = courseSelection.find_elements(By.CSS_SELECTOR, "[data-role='button']")
    courseTitles = [course.find_element(By.CSS_SELECTOR, "div[id*='win0divPTS_LIST_TITLE$']").text for course in courses]
    
    print(f"[Sniper]: Found {len(courses)} course(s) from search. In order they are: \n")
    
    for courseIndex in range(len(courses)):
        description, classAvailability = courses[courseIndex].find_element(By.CSS_SELECTOR, "[id*='win0divPTS_LIST_SUMMARY$']").text.split("\n")
        
        print(f"[{courseIndex + 1}]: {courseTitles[courseIndex]} - {description}. Currently {classAvailability}.")
    
    while True:
        try:
            selection = int(input(f"[Sniper]: Please type and enter the index of the course you want surveyed. Possible selections are from 1 - {len(courses)}.\n"))
            assert selection >= 1 and selection <= len(courses)
            selection = selection - 1
            
            break
        except:
            print("[Sniper]: Invalid input. Please try again.")
    
    print(f"[Sniper]: Selected {courseTitles[selection]}.")
    
    courses[selection].click()
    
    classTable = wd_wait(driver, credentials.DELAY).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "[class='ps_grid-flex']")
        )
    )
    
    classTableBody = classTable.find_element(By.CSS_SELECTOR, "tbody[class='ps_grid-body']")

    classes = classTableBody.find_elements(By.CSS_SELECTOR, "[id*='SSR_CLS_DTLS_VW$0_row_']")
    
    classCapacity(driver, classes)
    
    return driver


def classCapacity(driver, classes):
    # what section contains:
    # [0]: Class option number
    # [1]: Availability (Open / WL)
    # [2]: Academic Session
    # [3]: Class & Section Number
    # [4]: Meeting Dates
    # [5]: Class Times and Days
    # [6]: Room
    # [7]: Instructor
    # [8]: Seats
    
    # print(len(classes))
    # [print(f"[[{classThing.text}]]") for classThing in classes]
    
    section = [cell.find_elements(By.CSS_SELECTOR, "td[class*='ps_grid-cell']") for cell in classes]
    
    courseCode = driver.find_element(By.CSS_SELECTOR, "[class='ps_box-edit psc_disabled psc_has_value psc_nolabel psc_font-size11em psc_bold psc_padding-top0_6em']").text
    
    for section in classes:
        sectionInfo = section.find_elements(By.CSS_SELECTOR, "td[class*='ps_grid-cell']")
        
        [cell.text for cell in section]
        
        waitlistText = section[8].split()
        
        print(waitlistText)
        
        if "Open" not in section[1]:
            print(f"[Sniper]: {courseCode} is not open at this time. The waitlist is currently ")

def main():
    driver = setup()

    login(driver)

    mymav(driver)


if __name__ == "__main__":
    main()

