"""
今日句子

抓任意包请求头 token
变量名: JRJZ_TOKEN

cron: 35 7 * * *
const $ = new Env("今日句子");
---------------------------------------------
20240706 取消发布句子重复度校验，改为直接发布
20240701 频繁调用会出现滑块验证，取消鸡肋助力
20240625 助力废了,单账号每天一次变为每月一次,没有维护的必要了
---------------------------------------------
"""
import os
import random
import re
import time
import requests
from urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning
from common import qianwen_messages, make_request, daily_one_word, get_163music_comments, save_result_to_file

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)


class JRJZ():
    name = "今日句子"

    def __init__(self, token):
        self.token = token
        self.openid = ''
        self.money = 0
        self.headers = {
            'Host': 'api.juzi.co',
            'Connection': 'keep-alive',
            'token': token,
            'content-type': 'application/json',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.49(0x18003137) NetType/WIFI Language/zh_CN',
            'Referer': 'https://servicewechat.com/wx3e3540cb2012ea1f/27/page-frame.html',
        }

    def user_status_verify(self):
        response = requests.get('https://api.juzi.co/index/getCaptcha', headers=self.headers)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            return True
        response_json = response.json()
        if response_json['code'] == 200:
            save_result_to_file("success", self.name)
            msg = "需要进行安全验证"
            print(msg)
            return False
        elif response_json['code'] == 202:
            msg = "无需进行安全验证"
            print(msg)
            return False
        else:
            save_result_to_file("error", self.name)
            msg = "状态异常"
            print(msg)
            return True

    def user_info(self):
        response = requests.get('https://api.juzi.co//member/getWalletInfo', headers=self.headers)
        print(response.text)
        print(response.text)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            return None
        response_json = response.json()
        if response_json['code'] == 200:
            save_result_to_file("error", self.name)
            money = f'{response_json["data"]["member"]["money"]}'
            openid = response_json['data']["member"]["openid"]
            nickName = response_json["data"]["member"]["nickname"]
            self.money = money
            self.openid = openid
            print(f'🐹昵称：{response_json["data"]["member"]["nickname"]}')
            print(f'🐶余额：{response_json["data"]["member"]["money"]}')
            print(f'🐱句子数量：{response_json["data"]["member"]["juzi_count"]}')
            print(f'---------------------------')
            return nickName, openid
        else:
            save_result_to_file("error", self.name)
            return None

    def get_no_repeat_sentence(self):
        time.sleep(random.randint(20, 30))
        quote = ''
        ids = [1, 2]
        if random.choice(ids) == 1:
            print("🐱句子来源 | 【每日一句】")
            quote = daily_one_word()
        elif random.choice(ids) == 2:
            print("🐱句子来源 | 【网易云音乐热评】")
            quote = get_163music_comments()
        if not quote:
            return None
        else:
            return quote

        # while True:
        #     time.sleep(random.randint(20, 30))
        #     quote = ''
        #     ids = [2]
        #     if random.choice(ids) == 1:
        #         print("🐱句子来源 | 【每日一句】")
        #         quote = daily_one_word()
        #     elif random.choice(ids) == 2:
        #         print("🐱句子来源 | 【网易云音乐热评】")
        #         quote = get_163music_comments()
        #     if not quote:
        #         continue
        #     data = {'juzi': quote}
        #     print(f"data: {data}")
        #     url = 'https://api.juzi.co/sentence/repeatedList'
        #     response = requests.post(url, headers=self.headers, json=data)
        #     print(response.text)
        #     if response.status_code != 200:
        #         continue
        #     response_json = response.json()
        #     if response_json['code'] != 200:
        #         continue
        #     sentences = response_json.get('data', [])
        #     if len(sentences) <= 0 and len(quote) >= 10:
        #         return quote
        #     else:
        #         print(f"⛔️句子重复， 已有{len(sentences)}人发布，跳过......")
        #         continue

    def write_sentence(self):
        quote = self.get_no_repeat_sentence()
        print(f"🐹开始发布句子: {quote}")
        if quote is not None:
            json_data = {
                'juzi': quote,
                'original': 'false',
                'writer': '',
                'source': '',
                'tagsValue': '随笔',
                'tagslength': '0',
                'tags': '随笔',
            }
            url = 'https://api.juzi.co/sentence/execWrite'
            response = requests.post('https://api.juzi.co/sentence/execWrite', headers=self.headers, json=json_data)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json and response_json['code'] == 200:
                    print(f'✅今日句子发布成功')
                else:
                    print(f'❌今日句子发布失败 | {response_json["msg"]}')
            else:
                print(f'❌今日句子发布失败：{response.text}')
        else:
            print(f'❌今日句子发布失败, 取消发布')

    def my_info(self):
        response = requests.get('https://api.juzi.co//member/getWalletInfo', headers=self.headers)
        print("1111111111111==", response.text)
        if not response or response.status_code != 200:
            return None
        response_json = response.json()
        if response_json['code'] == 200:
            money = f'{response_json["data"]["member"]["money"]}'
            openid = response_json['data']["member"]["openid"]
            nickName = response_json["data"]["member"]["nickname"]
            self.money = money
            self.openid = openid
            # print(f'🐹昵称：{response_json["data"]["member"]["nickname"]}')
            # print(f'🐶余额：{response_json["data"]["member"]["money"]}')
            # print(f'🐱句子数量：{response_json["data"]["member"]["juzi_count"]}')
            # print(f'---------------------------')
            return nickName, openid
        else:
            save_result_to_file("error", self.name)
            return None

    def person_first_sentence(self, openid):
        params = {
            'openid': openid,  # 用户的openid
            'page': '1',
        }
        try:
            response = requests.get('https://api.juzi.co/member/index', params=params, headers=self.headers, )
            response.raise_for_status()
            response_json = response.json()
            if response_json['code'] != 200:
                return None
            sentences = response_json['data'].get("sentenceAll", [])
            if not sentences:
                return None
            for sentence in sentences:
                if sentence["checkResult"] == "":
                    return sentence
            return None
        except requests.RequestException as e:
            print(f"获取句子列表失败: {e}")
            return None

    def sentence_like(self, sid, nickName):
        data = {
            'sid': sid,
        }
        response = requests.post('https://api.juzi.co/sentence/slike', headers=self.headers, data=data)
        if not response or response.status_code != 200:
            return
        response_json = response.json()
        if response_json['code'] == 200:
            print(f'❤️【{nickName}】对句子【{sid}】点了赞 | {response_json["msg"]}')
        else:
            print("❌点赞失败 | ", response_json["msg"])

    def sentence_comment(self, sid):
        quote = daily_one_word()
        if quote is not None:
            data = {
                'content': quote,
                'pid': '0',
                'sid': sid,
            }
            url = 'https://api.juzi.co/sentence/addComments'
            response = requests.post(url, headers=self.headers, data=data)
            if response and response.status_code == 200:
                response_json = response.json()
                if response_json['code'] == 200:
                    print(f'对句子{sid}做了评论 | {response_json["msg"]}')

    def sentence_share(self, sid, share_user_id):
        params = {
            'openid': sid,  # 句子详情的openid | '165fccff78fb3d6021f279ced2d5cf93'
            'share': share_user_id,  # 发起分享的用户openid | 'd37850c6d0383eac5edeba21b6e89cf4'
        }
        response = requests.get('https://api.juzi.co/sentence/makePic', params=params, headers=self.headers)
        print(response.text)

    def sentence_detail(self, sid):
        params = {
            'openid': sid,  # 句子详情的openid # '4225a8430480a2176a6ffeb36c3caf17'
        }
        response = requests.get('https://api.juzi.co/sentence/detail', params=params, headers=self.headers)
        print(response.text)

    def sentence_share_callback(self, sid):
        # https://api.juzi.co/sentence/makePic?openid=165fccff78fb3d6021f279ced2d5cf93&share=d37850c6d0383eac5edeba21b6e89cf4
        data = {
            'user_openid': self.openid,  # 分享者的openid， url中share对应的值
            'code': '0e3scs200mechS12rE300dxRKi1scs2e',
            'provider': 'weixin',
            'sentence_id': sid,  # 句子信息的openid  # '4225a8430480a2176a6ffeb36c3caf17'
        }
        response = requests.post('https://api.juzi.co//sentence/picShareCallback', headers=self.headers, data=data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'分享回调成功 | {response_json["msg"]}')

    def cashout(self):
        print(f'---------------------------')
        print(f'💰余额：{self.money}元, 满足提现条件，开始提现......')
        data = {
            'price': '3',
        }
        response = requests.post('https://api.juzi.co/member/cashOut', headers=self.headers, data=data)
        if response and response.status_code == 200:
            response_json = response.json()
            if response_json['code'] == 200:
                print(f'提现成功 | {response_json["msg"]}')
            elif response_json['code'] == 202:
                print(f'余额不足')
            else:
                print(f'提现失败 | {response_json["msg"]}')

    def assist(self, tokens):
        """
        1、句子被点赞
        2、分享被浏览
        3、发布新句子
        """
        # 用户是否点赞字典
        users_liked = {token: False for token in tokens}
        sentence_openids = []
        for token in tokens:
            jrjz_instance = JRJZ(token)
            nickName, openid = jrjz_instance.my_info()
            first_sentence = jrjz_instance.person_first_sentence(openid)
            if first_sentence:
                sentence_openids.append(first_sentence["id"])
        for sid in sentence_openids:
            print(f"\n======== ▷ EveryBody开始为句子【{sid}】助力 ◁ ========")
            for token in tokens:
                if token != self.token:
                    if not users_liked[token]:
                        jrjz_instance = JRJZ(token)
                        nickName, openid = jrjz_instance.my_info()

                        # 长按图片识别浏览
                        jrjz_instance.sentence_share_callback(sid)
                        time.sleep(random.randint(20, 30))

                        # 点赞|每个用户每天只能给其他人点赞一次
                        jrjz_instance.sentence_like(sid, nickName)
                        users_liked[token] = True
                        time.sleep(random.randint(20, 30))
                    else:
                        print(f'✈️【{nickName}】今天已经点过赞了, 跳过')
                        continue
                else:
                    print(f'✈️自己不能给自己点赞, 跳过')

    # 作品列表
    def ck_check(self):
        print(f'---------------- 用户CK检测 ----------------')
        params = {
            'page': '1',
            'type': 'source',
        }
        response = requests.get('https://api.juzi.co/album/indexList', params=params, headers=self.headers)
        if not response or response.status_code != 200:
            save_result_to_file("error", self.name)
            print("❌CK异常 | ", response.text)
            return False
        response_json = response.json()
        if response and response.status_code == 200:
            save_result_to_file("error", self.name)
            print("CK正常")
            return True
        else:
            save_result_to_file("error", self.name)
            print("❌CK异常 | ", response_json["msg"])
            return False

    def main(self):
        """
        1、发布句子奖励标准：发布句子且审核通过随机0.3元左右，每天奖励1条
        """
        # self.user_status_verify()
        if not self.user_status_verify():
            # 发布句子
            print("开始发布句子......")
            self.write_sentence()
            time.sleep(random.randint(30, 60))

            # 提现
            if float(self.money) >= 3.0:
                self.cashout()
            else:
                print(f'---------------------------')
                print(f'💰余额不足，跳过提现 | 当前余额：{self.money}元')
        else:
            print("需要进行安全验证，取消发布")


if __name__ == '__main__':
    env_name = 'JRJZ_TOKEN'
    tokenStr = os.getenv(env_name)
    if not tokenStr:
        print(f'⛔️未获取到ck变量：请检查变量 {env_name} 是否填写')
        exit(0)
    tokens = re.split(r'&', tokenStr)
    print(f"今日句子共获取到{len(tokens)}个账号")
    for i, token in enumerate(tokens, start=1):
        print(f"\n======== ▷ 第 {i} 个账号 ◁ ========")
        jrjz_instance = JRJZ(token)
        jrjz_instance.main()
        # if i == len(tokens):
        #     jrjz_instance.assist(tokens)
        print("\n【日常任务】随机等待30-60s进行下一个账号")
        time.sleep(random.randint(10, 15))
        print("----------------------------------")
