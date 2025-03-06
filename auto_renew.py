import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import time

class RenewAutomation:
    def __init__(self):
        self.driver = self.setup_driver()
        self.wait = WebDriverWait(self.driver, 25)
        
    def setup_driver(self):
        options = uc.ChromeOptions()
        
        # 路径配置优化
        options.binary_location = os.getenv('CHROME_PATH', '/usr/bin/chromium-browser')
        driver_executable_path = os.getenv('CHROMEDRIVER_PATH', '/usr/bin/chromedriver')
        
        # 权限配置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        
        if os.getenv('HEADLESS_MODE', 'false').lower() == 'true':
            options.add_argument("--headless=new")
            
        # 使用用户级临时目录
        user_data_dir = "/home/runner/chrome_profile"
        options.add_argument(f"--user-data-dir={user_data_dir}")
        
        return uc.Chrome(
            options=options,
            driver_executable_path=driver_executable_path,
            version_main=114
        )

    def handle_captcha(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # 优化iframe切换逻辑
            iframe = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='验证']"))
            )
            self.driver.switch_to.frame(iframe)
            
            # 添加显式等待确保元素加载
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".recaptcha-checkbox"))
            )
            checkbox.click()
            
            # 验证状态检测优化
            self.wait.until(
                lambda d: "aria-checked" in checkbox.get_attribute("outerHTML")
            )
            
        except Exception as e:
            print(f"验证处理失败: {str(e)}")
            self.driver.save_screenshot('captcha_error.png')
            raise
        finally:
            self.driver.switch_to.default_content()

    def perform_renew(self):
        try:
            self.driver.get("https://godlike.cool/huan")
            self.handle_captcha()
            
            renew_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Renew Server')]"))
            )
            renew_button.click()
            
            # 添加结果验证
            self.wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".success-indicator"))
            )
            print("续订操作成功完成")
            
        except Exception as e:
            print(f"操作失败: {str(e)}")
            self.driver.save_screenshot('operation_error.png')
            raise
        finally:
            self.driver.quit()

if __name__ == "__main__":
    automator = RenewAutomation()
    automator.perform_renew()
