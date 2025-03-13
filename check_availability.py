from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

app = Flask(__name__)

def check_availability(location, date):
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = f"http://studion.co.kr/dashboard?location={location}&date={date}"
        driver.get(url)
        time.sleep(5)

        available = False
        try:
            element = driver.find_element(By.CLASS_NAME, "available-slot")
            available = True if element else False
        except:
            available = False

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

    return {"available": available}

@app.route('/check_availability', methods=['POST'])
def check():
    data = request.json
    location = data.get("location")
    date = data.get("date")

    if not location or not date:
        return jsonify({"error": "Missing location or date"}), 400

    result = check_availability(location, date)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
