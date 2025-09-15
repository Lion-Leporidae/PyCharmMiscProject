import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from sqlalchemy import false

# 本地驱动路径（修改为你的实际路径）
CHROMEDRIVER_PATH = "chromedriver-win64/chromedriver-win64/chromedriver.exe"

# 配置信息
CONFIG = {
    "login_url": "http://172.19.0.5/srun_portal_pc?ac_id=17&clientip=10.161.91.33&clientmac=10%3Af6%3A0a%3Aa8%3Acd%3A66&iarmdst=www.msftconnecttest.com%2Fredirect&paip=10.99.99.99&theme=cucc&vlan=0.0&wlanacname=Panabit&wlanuserip=10.161.91.33",
    "username": "202300202132",
    "password": "lyx113.04",
    "check_interval": 10,       # 每30秒检查网络状态
    "max_retries": 3,           # 登录失败最多重试3次
    "headless": True           # True 无头运行，False 可视化调试
}

def check_internet():
    """检查网络是否连接"""
    try:
        return requests.get("https://www.baidu.com/", timeout=10).status_code == 200
    except:
        return False

def auto_login():
    """执行登录流程"""
    options = webdriver.ChromeOptions()
    if CONFIG["headless"]:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    try:
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(20)

        driver.get(CONFIG["login_url"])

        # 输入用户名
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_input.clear()
        username_input.send_keys(CONFIG["username"])

        # 输入密码
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_input.clear()
        password_input.send_keys(CONFIG["password"])

        # 勾选协议
        # protocol_checkbox = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "protocol"))
        # )
        # if not protocol_checkbox.is_selected():
        #     protocol_checkbox.click()

        # 点击登录按钮
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-account"))
        )
        login_button.click()

        time.sleep(3)
        if check_internet():
            print("✅ 登录成功，网络已恢复")
            return True
        else:
            print("⚠️ 登录操作已完成，但网络未恢复")
            return False

    except (WebDriverException, TimeoutException) as e:
        print(f"❌ 登录失败: {type(e).__name__} - {str(e)}")
        return False

    finally:
        try:
            driver.quit()
        except:
            pass

def main():
    while True:
        try:
            if not check_internet():
                print("检测到断网，开始自动登录...")

                for attempt in range(CONFIG["max_retries"]):
                    print(f"第 {attempt + 1} 次尝试登录")
                    if auto_login():
                        break
                    time.sleep(10)
                else:
                    print("⚠️ 多次尝试登录失败")

            else:
                print("网络连接正常")

            time.sleep(CONFIG["check_interval"])

        except KeyboardInterrupt:
            print("\n🛑 程序已手动终止")
            break

if __name__ == "__main__":
    main()


