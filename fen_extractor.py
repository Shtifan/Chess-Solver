from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import subprocess

def get_chrome_version():
    try:
        # Try to get Chrome version using command line
        result = subprocess.run(['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split()[-1]
            return version
    except:
        pass
    return None

def get_fen_from_image(image_path):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = None
    try:
        # Initialize Chrome driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        
        # Navigate to the website
        driver.get("https://elucidation.github.io/ChessboardFenTensorflowJs/")
        
        # Wait for the page to be fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        
        # Wait for file input and upload image
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(os.path.abspath(image_path))
        
        # Initial wait after upload to let the model process
        time.sleep(5)
        
        # Wait for FEN text to appear and stabilize
        previous_fen = None
        stable_count = 0
        max_attempts = 40
        for attempt in range(max_attempts):
            # Try multiple possible selectors where FEN might appear
            selectors = [
                "//div[contains(@class, 'fen')]",
                "//div[contains(@class, 'output')]",
                "//p[contains(text(), '/')]",
                "//*[contains(text(), '/') and string-length() > 20]"
            ]
            
            current_fen = None
            for selector in selectors:
                elements = driver.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text.strip()
                    if ('/' in text and 
                        text.count('/') == 7 and
                        any(c.isdigit() or c.lower() in 'kqrbnp' for c in text)):
                        parts = text.split()
                        candidate_fen = parts[0]
                        # Additional validation to ensure it's a valid FEN
                        if all(c.isdigit() or c.lower() in 'kqrbnp/' for c in candidate_fen):
                            current_fen = candidate_fen
                            print(f"Current FEN (attempt {attempt + 1}): {current_fen}")
                            break
                if current_fen:
                    break
            
            if current_fen:
                if current_fen == previous_fen:
                    stable_count += 1
                    if stable_count >= 5:  # Increased stability requirement
                        print(f"FEN stabilized after {attempt + 1} attempts")
                        return current_fen
                else:
                    stable_count = 0
                previous_fen = current_fen
            
            time.sleep(1.5)  # Increased wait time between attempts
            
        if previous_fen:
            print("Warning: FEN extraction timed out, returning last stable FEN")
            return previous_fen
            
        print("Failed to extract FEN from image")
        return None
        
    except Exception as e:
        print(f"Error in FEN extraction: {str(e)}")
        return None
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    image_path = r"C:\Users\sstoy\Documents\Programing\Projects\Chess Solver\chessboard.jpg"
    fen = get_fen_from_image(image_path)
    if fen:
        print(f"FEN: {fen}")
    else:
        print("Failed to extract FEN")