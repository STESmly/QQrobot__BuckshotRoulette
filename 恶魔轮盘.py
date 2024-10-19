import asyncio
from nonebot import on_command, on_keyword
from nonebot.adapters.qq import Message, MessageEvent, MessageSegment, Bot, GroupAddRobotEvent, GroupRobotEvent, GroupDelRobotEvent, MessageCreateEvent, GroupAtMessageCreateEvent, C2CMessageCreateEvent
import json
import random
import time
import nonebot
from nonebot import require
import requests
import time
import datetime
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from pathlib import Path
from nonebot import require

timing = require("nonebot_plugin_apscheduler").scheduler
@timing.scheduled_job("cron", hour='04', minute = '00' , second = '00' ,id="0点任务")
async def _():
    #这里是获取bot对象
    local_time = time.localtime()
    year = local_time.tm_year
    month = local_time.tm_mon
    day = local_time.tm_mday
    week_list = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    结果 = week_list[datetime.date(year, month, day).weekday()]
    if 结果 == "星期一":
        周更战绩()

def 排行榜(num_scores):
    try:
        data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
        with open(data, "r", encoding="utf-8") as file:
            战绩 = json.load(file)
            sorted_leaderboard = sorted(战绩["分数"].items(), key=lambda x: x[1], reverse=True)
            return sorted_leaderboard[:num_scores]
    except FileNotFoundError:
        return '无'
    except ValueError:
        return '无'
    except KeyError:
        return '无'
    
def 个人排行榜(player_name):
    try:
        data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
        with open(data, "r", encoding="utf-8") as file:
            战绩 = json.load(file)
            sorted_leaderboard = sorted(战绩["分数"].items(), key=lambda x: x[1], reverse=True)
            player_rank = [x[0] for x in sorted_leaderboard].index(player_name) + 1
            return player_rank
    except FileNotFoundError:
        return '无'
    except ValueError:
        return '无'
    except KeyError:
        return '无'

def 周更战绩():
    try:
        data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
        with open(data, "r", encoding="utf-8") as file:
            战绩 = json.load(file)
            长度 = len(战绩["分数"])
        top_scores = 排行榜(长度)
        for key, value in top_scores:
            if value >= 200:
                value = value/100 * 20 + 100
                战绩["分数"][key] = value
            elif value < 200:
                value = value/100 * 70
                战绩["分数"][key] = value
        with open(data, "w", encoding="utf-8") as file:
            json.dump(战绩, file, indent=4)
    except:
        pass

def 个人战绩(用户):
    data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
    with open(data, "r", encoding="utf-8") as file:
        战绩 = json.load(file)
        胜场 = 战绩[str(用户)]["胜场"]
        败场 = 战绩[str(用户)]["败场"]
        胜率 = 战绩[str(用户)]["胜率"]
        分数 = 战绩['分数'][str(用户)]
        return 胜场, 胜率, 败场, 分数

def 个人信息录入(用户1, 分数1, 用户2, 分数2):
    data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
    try:
        with open(data, "r", encoding="utf-8") as file:
            战绩 = json.load(file)
            总场次1 = 战绩[str(用户1)]["总场次"]
            胜场1 = 战绩[str(用户1)]["胜场"]
            原分数1 = 战绩['分数'][str(用户1)]
            胜率1 = round(((胜场1 + 1)/(总场次1 + 1)*100),2)
            总场次2 = 战绩[str(用户2)]["总场次"]
            胜场2 = 战绩[str(用户2)]["胜场"]
            败场2 = 战绩[str(用户2)]["败场"]
            原分数2 = 战绩['分数'][str(用户2)]
            胜率2 = round((胜场2/(总场次2 + 1)*100),2)
            战绩[str(用户2)]["总场次"] = 总场次2 + 1
            战绩[str(用户2)]["败场"] = 败场2 + 1
            战绩[str(用户2)]["胜率"] = 胜率2
            战绩['分数'][str(用户2)] = 原分数2 + 分数2
            战绩[str(用户1)]["总场次"] = 总场次1 + 1
            战绩[str(用户1)]["胜场"] = 胜场1 + 1
            战绩[str(用户1)]["胜率"] = 胜率1
            战绩['分数'][str(用户1)] = 原分数1 + 分数1
            print('信息录入完成')
            with open(data, "w", encoding="utf-8") as file:
                json.dump(战绩, file, indent=4)
    except FileNotFoundError:
        with open(data, "w", encoding="utf-8") as file:
            内容 = {"分数":{str(用户1):100,str(用户2):100},str(用户1):{"总场次":0,"胜场":0,"败场":0,"胜率":0},str(用户2):{"总场次":0,"胜场":0,"败场":0,"胜率":0}}
            json.dump(内容, file, indent=4)
        个人信息录入(用户1, 分数1, 用户2, 分数2)
    except KeyError:
        data = "src/plugins/恶魔轮盘/个人信息/战绩.txt"
        with open(data, "r", encoding="utf-8") as file:
            战绩 = json.load(file)
            战绩[str(用户1)] = {"总场次":0,"胜场":0,"败场":0,"胜率":0}
            战绩['分数'][str(用户1)] = 100
            战绩[str(用户2)] = {"总场次":0,"胜场":0,"败场":0,"胜率":0}
            战绩['分数'][str(用户2)] = 100
        with open(data, "w", encoding="utf-8") as file:
            json.dump(战绩, file, indent=4)
        个人信息录入(用户1, 分数1, 用户2, 分数2)

def 对局打分(胜负, 回合, 血量):
    赢分 = 100 - 回合 * 5 + 血量 * 3
    输分 = 回合 * 10 - 60
    if 胜负 == '赢':
        return 赢分
    elif 胜负 == '输':
        return 输分

def chuangjian_1(name,text):
    txt_name = "src/plugins/恶魔轮盘/匹配/" + name + ".txt"
    with open(txt_name, "w", encoding="utf-8") as file:
        json.dump(text, file, indent=4)
    print('创建完成')

