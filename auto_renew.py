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
        
        # 增强型无头模式配置
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        
        if os.getenv('HEADLESS_MODE', 'false').lower() == 'true':
            options.add_argument("--headless=new")
            
        # 用户代理随机化
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        ]
        options.add_argument(f"user-agent={user_agents[0]}")
        
        return uc.Chrome(
            options=options,
            version_main=114,
            driver_executable_path="/usr/bin/chromedriver"
        )

    def handle_captcha(self):
        """优化的人机验证处理流程"""
        try:
            # 显式等待页面加载完成
            self.wait.until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            
            # 切换到验证框架
            self.driver.switch_to.frame(
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[title*='验证']"))
                )
            )
            
            # 等待复选框可点击
            checkbox = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".recaptcha-checkbox"))
            )
            
            # 使用动作链模拟人类点击
            action = webdriver.ActionChains(self.driver)
            action.move_to_element(checkbox).pause(1).click().perform()
            
            # 验证状态检测
            self.wait.until(
                lambda d: d.find_element(By.CSS_SELECTOR, ".recaptcha-checkbox").get_attribute("aria-checked") == "true"
            )
            
        except Exception as e:
            print(f"验证处理失败: {str(e)}")
            self.driver.save_screenshot('captcha_error.png')
            raise
        finally:
            self.driver.switch_to.default_content()
            time.sleep(2)

    def perform_renew(self):
        try:
            self.driver.get("https://godlike.cool/huan")
            
            # 处理人机验证
            self.handle_captcha()
            
            # 点击续订按钮
            renew_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Renew Server')]"))
            )
            renew_button.click()
            
            # 验证操作结果
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "body"),
                    "success"
                )
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
