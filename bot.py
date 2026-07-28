import requests

def check_price():
    # 1. 请求 Dexscreener 获取价格数据
    url = "https://api.dexscreener.com/latest/dex/pairs/bsc/0x5a4bbfa871f6cacb80cfffcb04d63f6366c7cb5f"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        
        # 获取价格（对应你原本的 pairs[1].priceUsd）
        pairs = data.get("pairs", [])
        if len(pairs) > 1:
            price_usd = float(pairs[1]["priceUsd"])
        else:
            price_usd = float(pairs[0]["priceUsd"]) # 防止数组越界兜底
            
        print(f"当前获取到价格: {price_usd} USD")
        
        # 2. 条件判断与微信推送逻辑
        # 对应你原本路由中的判断条件
        # 3D 价格条件判断与微信推送逻辑
        if price_usd > 100:
            # 大于 100 时的提示
            send_wechat(
                f"🚨 价格预警通知（高位突破）\n\n当前代币价格已升至为：{price_usd} USD，本消息来自mac-docker", 
                f"🚨🚨🚨 当前价格:{price_usd}🚨价格升至 100 以上🚨🚨🚨"
            )
        elif price_usd < 40:
            # 小于 40 时的提示
            send_wechat(
                f"⚠️ 价格预警通知（跌破警戒线）\n\n当前代币价格已跌至：{price_usd} USD本消息来自mac-docker", 
                f"⚠️⚠️⚠️ 当前价格: {price_usd} 跌至 40 以下 ⚠️⚠️⚠️"
            )
            
    except Exception as e:
        print(f"请求出错: {e}")

def send_wechat(content, summary):
    # WxPusher 推送接口
    wx_url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": "AT_3Z8xtKdx7rHb2NxBdCV2rJr5K8SAa4zi",
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": [
            "UID_SkGWz0MxDpsC7x83MEknBFx8GXzk",
            "UID_Le64zRgq2tEO64GQgkkMiK5A0mWP"
        ]
    }
    res = requests.post(wx_url, json=payload)
    print("微信推送结果:", res.text)

if __name__ == "__main__":
    check_price()