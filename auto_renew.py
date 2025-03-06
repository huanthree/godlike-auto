from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 配置浏览器选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# 初始化WebDriver（注意ChromeDriver路径配置）
service = Service(executable_path='/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 访问目标网址
    driver.get('https://godlike.cool/huan')
    
    # 显式等待页面加载
    wait = WebDriverWait(driver, 20)
    
    # Step 1: 勾选人机验证复选框
    checkbox = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@type='checkbox' and preceding-sibling::text()[contains(., '人机身份验证')]]")
    ))
    checkbox.click()
    print("成功勾选人机验证")
    time.sleep(1)  # 等待验证处理
    
    # Step 2: 点击Renew按钮
    renew_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Renew Server')]")
    ))
    renew_btn.click()
    print("成功点击Renew按钮")
    
    # 等待操作完成
    time.sleep(3)

except Exception as e:
    print(f"操作失败: {str(e)}")
    driver.save_screenshot('error_screenshot.png')  # 保存错误截图

finally:
    driver.quit()
