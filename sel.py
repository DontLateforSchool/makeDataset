from selenium import webdriver
import time
import pyautogui
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

def move_and_click(x, y):
    # Get the current position of the Safari window on the screen
    window_position = browser.get_window_position()
    window_x = window_position['x']
    window_y = window_position['y']

    # Calculate the absolute coordinates on the screen
    absolute_x = window_x + x
    absolute_y = window_y + y

    # Move the mouse to the specified location and click using pyautogui
    pyautogui.moveTo(absolute_x, absolute_y, duration=0.1)
    pyautogui.click()

    time.sleep(1)

def date_click(x, y):
    # Get the current position of the Safari window on the screen
    window_position = browser.get_window_position()
    window_x = window_position['x']
    window_y = window_position['y']

    # Calculate the absolute coordinates on the screen
    absolute_x = window_x + x
    absolute_y = window_y + y

    # Move the mouse to the specified location and click using pyautogui
    pyautogui.moveTo(absolute_x, absolute_y, duration=0.1)
    pyautogui.click()

url = "https://www.stcis.go.kr/pivotIndi/wpsPivotIndicator.do?siteGb=P&indiClss=IC03"

# Launch Safari webdriver
browser = webdriver.Safari()
browser.maximize_window()
browser.get(url)
wait = WebDriverWait(browser, 10)

time.sleep(3)

move_and_click(500, 550)

#달력 이전날짜로 이동 (3월까지)
move_and_click(300, 615)
move_and_click(300, 615)
move_and_click(300, 615)
move_and_click(300, 615)


move_and_click(330, 675)
# move_and_click(330, 705)

date_click(330, 675)
date_click(330, 705)
alert = wait.until(EC.alert_is_present())
time.sleep(1)
alert.accept()

move_and_click(500, 635)
move_and_click(290, 405)
move_and_click(290, 405)
move_and_click(290, 405)
move_and_click(290, 405)
alert = wait.until(EC.alert_is_present())
time.sleep(1)
alert.accept()
# time.sleep(3)

move_and_click(290+150, 435)
# move_and_click(330+ 150, 705)


time.sleep(3)






# Quit the browser
browser.quit()
