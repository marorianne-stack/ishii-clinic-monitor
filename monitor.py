from playwright.sync_api import sync_playwright
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

LINE_USER_ID = os.getenv("LINE_USER_ID")
LINE_ACCESS_TOKEN = os.getenv("LINE_ACCESS_TOKEN")
def send_line(message):
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    print("LINE送信結果:", response.status_code, response.text)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://patient.digikar-smart.jp/institutions/41e9afbb-777b-4052-b928-df75cf7cb74a/reserve")
    page.get_by_role("button", name="ジュベルックボリューム（医師手打ち・局所麻酔込み）").click()
    page.get_by_text("初診").click()
    page.get_by_role("button", name="次へ").click()
    page.get_by_text("予約日時を選択してください").wait_for()
    page.locator("td button").first.wait_for(timeout=60000)
    print(page.title())

    
    buttons = page.locator("td button")
    print("td内buttonの数 =", buttons.count())

    x_path = buttons.locator("svg path").first.get_attribute("d")
    notified = False
    while True:
        found = False

        buttons = page.locator("td button")

        for i in range(buttons.count()):
            b = buttons.nth(i)
            text = b.inner_text().strip()
            svg = b.locator("svg")

            if svg.count() == 0:
                continue

            path = svg.locator("path").first.get_attribute("d")

        if True
            print("★空き候補！", i, "文字=", repr(text))

            if not notified:
                for _ in range(10):
                    send_line("石井クリニックに空き候補が出ました！予約ページを確認してね")
                    time.sleep(60)
                notified = True

            found = True

        if not found:
            print("空きなし")
            notified = False

        print("30秒後に再チェックします")
        time.sleep(30)

        page.reload()

        page.get_by_text("予約日時を選択してください").wait_for()
        page.locator("td button").first.wait_for(timeout=60000)
