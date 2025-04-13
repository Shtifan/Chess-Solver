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
    # Set up minimal Chrome options for speed
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=800,600')  # Reduced window size
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    driver = None
    try:
        # Initialize Chrome driver with shorter timeout
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(20)
        
        # Navigate to the website
        driver.get("https://elucidation.github.io/ChessboardFenTensorflowJs/")
        
        # Wait for file input with shorter timeout
        file_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Upload the image
        file_input.send_keys(os.path.abspath(image_path))
        
        # Wait for FEN with shorter intervals
        fen_text = None
        for _ in range(10):  # More frequent checks
            elements = driver.find_elements(By.XPATH, "//*[contains(text(), '/')]")
            for element in elements:
                text = element.text.strip()
                if '/' in text and any(c.isdigit() for c in text) and len(text) > 10:
                    fen_text = text
                    break
            if fen_text:
                break
            time.sleep(0.5)  # Shorter sleep intervals
            
        return fen_text
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
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