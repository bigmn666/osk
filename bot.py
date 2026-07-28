import os
import requests

def check_price():
    # 1. 请求 Dexscreener 获取价格数据
    url = "https://api.dexscreener.com/latest/dex/pairs/bsc/0x5a4bbfa871f6cacb80cfffcb04d63f6366c7cb5f"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 获取价格
        pairs = data.get("pairs", [])
        if len(pairs) > 1:
            price_usd = float(pairs[1]["priceUsd"])
        else:
            price_usd = float(pairs[0]["priceUsd"]) # 防止数组越界兜底
            
        print(f"当前获取到价格: {price_usd} USD")
        
        # 2. 条件判断与微信推送逻辑
        if price_usd > 100:
            send_wechat(
                f"🚨 价格预警通知（高位突破）\n\n当前代币价格已升至为：{price_usd} USD，本消息来自GitHub Actions", 
                f"🚨🚨🚨 当前价格:{price_usd}🚨价格升至 100 以上🚨🚨🚨"
            )
        elif price_usd < 40:
            send_wechat(
                f"⚠️ 价格预警通知（跌破警戒线）\n\n当前代币价格已跌至：{price_usd} USD，本消息来自GitHub Actions", 
                f"⚠️⚠️⚠️ 当前价格: {price_usd} 跌至 40 以下 ⚠️⚠️⚠️"
            )
            
    except Exception as e:
        print(f"请求出错: {e}")

def send_wechat(content, summary):
    wx_url = "https://wxpusher.zjiecode.com/api/send/message"
    
    # 从 GitHub Secrets 环境变量中读取配置
    app_token = os.getenv("WX_APP_TOKEN")
    uid_1 = os.getenv("WX_UID_1")
    uid_2 = os.getenv("WX_UID_2")

    payload = {
        "appToken": app_token,
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": [uid_1, uid_2]
    }
    res = requests.post(wx_url, json=payload)
    print("微信推送结果:", res.text)

if __name__ == "__main__":
    check_price()
