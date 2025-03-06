import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class HuanRenewer:
    def __init__(self):
        self.driver = self.setup_driver()
        
    def setup_driver(self):
        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--mute-audio")
        
        # 重要：使用undetected_chromedriver绕过Cloudflare检测
        driver = uc.Chrome(
            options=options,
            version_main=114  # 匹配最新稳定版Chrome
        )
        return driver

    def solve_captcha(self):
        """处理人机验证核心逻辑"""
        try:
            # 切换到验证iframe（关键步骤）
            WebDriverWait(self.driver, 20).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[title*='验证']")
                )
            )
            
            # 定位验证复选框
            checkbox = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, ".recaptcha-checkbox-border")
                )
            )
            checkbox.click()
            print("已触发人机验证流程...")
            
            # 处理可能的图像验证
            self.handle_image_verification()
            
        except Exception as e:
            print(f"验证失败: {str(e)}")
            self.driver.save_screenshot('captcha_error.png')
        finally:
            self.driver.switch_to.default_content()

    def handle_image_verification(self):
        """处理二级图像验证（如有触发）"""
        try:
            # 等待图像验证框出现
            image_frame = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "iframe[title='验证挑战']")
                )
            )
            
            # 点击验证按钮（示例定位器，需根据实际调整）
            verify_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "verify-button"))
            )
            verify_btn.click()
            print("已完成图像验证")
            
        except Exception as e:
            print(f"图像验证处理异常: {str(e)}")
            # 备用方案：自动重试或记录日志

    def renew_server(self):
        try:
            self.driver.get("https://godlike.cool/huan")
            
            # 第一阶段：处理人机验证
            self.solve_captcha()
            
            # 等待验证完成
            time.sleep(5)  # 重要：等待验证状态更新
            
            # 第二阶段：执行续订操作
            renew_btn = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Renew Server')]")
                )
            )
            renew_btn.click()
            print("服务器续订请求已发送")
            
            # 验证操作结果
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, ".success-message")
                )
            )
            print("续订成功！")
            
        except Exception as e:
            print(f"操作失败: {str(e)}")
            self.driver.save_screenshot('renew_error.png')
        finally:
            self.driver.quit()

if __name__ == "__main__":
    renewer = HuanRenewer()
    renewer.renew_server()