def 双方信息(user_1,user_2):
    子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    with open(子弹详情, "r", encoding="utf-8") as file_1:
        data_1 = json.load(file_1)
        血量1 = data_1[str(user_1)]['血量']
        血量2 = data_1[str(user_2)]['血量']
        return 血量1, 血量2

def 子弹检查(user_1,user_2):
    data = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    子弹 = ["空弹","实弹"]
    子弹安排 = []
    with open(data, "r", encoding="utf-8") as file:
        data_1 = json.load(file)
        回合 = data_1[str(user_1)]['回合数'] + 1
        状态 = 0
        道具反馈 = '无'
        if len(data_1[str(user_1)]['子弹安排']) == 0:
            状态 = 1
            颗数 = 0
            for i in range(4 + 回合//2):
                num = random.randint(0, 1)
                子弹安排.append(子弹[num])
                data_1[str(user_1)]['子弹安排'].append(子弹[num])
                data_1[str(user_2)]['子弹安排'].append(子弹[num])
                颗数 = 颗数 + 1
                if 子弹安排.count('空弹') == 3 + 回合//2 and 颗数 == 3 + 回合//2:
                    子弹安排.append("实弹")
                    data_1[str(user_1)]['子弹安排'].append('实弹')
                    data_1[str(user_2)]['子弹安排'].append('实弹')
                    print('实弹保底')
                    break
                elif 子弹安排.count('实弹') == 3 + 回合//2 and 颗数 == 3 + 回合//2:
                    子弹安排.append("空弹")
                    data_1[str(user_1)]['子弹安排'].append('空弹')
                    data_1[str(user_2)]['子弹安排'].append('空弹')
                    print('空弹保底')
                    break
            data_1[str(user_1)]['回合数'] = 回合
            data_1[str(user_2)]['回合数'] = 回合
            data_1[str(user_1)]['手铐效果'] = 0
            data_1[str(user_2)]['手铐效果'] = 0
            data_1[str(user_1)]['伤害'] = 1 + 回合//4
            data_1[str(user_2)]['伤害'] = 1 + 回合//4
            with open(data, "w", encoding="utf-8") as file:
                json.dump(data_1, file, indent=4)
                道具反馈 = 道具分配(user_1,user_2,回合)
                return 子弹安排, 状态, 道具反馈
        else:
            return 子弹安排, 状态, 道具反馈

def 道具分配(user_1,user_2,回合):
    列表 = ["小刀","华子","饮料","手机","骰子","手铐","偷偷","过期药","放大镜","逆转器"]
    data = 'src/plugins/恶魔轮盘/匹配/道具状况.txt'
    道具缓存1 = []
    道具缓存2 = []
    try:
        with open(data, "r", encoding="utf-8") as file:
            data_1 = json.load(file)
            概率 = {"小刀":2,"华子":2,"饮料":2,"手机":2,"骰子":1,"手铐":2,"偷偷":2,"过期药":2,"放大镜":2,"逆转器":2}
            for i in range(3 + 回合//2):
                结果 = random.choices(列表,weights=[概率["小刀"],概率["华子"],概率['饮料'],概率["手机"],概率["骰子"],概率["手铐"],概率["偷偷"],概率["过期药"],概率["放大镜"],概率["逆转器"]],k=1)
                道具 = 结果[0]
                if 道具缓存1.count(道具) == 2:
                    概率[道具] = 0
                    道具缓存1.append(道具)
                else:
                    道具缓存1.append(道具)
            概率 = {"小刀":2,"华子":2,"饮料":2,"手机":2,"骰子":1,"手铐":2,"偷偷":2,"过期药":2,"放大镜":2,"逆转器":2}
            for i in range(3 + 回合//2):
                结果 = random.choices(列表,weights=[概率["小刀"],概率["华子"],概率['饮料'],概率["手机"],概率["骰子"],概率["手铐"],概率["偷偷"],概率["过期药"],概率["放大镜"],概率["逆转器"]],k=1)
                道具 = 结果[0]
                if 道具缓存2.count(道具) == 2:
                    概率[道具] = 0
                    道具缓存2.append(道具)
                else:
                    道具缓存2.append(道具)
            data_1[str(user_1)]['道具安排'] = 道具缓存1
            data_1[str(user_2)]['道具安排'] = 道具缓存2
            with open(data, "w", encoding="utf-8") as file:
                json.dump(data_1, file, indent=4)
            return '道具分发完毕'
    except FileNotFoundError:
            chuangjian_1("道具状况",{str(user_1):{'道具安排':[]},str(user_2):{'道具安排':[]}})
            a = 道具分配(user_1,user_2,回合)
            return a
    except KeyError:
        data_1[str(user_1)] = {'道具安排':[]}
        data_1[str(user_2)] = {'道具安排':[]}
        with open(data, "w", encoding="utf-8") as file:
            json.dump(data_1, file, indent=4)
        a = 道具分配(user_1,user_2,回合)
        return a


def 进入游戏开局(user_1,user_2):
    子弹 = ["空弹","实弹"]
    用户 = [user_1,user_2]
    子弹安排 = []
    回合 = 1
    data = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    try:
        with open(data, "r", encoding="utf-8") as file:
            data_1 = json.load(file)
            data_1[str(user_1)]['手铐效果'] = 0
            data_1[str(user_2)]['手铐效果'] = 0
            data_1[str(user_1)]['回合数'] = 1
            data_1[str(user_2)]['回合数'] = 1
            data_1[str(user_1)]['先手顺序'] = '后手'
            data_1[str(user_2)]['先手顺序'] = '后手'
            data_1[str(user_1)]['伤害'] = 1
            data_1[str(user_2)]['伤害'] = 1
            data_1[str(user_1)]['血量'] = 5
            data_1[str(user_2)]['血量'] = 5
            data_1[str(user_1)]['血量上限'] = 5
            data_1[str(user_2)]['血量上限'] = 5
            状况 = random.randint(0, 1)
            先手 = 用户[状况]
            颗数 = 0
            data_1[str(先手)]['先手顺序'] = '先手'
            for i in range(4):
                num = random.randint(0, 1)
                子弹安排.append(子弹[num])
                data_1[str(user_1)]['子弹安排'].append(子弹[num])
                data_1[str(user_2)]['子弹安排'].append(子弹[num])
                颗数 = 颗数 + 1
                if 子弹安排.count('空弹') == 3 and 颗数 == 3:
                    子弹安排.append("实弹")
                    data_1[str(user_1)]['子弹安排'].append('实弹')
                    data_1[str(user_2)]['子弹安排'].append('实弹')
                    print('实弹保底')
                    break
                elif 子弹安排.count('实弹') == 3 and 颗数 == 3:
                    子弹安排.append("空弹")
                    data_1[str(user_1)]['子弹安排'].append('空弹')
                    data_1[str(user_2)]['子弹安排'].append('空弹')
                    print('空弹保底')
                    break
            with open(data, "w", encoding="utf-8") as file:
                json.dump(data_1, file, indent=4)
            道具反馈 = 道具分配(user_1,user_2,回合)
            return str(子弹安排), str(用户[状况]), 道具反馈
    except FileNotFoundError:
            chuangjian_1("子弹状况",{str(user_1):{'子弹安排':[]},str(user_2):{'子弹安排':[]}})
            a, b, c = 进入游戏开局(user_1,user_2)
            return a, b, c
    except KeyError:
        data_1[str(user_1)] = {'子弹安排':[]}
        data_1[str(user_2)] = {'子弹安排':[]}
        with open(data, "w", encoding="utf-8") as file:
            json.dump(data_1, file, indent=4)
        a, b, c = 进入游戏开局(user_1,user_2)
        return a, b, c
    
def 获取昵称(用户):
    data = f"src/plugins/恶魔轮盘/个人信息/基础信息/{用户}.txt"
    try:
        with open(data, "r", encoding="utf-8") as file:
            昵称 = file.read()
        return 昵称
    except:
        return "【未知】"

def 道具使用(用户, 道具):
    data = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
    with open(对局参数, "r", encoding="utf-8") as file:
        对手查询 = json.load(file)
    with open(data, "r", encoding="utf-8") as file:
        data_d = json.load(file)
        回合 = data_d[str(用户)]['回合数']
        伤害 = data_d[str(用户)]['伤害']
        血量 = data_d[str(用户)]['血量']
        血量上限 = data_d[str(用户)]['血量上限']
        对手 = 对手查询[str(用户)]['对手']
        手铐 = data_d[str(用户)]['手铐效果']
        对手血量 = data_d[str(对手)]['血量']
        if 道具 == '小刀':
            if 伤害 == 2 + 回合//4:
                return '无法使用', '小刀效果未消失'
            else:
                data_d[str(用户)]['伤害'] = 伤害 + 1
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', '使用成功'
        elif 道具 == '华子':
            if 血量 == 血量上限:
                return '无法使用', '是满血呢，无法使用'
            else:
                data_d[str(用户)]['血量'] = 血量 + 1
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', '使用成功'
        elif 道具 == '饮料':
            发送 = '使用成功，退掉了一颗'
            if len(data_d[str(用户)]['子弹安排']) == 1:
                子弹 = data_d[str(用户)]['子弹安排'][0]
                data_d[str(用户)]['子弹安排'].pop(0)
                data_d[str(对手)]['子弹安排'].pop(0)
                发送 += 子弹
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                子弹安排, 状态, 道具 = 子弹检查(用户,对手)
                发送 += f"\n子弹分配完毕\n空弹:{str(子弹安排.count('空弹'))}颗\n实弹:{str(子弹安排.count('实弹'))}颗\n道具分配完毕"
                return '刷回合', 发送
            else:
                子弹 = data_d[str(用户)]['子弹安排'][0]
                data_d[str(用户)]['子弹安排'].pop(0)
                data_d[str(对手)]['子弹安排'].pop(0)
                发送 += 子弹
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', 发送
        elif 道具 == '手机':
            子弹 = data_d[str(用户)]['子弹安排']
            长度 = len(data_d[str(用户)]['子弹安排']) - 1
            序号 = random.randint(0, 长度)
            结果1 = 序号 + 1
            结果2 = 子弹[序号]
            return '私聊', f"第{结果1}颗子弹是{结果2}"
        elif 道具 == '骰子':
            原子弹安排 = data_d[str(用户)]['子弹安排']
            random.shuffle(原子弹安排)
            data_d[str(用户)]['子弹安排'] = 原子弹安排
            data_d[str(对手)]['子弹安排'] = 原子弹安排
            with open(data, "w", encoding="utf-8") as file:
                json.dump(data_d, file, indent=4)
            return '群发', '使用成功，当前子弹已经打乱'
        elif 道具 == '手铐':
            if 手铐 != 0:
                return '无法使用', '手铐效果未消失'
            else:
                data_d[str(用户)]['手铐效果'] = 2
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', '使用成功'
        elif 道具 == '过期药':
            随机 = ["回血","扣血"]
            num = random.randint(0, 1)
            结果 = 随机[num]
            if 结果 == '回血':
                if 血量 >= 血量上限:
                    return '群发', '是满血消耗呢'
                else:
                    if 血量 < 3:
                        data_d[str(用户)]['血量'] = 血量 + 2
                        with open(data, "w", encoding="utf-8") as file:
                            json.dump(data_d, file, indent=4)
                        return '群发', '成功回复2滴血'
                    else:
                        data_d[str(用户)]['血量'] = 5
                        with open(data, "w", encoding="utf-8") as file:
                            json.dump(data_d, file, indent=4)
                        return '群发', '回满力'
            elif 结果 == '扣血':
                if 血量 > 1:
                    data_d[str(用户)]['血量'] = 血量 - 1
                    with open(data, "w", encoding="utf-8") as file:
                        json.dump(data_d, file, indent=4)
                    return '群发', '哎呀，扣血了'
                elif 血量 == 1:
                    del data_d[str(用户)]['子弹安排'][0:]
                    del data_d[str(对手)]['子弹安排'][0:]
                    data_d[str(用户)]['回合数'] = 1
                    data_d[str(对手)]['回合数'] = 1
                    对手查询[str(用户)]['type'] = '未开始'
                    对手查询[str(对手)]['type'] = '未开始'
                    with open(data, "w", encoding="utf-8") as file:
                        json.dump(data_d, file, indent=4)
                        file.close()
                    with open(对局参数, "w", encoding="utf-8") as file:
                        json.dump(对手查询, file, indent=4)
                        file.close()
                    赢 = 对局打分('赢', 回合, 对手血量)
                    输 = 对局打分('输', 回合, 血量)
                    个人信息录入(对手, 赢, 用户, 输)
                    return '游戏失败', 对手
        elif 道具 == '逆转器':
            子弹 = data_d[str(用户)]['子弹安排'][0]
            if 子弹 == '空弹':
                data_d[str(用户)]['子弹安排'][0] = '实弹'
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', '当前子弹逆转成功'
            elif 子弹 == '实弹':
                data_d[str(用户)]['子弹安排'][0] = '空弹'
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                return '群发', '当前子弹逆转成功'
        elif 道具 == '放大镜':
            子弹 = data_d[str(用户)]['子弹安排'][0]
            return '群发', f"当前子弹是{子弹}"
        
def 注册检测(用户):
    data = f"src/plugins/恶魔轮盘/个人信息/基础信息/{用户}.txt"
    try:
        with open(data, "r", encoding="utf-8") as f:
            out = f.read()
        return '注册'
    except:
        return '未注册'

yxcd = on_command('恶魔轮盘',priority=10,block=True)
kspp = on_command('开始匹配',priority=10,block=True)
zzpp = on_command('终止匹配',priority=10,block=True)
kqdd = on_command('开枪对敌',priority=10,block=True)
kqdj = on_command('开枪对己',priority=10,block=True)
phb = on_command('排行榜',priority=10,block=True)
zhanji = on_command('战绩',priority=10,block=True)
xx = on_command('信息',priority=10,block=True)
djcs = on_command('道具次数',priority=10,block=True)
sydj = on_keyword({'使用'},priority=10,block=True)
#priority的值越低，优先级越高，block=True用于阻断类似指令的重复触发
sydjtt = on_keyword({'使用偷偷'},priority=5,block=True)
dj = on_command('道具',priority=10,block=True)
djlb = on_command('道具列表',priority=10,block=True)
注册游戏 = on_command("注册恶魔轮盘",priority=10,block=True)
修改名称 = on_command("修改名称",priority=10,block=True)

@注册游戏.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if len(args) == 0:
        await  注册游戏.send("请勿输入空名称")
    else:
    # 获取用户输入的游戏名称
        data = f"src/plugins/恶魔轮盘/个人信息/基础信息/{event.get_user_id()}.txt"
        try:
            with open(data, "r", encoding="utf-8") as f:
                out = f.read()
            await 注册游戏.send("您已注册过游戏，请勿重复注册！")
        except:
            with open(data, "w", encoding="utf-8") as f:
                f.write(str(args))
            await 注册游戏.send("\n注册成功！\n欢迎"+args+"来到恶魔轮盘！\n发送【/恶魔轮盘】\n即可查看完整的游戏菜单\n\n[还请使用不易混淆的昵称，发送【修改名称 昵称】修改]\n\n注：本游戏极易刷屏，而且由于官方接口的限制，对局提示做不到很明显，望见谅")
            try:
                匹配参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
                with open(匹配参数, "r", encoding="utf-8") as file:
                    data_d = json.load(file)
                data_d[str(event.get_user_id())] = {'type':'未开始'}
                with open(匹配参数, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
            except:
                chuangjian_1("匹配参数",{str(event.get_user_id()):{'type':'未开始'}})
                

@修改名称.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if len(args) == 0:
        await  注册游戏.send("请勿输入空名称")
    else:
    # 获取用户输入的游戏名称
        data = f"src/plugins/恶魔轮盘/个人信息/基础信息/{event.get_user_id()}.txt"
        try:
            with open(data, "r", encoding="utf-8") as f:
                out = f.read()
            with open(data, "w", encoding="utf-8") as f:
                f.write(str(args))
            await 注册游戏.send(args+"昵称修改成功！")
        except:
            await 注册游戏.send("您还未注册游戏，请先发送【注册恶魔轮盘 昵称】注册！")

@djlb.handle()
async def emlpdj(bot: Bot, event: MessageEvent):
        data = 'src/plugins/恶魔轮盘/恶魔轮盘道具.png'
        await djlb.send(MessageSegment.file_image(Path(data)))

@xx.handle()
async def emlpdj(bot: Bot, event: MessageEvent):
    子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
    try:
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
        with open(子弹详情, "r", encoding="utf-8") as file_1:
            data_1 = json.load(file_1)
            对手 = data_2[str(event.get_user_id())]['对手']
            回合 = data_1[str(event.get_user_id())]['回合数']
            伤害 = data_1[str(event.get_user_id())]['伤害']
            血量 = data_1[str(event.get_user_id())]['血量']
            对手血量 = data_1[str(对手)]['血量']
            顺序1 = data_1[str(event.get_user_id())]['先手顺序']
            顺序2 = data_1[str(对手)]['先手顺序']
        if data_2[str(event.get_user_id())]['type'] == '未开始':
            await xx.send(Message('您暂未加入对局'))
        else:
            await xx.send(Message('\n当前回合：' + str(回合) + '\n基础伤害：' + str(伤害) + '\n\n' +获取昵称(event.get_user_id()) + '\n顺序：' + str(顺序1) +'\n血量：' + str(血量) + '\n\n' + 获取昵称(对手) + '\n顺序：' + str(顺序2) + '\n血量：' + str(对手血量)))
    except FileNotFoundError:
        await xx.send(Message('您暂未加入对局'))
    except json.decoder.JSONDecodeError:
        await xx.send(Message('您暂未加入对局'))
    except KeyError:
        await xx.send(Message('您暂未加入对局'))

@phb.handle()
async def emlpdj(bot: Bot, event: MessageEvent):
        反馈 = 排行榜(5)
        发送 = '\n以下是排名'
        序号 = 1
        if 反馈 == '无':
            await phb.send(Message('暂时没有排行榜的数据呢'))
        else:
            for key, value in 反馈:
                昵称 = 获取昵称(key)
                胜场, 胜率, 败场, 分数 = 个人战绩(key)
                value = round(value,2)
                发送 += '\n\n' + f"第{序号}名：{昵称}\n分数：{value}\n胜场：{胜场}场 胜率：{胜率}%"
                序号 = 序号 + 1
            await phb.send(Message(发送))

@zhanji.handle()
async def emlpdj(bot: Bot, event: MessageEvent):
        反馈 = 个人排行榜(str(event.get_user_id()))
        if 反馈 == '无':
            await phb.send(Message('暂时没有参加恶魔轮盘呢'))
        else:
            昵称 = 获取昵称(event.get_user_id())
            胜场, 胜率, 败场, 分数 = 个人战绩(str(event.get_user_id()))
            分数 = round(分数,2)
            发送 = f"\n用户：{昵称}\n第{反馈}名    分数：{分数}\n胜场：{胜场}场\n胜率：{胜率}%"
            await zhanji.send(Message(发送))


@dj.handle()
async def emlpdj(bot: Bot, event: MessageEvent):
    data = 'src/plugins/恶魔轮盘/匹配/道具状况.txt'
    对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
    道具 = ["小刀","华子","饮料","手机","骰子","手铐","偷偷","过期药","放大镜","逆转器"]
    try:
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
        with open(data, "r", encoding="utf-8") as file:
            data_d = json.load(file)
            对手 = data_2[str(event.get_user_id())]['对手']
            道具数量 = len(道具)
            用户道具 = data_d[str(event.get_user_id())]['道具安排']
            对手道具 = data_d[str(对手)]['道具安排']
            发送 = ''
            if data_2[str(event.get_user_id())]['type'] == '正在进行':
                if len(用户道具) != 0:
                    发送 += '\n您的道具如下：\n'
                    for i in range(道具数量):
                        当前道具 = 道具[i]
                        if 当前道具 in 用户道具:
                            发送 += '\n' + 当前道具 + ' x ' + str(用户道具.count(当前道具))
                        else:
                            pass
                    if len(对手道具) != 0:
                        发送 += '\n\n对手的道具如下：\n'
                        for i in range(道具数量):
                            当前道具 = 道具[i]
                            if 当前道具 in 对手道具:
                                发送 += '\n' + 当前道具 + ' x ' + str(对手道具.count(当前道具))
                            else:
                                pass
                    await dj.send(Message(发送))
                else:
                    await dj.send("你的道具用完了")
            else:
                await dj.send(Message('您暂未加入对局'))
    except FileNotFoundError:
        await dj.send(Message('您暂未加入对局'))
    except json.decoder.JSONDecodeError:
        await dj.send(Message('您暂未加入对局'))
    except KeyError:
        await dj.send(Message('您暂未加入对局'))

@sydj.handle()
async def emlpdj(event: MessageEvent):
    ans = str(event.get_message()).strip()
    ans = ans.strip('/使用 ')
    data = 'src/plugins/恶魔轮盘/匹配/道具状况.txt'
    子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
    try:
        with open(子弹详情, "r", encoding="utf-8") as file_1:
                data_1 = json.load(file_1)
        with open(data, "r", encoding="utf-8") as file:
            data_d = json.load(file)
            用户道具 = data_d[str(event.get_user_id())]['道具安排']
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
        if data_2[str(event.get_user_id())]['type'] == '正在进行':
            if data_1[str(event.get_user_id())]['先手顺序'] == '后手':
                await kqdj.send(Message('还不是你的回合'))
            else:
                if ans in 用户道具:
                    情况, 反馈 = 道具使用(event.get_user_id(), ans)
                    if 情况 == '群发':
                        if 反馈 == '使用成功':
                            await dj.send(Message(ans + '使用成功'))
                            data_d[str(event.get_user_id())]['道具安排'].remove(ans)
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                        else:
                            await dj.send(Message(反馈))
                            data_d[str(event.get_user_id())]['道具安排'].remove(ans)
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                    elif 情况 == '刷回合':
                        resp = await dj.send(Message(反馈))
                        await asyncio.sleep(10)
                        (bot,) = nonebot.get_bots().values()
                        await bot.delete_group_message(group_openid=event.get_session_id().split('_')[2], message_id=resp.id)
                    elif 情况 == '无法使用':
                        await dj.send(Message(反馈))
                    elif 情况 == '私聊':
                        if "friend" in event.get_session_id():
                            data_d[str(event.get_user_id())]['道具安排'].remove(ans)
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                            await dj.send(Message(反馈))
                        else:
                            await dj.send(Message('请在私聊使用该道具\n格式为/使用 手机'))
                    elif 情况 == '游戏失败':
                        await dj.send(Message('恭喜' + 获取昵称(反馈) + '获得胜利'))
                else:
                    await dj.send(Message('没有这个道具哦'))
        else:
            await dj.send(Message('您暂未加入对局'))
    except FileNotFoundError:
        await dj.send(Message('您暂未加入对局'))
    except json.decoder.JSONDecodeError:
        await dj.send(Message('您暂未加入对局'))
    except KeyError:
        await dj.send(Message('您暂未加入对局'))

@sydjtt.handle()
async def emlpdjtt(event: MessageEvent):
    ans = str(event.get_message()).strip()
    ans = ans.strip('/使用偷偷 ')
    data = 'src/plugins/恶魔轮盘/匹配/道具状况.txt'
    子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
    对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
    try:
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
        with open(子弹详情, "r", encoding="utf-8") as file_1:
            data_1 = json.load(file_1)
        with open(data, "r", encoding="utf-8") as file:
            data_d = json.load(file)
            对手 = data_2[str(event.get_user_id())]['对手']
            用户道具 = data_d[str(event.get_user_id())]['道具安排']
            对手道具 = data_d[str(对手)]['道具安排']
        if data_2[str(event.get_user_id())]['type'] == '正在进行':
            if data_1[str(event.get_user_id())]['先手顺序'] == '后手':
                await kqdj.send(Message('还不是你的回合'))
            elif '偷偷' in 用户道具:
                if ans in 对手道具:
                    情况, 反馈 = 道具使用(event.get_user_id(), ans)
                    if 情况 == '群发':
                        if 反馈 == '使用成功':
                            await dj.send(Message(ans + '使用成功'))
                            data_d[str(对手)]['道具安排'].remove(ans)
                            data_d[str(event.get_user_id())]['道具安排'].remove('偷偷')
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                        else:
                            await dj.send(Message(反馈))
                            data_d[str(对手)]['道具安排'].remove(ans)
                            data_d[str(event.get_user_id())]['道具安排'].remove('偷偷')
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                    elif 情况 == '刷回合':
                        resp = await dj.send(Message(反馈))
                        await asyncio.sleep(10)
                        (bot,) = nonebot.get_bots().values()
                        await bot.delete_group_message(group_openid=event.get_session_id().split('_')[2], message_id=resp.id)
                    elif 情况 == '无法使用':
                        await dj.send(Message(反馈))
                    elif 情况 == '私聊':
                        if "friend" in event.get_session_id():
                            data_d[str(对手)]['道具安排'].remove(ans)
                            with open(data, "w", encoding="utf-8") as file:
                                json.dump(data_d, file, indent=4)
                            await dj.send(Message(反馈))
                        else:
                            await dj.send(Message('请在私聊使用该道具\n格式为/使用偷偷 手机'))
                    elif 情况 == '游戏失败':
                        await dj.send(Message('恭喜' + 获取昵称(反馈) + '获得胜利'))
                else:
                    await dj.send(Message('没有这个道具哦'))
            else:
                await dj.send(Message('没有偷偷哦'))
        else:
            await dj.send("您暂未加入对局")
    except FileNotFoundError:
        await dj.send(Message('您暂未加入对局'))
    except json.decoder.JSONDecodeError:
        await dj.send(Message('您暂未加入对局'))
    except KeyError:
        await dj.send(Message('您暂未加入对局'))


@yxcd.handle()
async def emlpcd(event: MessageEvent):
        data = 'src/plugins/恶魔轮盘/菜单.txt'
        with open(data, "r", encoding="utf-8") as file:
            file = file.read()
            await yxcd.send(Message("\n"+file))

@kspp.handle()
async def emlpkspp(event: GroupAtMessageCreateEvent):
    群号 = event.group_openid
    if 注册检测(event.get_user_id()) == '未注册':
        await kspp.send(Message('请先注册游戏\n注册分发：【注册恶魔轮盘 昵称】'))
    else:
        try:
            data = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
            with open(data, "r", encoding="utf-8") as file:
                data_d = json.load(file)
            a = len(data_d[str(群号)]['匹配人'])
            状态 = data_d[str(event.get_user_id())]['type']
            if 状态 == '正在进行':
                await kspp.send(Message('您正在进行游戏中'))
            elif 状态 == '未开始':
                if event.get_user_id() not in data_d[str(群号)]['匹配人']:
                    data_d[str(群号)]['匹配人'].append(event.get_user_id())
                    data_d[str(event.get_user_id())]['type'] = '开始'
                    with open(data, "w", encoding="utf-8") as file:
                        await kspp.send(Message('正在为您匹配中'))
                        for i in range(a):
                            b = data_d[str(群号)]['匹配人'][i]
                            if data_d[str(b)]['type'] == '开始' and b != event.get_user_id():
                                await kspp.send(Message('匹配成功，你的对手是' + 获取昵称(b)))
                                data_d[str(event.get_user_id())]['type'] = '正在进行'
                                data_d[str(b)]['type'] = '正在进行'
                                data_d[str(event.get_user_id())]['对手'] = b
                                data_d[str(b)]['对手'] = event.get_user_id()
                                json.dump(data_d, file, indent=4)
                                file.close()
                                await asyncio.sleep(2)
                                反馈, 用户, 道具 = 进入游戏开局(b,event.get_user_id())
                                resp = await kspp.send(Message('\n子弹分配完毕\n' + '空弹:' + str(反馈.count('空弹')) + '颗\n' + '实弹:' + str(反馈.count('实弹')) + '颗\n'+ 获取昵称(用户) + "是先手"))
                                if 道具 == '无':
                                    print('没到发道具的时候')
                                else:
                                    await kspp.send(Message(道具))
                                    await asyncio.sleep(10)
                                    (bot,) = nonebot.get_bots().values()
                                    await bot.delete_group_message(group_openid=event.group_openid, message_id=resp.id)
                                break
                            elif i + 1 < a:
                                pass
                            else:    
                                await kspp.send('没人匹配的喔，可以先终止匹配')
                                json.dump(data_d, file, indent=4)
                                file.close()
                else:
                    data_d[str(event.get_user_id())]['type'] = '开始'
                    with open(data, "w", encoding="utf-8") as file:
                        await kspp.send(Message('正在为您匹配中'))
                        for i in range(a):
                            b = data_d[str(群号)]['匹配人'][i]
                            if data_d[str(b)]['type'] == '开始' and b != event.get_user_id():
                                await kspp.send(Message('匹配成功，你的对手是' + 获取昵称(b)))
                                data_d[str(event.get_user_id())]['type'] = '正在进行'
                                data_d[str(b)]['type'] = '正在进行'
                                data_d[str(event.get_user_id())]['对手'] = b
                                data_d[str(b)]['对手'] = event.get_user_id()
                                json.dump(data_d, file, indent=4)
                                file.close()
                                await asyncio.sleep(2)
                                反馈, 用户, 道具 = 进入游戏开局(b,event.get_user_id())
                                resp = await kspp.send(Message('\n子弹分配完毕\n' + '空弹:' + str(反馈.count('空弹')) + '颗\n' + '实弹:' + str(反馈.count('实弹')) + '颗\n'+ 获取昵称(用户) + "是先手"))
                                if 道具 == '无':
                                    print('没到发道具的时候')
                                else:
                                    await kspp.send(Message(道具))
                                    await asyncio.sleep(10)
                                    (bot,) = nonebot.get_bots().values()
                                    await bot.delete_group_message(group_openid=event.group_openid, message_id=resp.id)
                                break
                            elif i + 1 < a:
                                pass
                            else:    
                                await kspp.send('没人匹配的喔，可以先终止匹配')
                                json.dump(data_d, file, indent=4)
                                file.close()
            elif data_d[str(event.get_user_id())]['type'] == '开始':
                await kspp.send(Message('您已经在匹配中'))
        except KeyError:
            if str(群号) not in data_d:
                data_d[str(群号)] = {'匹配人':[event.get_user_id()]}
                data_d[str(event.get_user_id())]['type'] = '开始'
                with open(data, "w", encoding="utf-8") as file:
                    await kspp.send(Message('正在为您匹配中,该游戏为群友pvp游戏如果没有群友响应匹配的话，请耐心等待'))
                    json.dump(data_d, file, indent=4)

@zzpp.handle()
async def emlpzzpp(bot: Bot, event: GroupAtMessageCreateEvent):
    if 注册检测(event.get_user_id()) == '未注册':
        await kspp.send(Message('请先注册游戏\n注册分发：【注册恶魔轮盘 昵称】'))
    else:
        try:
            群号 = event.group_openid
            data = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
            with open(data, "r", encoding="utf-8") as file:
                data_d = json.load(file)
            if data_d[str(event.get_user_id())]['type'] == '正在进行':
                await zzpp.send(Message('暂时不支持中途退出哦'))
            elif data_d[str(event.get_user_id())]['type'] == '开始':
                data_d[str(event.get_user_id())]['type'] = '未开始'
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                    await zzpp.send(Message('已经终止匹配'))
            elif data_d[str(event.get_user_id())]['type'] == '未开始':
                await zzpp.send(Message('已经终止匹配了'))
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
        except FileNotFoundError:
            chuangjian_1("匹配参数",{str(群号):{'匹配人':[event.get_user_id()]},str(event.get_user_id()):{'type':'未开始'}})
            await zzpp.send(Message('已经终止匹配'))
        except json.decoder.JSONDecodeError:
            data_b = {str(群号):{'匹配人':[event.get_user_id()]},str(event.get_user_id()):{'type':'未开始'}}
            with open(data, "w", encoding="utf-8") as file:
                json.dump(data_b, file, indent=4)
                print('创建完成完成')
                await zzpp.send(Message('已经终止匹配'))
        except KeyError:
                data = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
                with open(data, "r", encoding="utf-8") as file:
                    data_d = json.load(file)
                data_d[str(event.get_user_id())] = {'type':'未开始'}
                with open(data, "w", encoding="utf-8") as file:
                    json.dump(data_d, file, indent=4)
                    await zzpp.send(Message('已经终止匹配'))

@kqdd.handle()
async def emlpkqdd(event: GroupAtMessageCreateEvent):
    try:

        子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
        对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
        对局结束 = 2
        with open(子弹详情, "r", encoding="utf-8") as file_1:
            data_1 = json.load(file_1)
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
            对手 = data_2[str(event.get_user_id())]['对手']
            血量 = data_1[str(对手)]['血量']
            己方血量 = data_1[str(event.get_user_id())]['血量']
            伤害 = data_1[str(event.get_user_id())]['伤害']
            回合 = data_1[str(event.get_user_id())]['回合数']
            手铐 = data_1[str(event.get_user_id())]['手铐效果']
            if data_2[str(event.get_user_id())]['type'] == '正在进行':
                if data_1[str(event.get_user_id())]['先手顺序'] == '后手':
                    await kqdd.send(Message('还不是你的回合'))
                elif data_1[str(event.get_user_id())]['先手顺序'] == '先手':
                    if len(data_1[str(event.get_user_id())]['子弹安排']) == 0:
                        await kqdd.send(Message('请等待子弹补充完毕'))
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '实弹' and 血量 - 伤害 <=0:
                        del data_1[str(event.get_user_id())]['子弹安排'][0:]
                        del data_1[str(对手)]['子弹安排'][0:]
                        data_1[str(event.get_user_id())]['回合数'] = 1
                        data_1[str(对手)]['回合数'] = 1
                        手铐 = data_1[str(event.get_user_id())]['手铐效果'] = 0
                        data_2[str(event.get_user_id())]['type'] = '未开始'
                        data_2[str(对手)]['type'] = '未开始'
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                            file.close()
                        with open(对局参数, "w", encoding="utf-8") as file:
                            json.dump(data_2, file, indent=4)
                            file.close()
                            await kqdd.send(Message('恭喜' +获取昵称(event.get_user_id())+ '获取胜利'))
                            赢 = 对局打分('赢', 回合, 己方血量)
                            输 = 对局打分('输', 回合, 血量)
                            个人信息录入(event.get_user_id(), 赢, 对手, 输)
                            对局结束 = 1
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '实弹':
                        if 手铐 == 2:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '先手'
                            data_1[str(对手)]['先手顺序'] = '后手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 1
                            data_1[str(对手)]['血量'] = 血量 - 伤害
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdd.send(Message('是实弹\n' +获取昵称(event.get_user_id())+ '是先手'))
                        else:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '后手'
                            data_1[str(对手)]['先手顺序'] = '先手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 0
                            data_1[str(对手)]['血量'] = 血量 - 伤害
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdd.send(Message('是实弹\n' + 获取昵称(对手) + '是先手'))
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '空弹':
                        if 手铐 == 2:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '先手'
                            data_1[str(对手)]['先手顺序'] = '后手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 1
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdd.send(Message('是空弹\n' +获取昵称(event.get_user_id())+'是先手'))
                        else:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '后手'
                            data_1[str(对手)]['先手顺序'] = '先手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 0
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdd.send(Message('是空弹\n' + 获取昵称(对手) + '是先手'))
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                    if 对局结束 == 1:
                        print('对局结束')
                    else:
                        await asyncio.sleep(1)
                        血1, 血2 = 双方信息(event.get_user_id(),对手)
                        子弹安排, 状态, 道具 = 子弹检查(对手,event.get_user_id())
                        if 状态 == 0:
                            await kqdd.send(Message('\n双方状态\n' +获取昵称(event.get_user_id())+ '血量：' + str(血1) + '\n' + 获取昵称(对手) + '血量：' + str(血2)))
                        elif 状态 == 1:
                            resp = await kqdd.send(Message('\n子弹分配完毕\n' + '空弹:' + str(子弹安排.count('空弹')) + '颗\n' + '实弹:' + str(子弹安排.count('实弹')) + '颗'))
                            await asyncio.sleep(1)
                            await kqdd.send(Message('\n双方状态\n' +获取昵称(event.get_user_id())+ '血量：' + str(血1) + '\n' + 获取昵称(对手) + '血量：' + str(血2)))
                            await kqdd.send(Message(道具))
                            await asyncio.sleep(9)
                            (bot,) = nonebot.get_bots().values()
                            await bot.delete_group_message(group_openid=event.group_openid, message_id=resp.id)
            else:
                await kqdd.send("您暂未加入对局")
    except FileNotFoundError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")
    except json.decoder.JSONDecodeError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")
    except KeyError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")

@kqdj.handle()
async def emlpkqdj(event: GroupAtMessageCreateEvent):
    try:

        子弹详情 = 'src/plugins/恶魔轮盘/匹配/子弹状况.txt'
        对局参数 = 'src/plugins/恶魔轮盘/匹配/匹配参数.txt'
        对局结束 = 2
        with open(子弹详情, "r", encoding="utf-8") as file_1:
            data_1 = json.load(file_1)
        with open(对局参数, "r", encoding="utf-8") as file_2:
            data_2 = json.load(file_2)
            血量 = data_1[str(event.get_user_id())]['血量']
            对手 = data_2[str(event.get_user_id())]['对手']
            伤害 = data_1[str(event.get_user_id())]['伤害']
            回合 = data_1[str(event.get_user_id())]['回合数']
            手铐 = data_1[str(event.get_user_id())]['手铐效果']
            对手血量 = data_1[str(对手)]['血量']
            if data_2[str(event.get_user_id())]['type'] == '正在进行':
                if data_1[str(event.get_user_id())]['先手顺序'] == '后手':
                    await kqdj.send(Message('还不是你的回合'))
                elif data_1[str(event.get_user_id())]['先手顺序'] == '先手':
                    if len(data_1[str(event.get_user_id())]['子弹安排']) == 0:
                        await kqdj.send(Message('请等待子弹补充完毕'))
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '实弹' and 血量 - 伤害 <=0:
                        del data_1[str(event.get_user_id())]['子弹安排'][0:]
                        del data_1[str(对手)]['子弹安排'][0:]
                        data_1[str(event.get_user_id())]['回合数'] = 1
                        data_1[str(对手)]['回合数'] = 1
                        data_2[str(event.get_user_id())]['type'] = '未开始'
                        data_2[str(对手)]['type'] = '未开始'
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                            file.close()
                        with open(对局参数, "w", encoding="utf-8") as file:
                            json.dump(data_2, file, indent=4)
                            file.close()
                            await kqdj.send(Message('恭喜' + 获取昵称(对手) + '获取胜利'))
                            赢 = 对局打分('赢', 回合, 对手血量)
                            输 = 对局打分('输', 回合, 血量)
                            个人信息录入(对手, 赢, event.get_user_id(), 输)
                            对局结束 = 1
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '实弹':
                        if 手铐 == 2:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '先手'
                            data_1[str(对手)]['先手顺序'] = '后手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 1
                            data_1[str(event.get_user_id())]['血量'] = 血量 - 伤害
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdj.send(Message('是实弹\n' +获取昵称(event.get_user_id())+ '是先手'))
                        else:
                            data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                            data_1[str(对手)]['子弹安排'].pop(0)
                            data_1[str(event.get_user_id())]['先手顺序'] = '后手'
                            data_1[str(对手)]['先手顺序'] = '先手'
                            data_1[str(event.get_user_id())]['手铐效果'] = 0
                            data_1[str(event.get_user_id())]['血量'] = 血量 - 伤害
                            data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                            await kqdj.send(Message('是实弹\n' + 获取昵称(对手) + '是先手'))
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                    elif data_1[str(event.get_user_id())]['子弹安排'][0] == '空弹':
                        data_1[str(event.get_user_id())]['子弹安排'].pop(0)
                        data_1[str(对手)]['子弹安排'].pop(0)
                        data_1[str(event.get_user_id())]['伤害'] = 1 + 回合//4
                        with open(子弹详情, "w", encoding="utf-8") as file:
                            json.dump(data_1, file, indent=4)
                        await kqdj.send(Message('是空弹\n' +获取昵称(event.get_user_id())+ '是先手'))
                    if 对局结束 == 1:
                        print('对局结束')
                    else:
                        await asyncio.sleep(1)
                        血1, 血2 = 双方信息(event.get_user_id(),对手)
                        子弹安排, 状态, 道具 = 子弹检查(对手,event.get_user_id())
                        if 状态 == 0:
                            await kqdd.send(Message('\n双方状态\n' +获取昵称(event.get_user_id())+ '血量：' + str(血1) + '\n' + 获取昵称(对手) + '血量：' + str(血2)))
                        elif 状态 == 1:
                            resp = await kqdd.send(Message('\n子弹分配完毕\n' + '空弹:' + str(子弹安排.count('空弹')) + '颗\n' + '实弹:' + str(子弹安排.count('实弹')) + '颗'))
                            await asyncio.sleep(1)
                            await kqdd.send(Message('\n双方状态\n' +获取昵称(event.get_user_id())+ '血量：' + str(血1) + '\n' + 获取昵称(对手) + '血量：' + str(血2)))
                            await kqdd.send(Message(道具))
                            await asyncio.sleep(9)
                            (bot,) = nonebot.get_bots().values()
                            await bot.delete_group_message(group_openid=event.group_openid, message_id=resp.id)
            else:
                await kqdd.send("您暂未加入对局")
    except FileNotFoundError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")
    except json.decoder.JSONDecodeError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")
    except KeyError:
            await kqdd.send("您暂未的对局暂未开始，该游戏为群友pvp游戏，可能是未匹配到群友")