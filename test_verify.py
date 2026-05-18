import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration variables matching cluster local node setup
FRONTEND_URL = os.getenv("TEST_FRONTEND_URL", "http://localhost:80")
BACKEND_URL = os.getenv("TEST_BACKEND_URL", "http://localhost:5000")
TIMEOUT_LIMIT = 6

def init_driver():
    """Initializes chrome webdriver with typical student lab options"""
    try:
        opts = webdriver.ChromeOptions()
        # opts.add_argument('--headless') # keep disabled to watch browser open live during viva
        opts.add_argument('--log-level=3')
        opts.add_argument('--start-maximized')
        
        driver = webdriver.Chrome(options=opts)
        return driver
    except Exception as init_err:
        print(f"[-] Webdriver Initialization Failure: {init_err}")
        sys.exit(1)

def run_tests():
    print("[*] Starting automation test suite execution script...")
    driver = init_driver()
    passed_cases = 0
    
    try:
        # 📋 TEST CASE 1: Platform Homepage Asset Loading Verification [cite: 66, 68]
        print("[->] Running Test Case 1: Title & Dashboard Verification...")
        driver.get(FRONTEND_URL)
        
        # Checking if title contains academic platform naming structure
        WebDriverWait(driver, TIMEOUT_LIMIT).until(EC.title_contains("OpenReview"))
        current_title = driver.title
        print(f"[+] Test Case 1 Passed. Target Title Located: '{current_title}'")
        passed_cases += 1
        
        # 📋 TEST CASE 2: DOM Form/Input Element Structural Layout Scan [cite: 66, 69]
        print("[->] Running Test Case 2: Validation of Layout Content Areas...")
        time.sleep(1) # standard delay to ensure async rendering completes
        
        # Checking body markup wrapper presence
        main_content = driver.find_element(By.TAG_NAME, "body")
        if len(main_content.text.strip()) > 0:
            print("[+] Test Case 2 Passed. Validated active DOM text layers.")
            passed_cases += 1
        else:
            print("[-] Test Case 2 Failed. DOM container parsed empty.")

        # 📋 TEST CASE 3: Direct Core Microservice Handshake Check [cite: 66, 70]
        print("[->] Running Test Case 3: Evaluating Microservice Connectivity...")
        driver.get(BACKEND_URL)
        
        time.sleep(0.5)
        response_container = driver.find_element(By.TAG_NAME, "body")
        server_response = response_container.text
        
        # Check for non-empty response or standard status objects
        if server_response:
            print(f"[+] Test Case 3 Passed. Backend responded: {server_response[:35]}...")
            passed_cases += 1
        else:
            print("[-] Test Case 3 Failed. No response payload from targeted port.")

    except Exception as test_exception:
        print(f"[-] Execution interrupted due to runtime exception: {test_exception}")
        
    finally:
        print("\n==================================================")
        print(f"[*] Summary: ({passed_cases}/3) Automated Assertions Completed Successfully.") 
        print("==================================================")
        time.sleep(3333)
        driver.quit()

if __name__ == "__main__":
    run_tests()