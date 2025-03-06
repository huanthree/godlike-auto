import sys
import io
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

TARGET_URLS = [
    "https://stream4lit-l89x9uaknyuyndksxqvatx.streamlit.app/",
    "https://fool4stream-xr8trzmsvvm9yfbecdqtuz.streamlit.app/"
]

def take_screenshot(driver, name):
    """保存调试截图"""
    driver.save_screenshot(f"{name}.png")
    print(f"已保存截图：{name}.png")

def process_url(url):
    print(f"\n正在处理URL: {url}")
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")  # 固定窗口尺寸

    try:
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(45)
        driver.get(url)
        take_screenshot(driver, "page_loaded")

        # 增强元素定位策略
        button_locator = (By.XPATH, 
            "//button[contains(translate(normalize-space(.), ' ', ''), 'Yes,getthisappbackup!')]")  # 忽略空格和大小写

        wait = WebDriverWait(driver, 20)
        button = wait.until(EC.presence_of_element_located(button_locator))
        
        # 滚动到元素可视区域
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(1)  # 等待滚动完成
        take_screenshot(driver, "after_scroll")

        # 双重验证元素可点击
        wait.until(EC.element_to_be_clickable(button_locator))
        
        # 使用ActionChains模拟真实点击
        ActionChains(driver).move_to_element(button).pause(0.5).click().perform()
        print("执行点击动作")
        take_screenshot(driver, "after_click")

        # 验证点击结果（根据页面实际情况调整）
        try:
            wait.until(EC.invisibility_of_element(button_locator))
            print("按钮状态变化验证成功")
            return True
        except TimeoutException:
            print("警告：按钮状态未发生预期变化")
            return False

    except TimeoutException as e:
        print("状态正常：未找到需要点击的按钮")
        take_screenshot(driver, "no_button_found")
        return True
    except Exception as e:
        print(f"操作异常：{type(e).__name__} - {str(e)}")
        take_screenshot(driver, "error_occurred")
        return False
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    success_count = 0
    
    for index, url in enumerate(TARGET_URLS, 1):
        print(f"\n{'='*30}")
        print(f"处理进度：{index}/{len(TARGET_URLS)}")
        result = process_url(url)
        if result:
            success_count += 1
        time.sleep(3)  # 间隔防止请求过频
    
    print(f"\n最终结果：成功处理 {success_count}/{len(TARGET_URLS)} 个应用")
