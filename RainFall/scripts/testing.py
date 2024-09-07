import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import atexit
import shutil

# Function to hide unwanted elements by XPath instead of removing them
def hide_element(driver, xpath):
    try:
        element = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].style.display='none';", element)
        print(f"Hidden element: {xpath}")
    except Exception as e:
        print(f"Failed to hide element {xpath}: {e}")

# Function to click an element by XPath
def click_element(driver, xpath, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        print(f"Clicked element: {xpath}")
        return True
    except TimeoutException:
        print(f"Timeout while waiting for element: {xpath}")
        return False

# Function to inject control panel HTML with testing buttons into the Snapchat web page
def inject_control_panel(driver):
    panel_script = """
    (function () {
        let snapCount = 0;
        let loopRunning = false;
        let nightMode = false;

        const elementsToDelete = [
            '/html/body/main/div[1]/div[1]'
        ];

        const elementsToHide = [
            '/html/body/main/div[1]/div[1]',
            '/html/body/main/div[1]/div[2]/div/div/div/img',
            '/html/body/main/div[1]/div[2]/div/div/div/div[1]'
        ];

        function deleteElements() {
            elementsToDelete.forEach(xpath => {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) element.remove();
            });
        }

        function hideElements() {
            elementsToHide.forEach(xpath => {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) element.style.display = 'none';
            });
        }

        function widenElement() {
            const elementXpath = '/html/body/main/div[1]/div[2]/div/div/div';
            const element = document.evaluate(elementXpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {
                element.style.width = '65vw';
            }
        }

        const styles = `
            @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
            
            #rainfall-ui {
                position: fixed;
                top: 0;
                right: 0;
                width: 450px;
                height: 100%;
                background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
                color: #b19cd9;
                font-family: 'Orbitron', sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                padding: 20px;
                box-sizing: border-box;
                box-shadow: -5px 0 15px rgba(177, 156, 217, 0.3);
                z-index: 9999;
                overflow-y: auto;
                transition: all 0.3s ease;
            }

            #rainfall-ui::-webkit-scrollbar {
                width: 10px;
            }

            #rainfall-ui::-webkit-scrollbar-track {
                background: #1a1a1a;
            }

            #rainfall-ui::-webkit-scrollbar-thumb {
                background: #b19cd9;
                border-radius: 5px;
            }

            #rainfall-ui h2 {
                font-size: 2.5em;
                margin-bottom: 30px;
                text-align: center;
                color: #b19cd9;
                text-shadow: 0 0 10px rgba(177, 156, 217, 0.5);
                animation: neonGlow 1.5s ease-in-out infinite alternate;
            }

            @keyframes neonGlow {
                from {
                    text-shadow: 0 0 5px #b19cd9, 0 0 10px #b19cd9, 0 0 15px #b19cd9;
                }
                to {
                    text-shadow: 0 0 10px #b19cd9, 0 0 20px #b19cd9, 0 0 30px #b19cd9;
                }
            }

            .input-group {
                width: 100%;
                display: flex;
                justify-content: space-between;
                margin-bottom: 20px;
            }

            .input-wrapper {
                width: 48%;
            }

            .input-wrapper label {
                display: block;
                margin-bottom: 5px;
                color: #b19cd9;
                font-weight: bold;
            }

            .input-wrapper input {
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                background-color: #2a2a2a;
                color: #b19cd9;
                font-size: 16px;
                transition: all 0.3s ease;
            }

            .input-wrapper input:focus {
                outline: none;
                box-shadow: 0 0 0 2px #b19cd9;
            }

            .button {
                width: 100%;
                padding: 15px;
                margin-bottom: 15px;
                border: none;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                background-color: #2a2a2a;
                color: #b19cd9;
            }

            .button::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                background: rgba(177, 156, 217, 0.2);
                border-radius: 50%;
                transform: translate(-50%, -50%);
                transition: all 0.5s ease;
            }

            .button:hover {
                background-color: #3a3a3a;
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(177, 156, 217, 0.4);
            }

            .button:active::before {
                width: 300px;
                height: 300px;
            }

            #snapCounter {
                font-size: 24px;
                font-weight: bold;
                margin-top: 30px;
                padding: 15px;
                background-color: #2a2a2a;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(177, 156, 217, 0.3);
                transition: all 0.3s ease;
            }

            #snapCounter:hover {
                transform: scale(1.05);
                box-shadow: 0 0 20px rgba(177, 156, 217, 0.5);
            }

            .night-mode {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.9);
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: #b19cd9;
                font-family: 'Orbitron', sans-serif;
                z-index: 10000;
            }

            .night-mode button {
                padding: 15px 30px;
                font-size: 20px;
                background-color: #b19cd9;
                color: #0f0f0f;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
            }

            .night-mode button:hover {
                background-color: #0f0f0f;
                color: #b19cd9;
                box-shadow: 0 0 15px #b19cd9;
            }

            .night-mode #nightSnapCounter {
                font-size: 36px;
                margin-top: 30px;
            }
        `;

        const styleSheet = document.createElement("style");
        styleSheet.type = "text/css";
        styleSheet.innerText = styles;
        document.head.appendChild(styleSheet);

        const uiHtml = `
            <div id="rainfall-ui">
                <h2>RainFall V2</h2>
                <div class="input-group">
                    <div class="input-wrapper">
                        <label for="shortcutNumber">Shortcut Number:</label>
                        <input id="shortcutNumber" type="number" min="1" value="1">
                    </div>
                    <div class="input-wrapper">
                        <label for="recipientsNumber">Number of Recipients:</label>
                        <input id="recipientsNumber" type="number" min="1" value="1">
                    </div>
                </div>
                <button id="toggleLoopButton" class="button">Start Loop</button>
                <button id="toggleNightModeButton" class="button">Night Mode</button>
                <div id="snapCounter">Snaps Sent: 0</div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', uiHtml);

        // Define the XPaths
        const cameraXPath = '/html/body/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/button';
        const sendToXPath = '/html/body/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/button[2]';
        const shortcutBaseXPath = '/html/body/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/form/div/div[2]/button[';
        const recipientBaseXPath = '//*[@id="root"]/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/form/div/ul/li[';
        const sendSnapXPath = '/html/body/main/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/form/div[2]/button';
        const sleeperXPath = '//*[@id="root"]/div[1]/div[2]/div/div/div/div[2]/div[1]/div/div/div/div/div/button';

        // Function to get dynamic XPaths
        function getShortcutXPath() {
            const shortcutNumber = document.getElementById('shortcutNumber').value;
            return shortcutBaseXPath + shortcutNumber + ']';
        }

        function getRecipientXPaths() {
            const recipientsNumber = parseInt(document.getElementById('recipientsNumber').value);
            return Array.from({length: recipientsNumber}, (_, i) => recipientBaseXPath + (i + 2) + ']/div/div[3]');
        }

        // Function to click an element
        async function clickElement(xpath) {
            const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (element) {
                element.click();
                console.log(`Clicked element at ${xpath}`);
            } else {
                console.log(`Failed to find element at ${xpath}`);
            }
        }

        // Function to run the sequence
        async function runSequence() {
            const sequence = [
                cameraXPath,
                sendToXPath,
                getShortcutXPath(),
                ...getRecipientXPaths(),
                sendSnapXPath
            ];

            for (const xpath of sequence) {
                if (Array.isArray(xpath)) {
                    for (const singleXPath of xpath) {
                        await clickElementWithRetry(singleXPath, 3, 500);
                    }
                } else {
                    await clickElementWithRetry(xpath, 3, 500);
                }
            }
            snapCount++;
            document.getElementById('snapCounter').textContent = `Snaps Sent: ${snapCount}`;
        }

        // Function to click an element with retry mechanism
        async function clickElementWithRetry(xpath, retries = 3, delay = 500) {
            for (let attempt = 1; attempt <= retries; attempt++) {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    element.click();
                    console.log(`Clicked element at ${xpath}`);
                    return;
                } else {
                    console.log(`Failed to find element at ${xpath}, attempt ${attempt}`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
            console.log(`Failed to click element at ${xpath} after ${retries} attempts`);
            if (xpath === cameraXPath) {
                console.log(`Attempting sleeper action as fallback for camera button`);
                await clickElement(sleeperXPath);
            }
        }

        // Function to run the sequence in a loop
        async function runSequenceLoop() {
            while (loopRunning) {
                await runSequence();
                await waitForElement(cameraXPath);
            }
        }

        // Function to wait for an element to be clickable
        async function waitForElement(xpath, delay = 1000) {
            while (true) {
                const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                if (element) {
                    console.log(`Element at ${xpath} is clickable`);
                    return;
                } else {
                    console.log(`Waiting for element at ${xpath} to be clickable`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }

        // Toggle loop button event listener
        document.getElementById('toggleLoopButton').addEventListener('click', () => {
            loopRunning = !loopRunning;
            document.getElementById('toggleLoopButton').textContent = loopRunning ? 'End Loop' : 'Start Loop';
            if (loopRunning) {
                runSequenceLoop();
            }
        });

        // Toggle night mode button event listener
        document.getElementById('toggleNightModeButton').addEventListener('click', () => {
            nightMode = !nightMode;
            if (nightMode) {
                document.body.requestFullscreen();
                document.body.style.backgroundColor = 'black';
                document.getElementById('rainfall-ui').style.display = 'none';
                const nightModeUI = `
                    <div class="night-mode">
                        <button id="toggleNightModeOffButton">Toggle Off</button>
                        <div id="nightSnapCounter">Snaps Sent: ${snapCount}</div>
                    </div>
                `;
                document.body.insertAdjacentHTML('beforeend', nightModeUI);
                document.getElementById('toggleNightModeOffButton').addEventListener('click', () => {
                    nightMode = false;
                    document.exitFullscreen();
                    document.body.style.backgroundColor = '';
                    document.getElementById('rainfall-ui').style.display = 'flex';
                    document.querySelector('.night-mode').remove();
                });
            } else {
                document.exitFullscreen();
                document.body.style.backgroundColor = '';
                document.getElementById('rainfall-ui').style.display = 'flex';
                document.querySelector('.night-mode').remove();
            }
        });

        // Enhance button click effects
        document.querySelectorAll('.button').forEach(button => {
            button.addEventListener('click', function(e) {
                let x = e.clientX - e.target.offsetLeft;
                let y = e.clientY - e.target.offsetTop;
                
                let ripple = document.createElement('span');
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 1000);
            });
        });

        // Add hover effects
        document.querySelectorAll('.button, #snapCounter').forEach(element => {
            element.addEventListener('mouseover', function() {
                this.style.transform = 'scale(1.05)';
            });
            element.addEventListener('mouseout', function() {
                this.style.transform = 'scale(1)';
            });
        });

        deleteElements();
        hideElements();
        widenElement();
    })();
    """
    driver.execute_script(panel_script)

# Function to initialize and run Selenium WebDriver with error suppression options
def setup_selenium():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_downloads_dir = os.path.join(script_dir, 'tempdownloads')
    os.makedirs(temp_downloads_dir, exist_ok=True)

    path_file = os.path.join(script_dir, 'path.txt')

    try:
        with open(path_file, 'r') as file:
            chrome_driver_path = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file 'path.txt' was not found in the directory {script_dir}. Please ensure it exists.")
        return None

    # Close all existing Chrome instances to avoid conflicts
    try:
        subprocess.call("taskkill /IM chrome.exe /F", shell=True)
    except Exception as e:
        print(f"Error closing Chrome instances: {e}")

    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={os.environ['USERPROFILE']}\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument("--app=https://web.snapchat.com")
    chrome_options.add_argument("--window-size=1174,730")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-infobars")  # Disable infobars
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent Chrome from using /dev/shm
    chrome_options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    chrome_options.add_argument("--disable-background-networking")  # Disable background networking tasks
    chrome_options.add_argument("--disable-background-timer-throttling")  # Disable throttling of timers
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")  # Disable background processing of occluded windows
    chrome_options.add_argument("--disable-client-side-phishing-detection")  # Disable phishing detection
    chrome_options.add_argument("--disable-component-extensions-with-background-pages")  # Disable background extensions
    chrome_options.add_argument("--disable-breakpad")  # Disable crash reporting
    chrome_options.add_argument("--disable-features=Translate,BackForwardCache,WebRTC-HW-Decoding,AutofillServerCommunication")  # Disable extra features
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking to avoid delays
    chrome_options.add_argument("--disable-prompt-on-repost")  # Disable prompts on reposts
    chrome_options.add_argument("--disable-renderer-backgrounding")  # Keeps the renderer process running even if backgrounded
    chrome_options.add_argument("--disable-hang-monitor")  # Disables Chrome's hang monitor
    chrome_options.add_argument("--disable-default-apps")  # Disable default apps
    chrome_options.add_argument("--disable-translate")  # Disable Chrome's built-in translation
    chrome_options.add_argument("--disable-image-loading")  # Disable image loading (improves performance)
    chrome_options.add_argument("--mute-audio")  # Disable sound for reduced resource usage
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": temp_downloads_dir,  # Set to tempdownloads directory
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    })

    # Initialize WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Wait for the page to load
    driver.get("https://web.snapchat.com")
    time.sleep(5)

    # Hide unwanted elements instead of removing them
    hide_element(driver, "/html/body/main/div[1]/div[2]")  # First element
    hide_element(driver, "//div[@class='dg8Lv']")  # Spotlight button

    # Inject custom HTML for the control panel
    inject_control_panel(driver)

    return driver

# Function to clean up tempdownloads directory
def cleanup_temp_downloads(script_dir):
    temp_downloads_dir = os.path.join(script_dir, 'tempdownloads')
    if os.path.exists(temp_downloads_dir):
        for filename in os.listdir(temp_downloads_dir):
            if filename.endswith(".jpeg"):
                file_path = os.path.join(temp_downloads_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

# Main entry point of the script
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    atexit.register(cleanup_temp_downloads, script_dir)

    driver = setup_selenium()
    if driver:
        try:
            while True:
                if not driver.window_handles:
                    print("Browser window closed. Exiting script.")
                    break
                time.sleep(2)
                # Poll for any JavaScript-driven changes in the web app state.
        except KeyboardInterrupt:
            print("Script interrupted by user.")
        finally:
            driver.quit()
            cleanup_temp_downloads(script_dir)
 