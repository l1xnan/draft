import json
import requests



data = {
    "r": json.dumps({
        "to": 2409924115,
        "content": json.dumps([
            '你好',
            ["font", {"name": "宋体", "size": 10,
                      "style": [0, 0, 0], "color": "000000"}],
        ]),
        "face": 603,
        "clientid": 53999199,
        "msg_id": 27240001,
         "psessionid": "8368046764001d636f6e6e7365727665725f77656271714031302e3133332e34312e383400001ad00000066b026e040015808a206d0000000a406172314338344a69526d0000002859185d94e66218548d1ecb1a12513c86126b3afb97a3c2955b1070324790733ddb059ab166de6857"})}

headers = {"Host": "d1.web2.qq.com",
           "Connection": "keep-alive",
           "Content-Length": "601",
           "Pragma": "no-cache",
           "Cache-Control": "no-cache",
           "Origin": "http://d1.web2.qq.com",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
           "Content-Type": "application/x-www-form-urlencoded",
           "Accept": "*/*",
           "Referer": "http://d1.web2.qq.com/proxy.html?v=20151105001&callback=1&id=2",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
           "Cookie": "tvfe_boss_uuid=2b4274444c68ce40; pac_uid=1_1286967493; ptui_loginuin=l1xnan@qq.com; pgv_pvi=4268167168; pgv_si=s5631590400; ptcz=df1efd94d0c301b0653d2c6b91c5bb0c4c47406161cc635342bc770d26a9cc79; rv2=8037A8CC661BC615AA988F59410FC4D7661829317AE5A23975; property20=D0A8D3EEAC014E0E057B437B96722BB3002BAB9A510F7CB0E463DC36CBCE2771C68C28E50249300B; ptisp=ctc; RK=e+GTzUwjTz; pt2gguin=o1286967493; uin=o1286967493; skey=@qYNwiXVeO; p_uin=o1286967493; p_skey=jd62UfEDb*88gRix2U2Q-bFcm589ZDu4LpQ0AL-rX5w_; pt4_token=nvL4bdDHWHw4ZRK5M9xek3Q3uQEOxz3BglvsCCuaUTs_; pgv_info=ssid=s253427800; pgv_pvid=9987491960; o_cookie=1286967493; ptwebqq=732be4547c83c76f8d4b5bcd1cb02b77cd660b8b66a7bb115351a63cd989fd1e", }


# url = 'http://d1.web2.qq.com/channel/send_buddy_msg2'
# req = requests.post(url, data=data, headers=headers)
# req.text

# req.text

url_get_msg = 'http://d1.web2.qq.com/channel/poll2'
data_get_msg = {
    "r": json.dumps({
        "ptwebqq":"732be4547c83c76f8d4b5bcd1cb02b77cd660b8b66a7bb115351a63cd989fd1e",
        "clientid":53999199,"psessionid":"8368046764001d636f6e6e7365727665725f77656271714031302e3133332e34312e383400001ad00000066b026e040015808a206d0000000a406172314338344a69526d0000002859185d94e66218548d1ecb1a12513c86126b3afb97a3c2955b1070324790733ddb059ab166de6857",
        "key":"",
    })
}
req_get_msg = requests.post(url_get_msg,data =data_get_msg, headers = headers )

req_get_msg.text

req_get_msg.text