import logging
import random

import requests
from playwright import sync_api

from src import config


def run() -> int:
    # 执行签到任务
    autoSignIn()
    logging.info("已完成签到任务")

    # 执行评论任务
    autoCommit()
    logging.info("已完成评论任务")

    logging.info("任务完成")
    return 1


def autoSignIn() -> None:
    logging.info("正在执行签到任务")
    with sync_api.sync_playwright() as pw:
        # 打开网页
        browser = pw.chromium.launch(headless=True)
        logging.info("已启动浏览器")

        viewport = sync_api.ViewportSize(width=1920, height=1080)
        storage_state = sync_api.StorageState(
            {
                "cookies": [
                    {
                        "name": "PHPSESSID",
                        "value": config.topfeel_session_id,
                        "domain": ".topfeel.com",
                        "path": "/",
                    }
                ],
                "origins": [
                    {
                        "origin": "https://bbs.topfeel.com",
                        "localStorage": [
                            {
                                "name": "token",
                                "value": config.topfeel_access_token,
                            }
                        ],
                    }
                ],
            }
        )
        context = browser.new_context(viewport=viewport, storage_state=storage_state)
        logging.info("已创建上下文")

        page = context.new_page()
        logging.info("已创建新页面")

        # 前往签到页面
        page.goto(
            "https://bbs.topfeel.com/h5/#/minePages/qiandao",
            wait_until="networkidle",
            timeout=30_000,
        )
        logging.info("已前往签到页面")

        # 检查是否未登录
        if page.locator(".login-tips-block").is_visible():
            raise Exception("未登录，无法签到")
        logging.info("已登录，即将进行签到")

        # 检查是否已签到
        if page.locator("uni-button:has(> .yiqian)"):
            logging.info("已签到，无需重复签到")
            return
        logging.info("未签到，即将进行签到")

        # 加载并点击签到按钮
        sign_btn = page.locator("uni-button:has(> .weiqian)")
        sign_btn.wait_for(state="visible", timeout=5_000)
        logging.info("已加载签到按钮")

        sign_btn.click()
        logging.info("已点击签到按钮")

        # 等待滑块并完成验证
        page.locator(".zmm-slider-verify-title").wait_for(state="visible", timeout=5_000)
        logging.info("已弹出滑块弹框")

        touch_block = page.locator(".zmm-slider-verify-block-touch").bounding_box()
        verify_block = page.locator(".zmm-slider-verify-block-verify").bounding_box()
        logging.info("已出现滑动方块和验证方块")

        center_x = touch_block["x"] + touch_block["width"] / 2
        center_y = touch_block["y"] + touch_block["height"] / 2
        target_x = verify_block["x"] + verify_block["width"] / 2
        target_y = verify_block["y"] + verify_block["height"] / 2

        mouse = page.mouse
        mouse.move(center_x, center_y)
        mouse.down()
        logging.info("已移动到滑动方块并按下鼠标左键")

        mouse.move(target_x, target_y, steps=20)
        mouse.up()
        logging.info("已移动到验证方块并松开鼠标左键")


def autoCommit() -> None:
    logging.info("正在执行评论任务")

    # 随机选择评论模板
    tpl_comments = ["日赚一分", "加油加油", "快了快了", "积分快涨"]
    random_comment = random.choice(tpl_comments)
    logging.info(f"已随机选择评论模板：{random_comment}")

    # 随机选择评论帖子
    tpl_posts = ["923", "917"]
    random_post = random.choice(tpl_posts)
    logging.info(f"已随机选择评论帖子：{random_post}")

    # 发送请求提交评论
    url = "https://bbs.topfeel.com/api/user/addGoodsComment"
    headers = {
        "content-type": "application/json",
        "referer": "https://bbs.topfeel.com/h5/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
        "token": config.topfeel_access_token,
    }
    data = {
        "images": "",
        "goods_id": random_post,
        "vocdec": 0, "voc": "",
        "content": random_comment,
        "pid": 0,
        "to_name": ""
    }
    response = requests.post(url, headers=headers, json=data)
    logging.info(f"已发送请求提交评论，状态码：{response.status_code}")
