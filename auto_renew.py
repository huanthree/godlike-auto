from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

class RenewAutomation:
    def __init__(self):
        self.driver = self.setup_driver()
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        if os.getenv('HEADLESS_MODE', 'false').lower() == 'true':
            options.add_argument("--headless=new")
            
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        service = webdriver.ChromeService(
            executable_path=ChromeDriverManager().install()
        )
        
        return webdriver.Chrome(service=service, options=options)

    def handle_captcha(self):
        """处理人机验证的CI优化方案"""
        try:
            # 切换到验证框架
            WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[title*='验证']")
                )
            )
            
            # 执行JavaScript点击（绕过点击检测）
            self.driver.execute_script(
                "document.querySelector('.recaptcha-checkbox').click()"
            )
            
            # 验证通过检测
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".recaptcha-checkbox-checked")
                )
            )
            
        except Exception as e:
            print(f"验证处理失败: {str(e)}")
            self.driver.save_screenshot('captcha_failure.png')
            raise
        finally:
            self.driver.switch_to.default_content()

    def perform_renew(self):
        try:
            self.driver.get("https://godlike.cool/huan")
            
            # 处理人机验证
            self.handle_captcha()
            
            # 点击续订按钮
            renew_button = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Renew Server')]")
                )
            )
            self.driver.execute_script("arguments[0].click();", renew_button)
            
            # 验证操作结果
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".success-indicator")
                )
            )
            print("续订操作成功完成")
            
        except Exception as e:
            print(f"操作失败: {str(e)}")
            self.driver.save_screenshot('operation_failure.png')
            raise
        finally:
            self.driver.quit()

if __name__ == "__main__":
    automator = RenewAutomation()
    automator.perform_renew()
