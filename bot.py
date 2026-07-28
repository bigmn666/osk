import os
import requests

def check_price():
    url = "https://api.dexscreener.com/latest/dex/pairs/bsc/0x5a4bbfa871f6cacb80cfffcb04d63f6366c7cb5f"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        pairs = data.get("pairs", [])
        if len(pairs) > 1:
            price_usd = float(pairs[1]["priceUsd"])
        else:
            price_usd = float(pairs[0]["priceUsd"])
            
        print(f"当前获取到价格: {price_usd} USD")
        
        # 测试期间：只要价格大于 0 就必定会发一条微信，用来验证推送通不通
        if price_usd > 0:
            send_wechat(
                f"🚨 价格测试通知\n\n当前代币价格为：{price_usd} USD，本消息来自GitHub Actions", 
                f"🚨 当前价格测试:{price_usd}"
            )
            
    except Exception as e:
        print(f"请求出错: {e}")

def send_wechat(content, summary):
    wx_url = "https://wxpusher.zjiecode.com/api/send/message"
    
    # 严格对应你在 GitHub 里添加的 Secret 名字（全大写 WXPUSHER_TOKEN）
    app_token = os.getenv("WXPUSHER_TOKEN")
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
