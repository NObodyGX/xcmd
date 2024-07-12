import re
import os
import re
import unicodedata
import zhconv


class KWords(object):
    data = {
        # 数字
        r"(?<!\d)6(?=[地离续])|(?<=[大着内])6": "陆",
        # a
        r"(?i)(?<=[恋情])[aà]i|[aà]i(?=[情好惜心液])": "爱",
        # b
        r"(?i)(?<=[^a-zA-Z])bi[aǎ]o(?=[^a-zA-Z])": "婊",
        r"(?i)(?:(?<=[小的肏浪舔黑淫粉娘她大老说搔骚嫩抠扣的操曹干齐，])|(?<=[扣抠操曹干]着))(b[īi]|碧)(?![波绿幽玉人])|(b[īi]|碧)(?=[洞穴水腔口痒事肏里内上缝好][^港])": "屄",
        r"(?i)(?<=[傻牛])(b[iī]|\*|b)|(b[iī])(?=[上死我你近迫的])": "逼",
        # c
        r"(?i)(?:(?<=[曹我体贞节狠猛爆])(\*\*?|曹)|(\*\*?|曹))(?=[我你他场心蛋死得控练纵弄舟持盘守办刀劳着淡碧屄着烂])|艹|肏|(?<![a-zA-Z\s])c[aāà]o(?![a-zA-Z\s])": "操",
        r"(?i)揷(?=[槽头入拔座队送])|(?<=[拔抽强硬])揷|(?<![a-zA-Z\s])ch[āa](?![a-zA-Z\s])": "插",
        r"(?i)(?<=[全浑半上下]身)\*\*|\*\*(?=裸|[着的][\u4e00-\u9fa5]{0,2}身)|ch[iì]\s?lu[oǒ]": "赤裸",
        r"(?i)(?<=变)\*\*|ch[eé]ng\s?r[eé]n|诚仁|\*人": "成人",
        r"(?i)chu[aá]ng|[(（]床[)）]": "床",
        r"(?i)(?<=[叫发])ch[uú]n|ch[uú]n(?=[天风潮色情雨季雷心光梦])": "春",
        # d
        r"(?i)(?<=[阴旱上条大轨仙魔妖人])(\*|d[aà]o)|(\*|d[aà]o)(?=[韵理纹路理法上题教具歉])": "道",
        r"(?i)d[aà]ng": "荡",
        r"(?i)di[aà]n\s*?hu[aà]": "电话",
        r"(?<=[震振摇摆])d[oò]ng|d[oò]ng(?=[荡摇作手心])": "动",
        r"(?i)(?<=[空漏帘涵个])d[oò]ng|d[oò]ng(?=[口主开里门眼察])": "洞",
        # f
        r"(?i)f[eē]i\s*?w[eé]n": "绯闻",
        r"(?i)f[uú]\s*?w[uù]": "服务",
        # g
        r"(?i)(?<![a-zA-Z\s])g[aà]n(?![a-zA-Z\s])": "干",
        r"(?i)(gu[iī]|\*)(?=[头孙冠])": "龟",
        # h
        r"(?i)(?<=[心浪水])hu[aā]|hu[aā](?=[样式开椒招])": "花",
        r"(?i)(?<![a-z])hu[aá]ng": "黄",
        r"(?i)(?<=[精灵])h[uú]n|h[uú]n(?=[魄灵体])": "魂",
        r"(?i)(?<=[迷困疑蛊所])h[uù]o": "惑",
        # j
        r"(?i)(?<=[感冲刺过])j[iī]|j[iī](?=[动烈进昂战发怒增将化荡活情励光])": "激",
        r"(?i)(?<=呆若木)(\*+)|(\*+|吉)(?=巴)|(?<![a-zA-Z\s])j[iī](?![a-zA-Z\s])": "鸡",
        r"(?i)j[ií]\s*?p[iǐ]n": "极品",
        r"(?i)(?<=[迷强为老汉通先])(ji[āa]n|歼|j)|(ji[āa]n|歼)(?=[淫商情臣诈笑夫])": "奸",
        r"(?i)(?<=[人么是])ji[aà]n|ji[aà]n(?=[人货])": "贱",
        r"(?i)(?<=[艺名])(记|j[iì])|(记|j[iì])(?=[女院])": "妓",
        r"(?i)(奸|ji[aā]n)\s?(y[ií]n|淫)": "奸淫",
        r"(?i)(?<=[口性群肛乱])(ji[aā]o|佼)|(ji[aā]o|佼)(?=[流给待合火缠])": "交",
        r"(?i)(?<=[报示])j[iǐ]ng|j[iǐ]ng(?=[告示察官徽惕])": "警",
        r"(?i)j[iǐ]ng\s*?ch[aá]": "警察",
        r"(?i)(?<=[浓涉射白阳龙])(\*|x|婧)|(\*|x|婧|哔……)(?=[准细液腋力神灵怪魄确魂气血锐彩病华致关囊斑])|(?<![a-zA-Z\s])j[iī]ng(?![a-zA-Z\s])": "精",
        # k
        r"(?i)(?<![a-zA-Z\s])k[aà]o(?![a-zA-Z\s])": "靠",
        r"(?i)(?<=[港金破可开井借进户收关住变闭])(k[oǒ]u|\*)|(k[oǒ]u|\*)(?=[才交福里袋唇破齿舌牙])": "口",
        # l
        r"(?i)l[ií]u\s*?m[aá]ng": "流氓",
        r"(?i)(?<=[赤裸])l[uǔ]o|l[uǔ]o(?=[贷退辞露睡体奔着机船])": "祼",
        # m
        r"m[eé]n": "门",
        # n
        r"(?i)(?<=[牛羊马豆白大揉硕])(n[aǎ]i|乃)|(n[aǎ]i|乃)(?=[子头奶瓶茶粉罩滴])": "奶",
        r"(?i)(?<=[捉玩摆])n[oò]ng|n[oò]ng(?=[虚手臣明点权])": "弄",
        r"(?i)(?<=[一男儿淑美少处])n[vǚu]|n[vǚu](?=[人孩子士儿子官装性帝王奴])": "女",
        # p
        r"(?i)(?<![\da-zA-Z\s])pi?(?![\da-zA-Z\s])": "屁",
        # q
        r"(?i)qi[aá]ng\s*?ji[aā]n|强\*奸": "强奸",
        r"(?i)(?<![a-zA-Z\s])qi[aā]ng(?![a-zA-Z\s])": "枪",
        r"(?i)qi[aà]ot[uú]n": "翘臀",
        r"(?i)qing\s?ren": "情人",
        r"(?i)q[uú]n(?=[体落居奸主里交pP])|(?<=[族超种人])q[uú]n": "群",
        # r
        r"(?i)(?<![a-zA-Z\s])r[eè](?![a-zA-Z\s])": "热",
        r"(?i)(?<![a-zA-Z])r[iì]|r[iì](?![a-zA-Z])|(?<=[每时几昨今前明早当百千好一二三四五六七八九十两近平假生往次春夏秋冬周昔翌度蔽隔逐值吉改天末终他曰日整数我那这白旧指来择半某异烈多])曰|曰(?=[子期月志记常历后趋渐程落光晷晕省曰日强近头出])": "日",
        r"(?i)(?<=[嫩肌血赘美软])\*|\*(?=[乎感囊袋珠柱棍杵菇壶筋浪壁膜唇缝洞盾末棒体便穴眼])|內|(?<![a-z])r[oò]u(?![a-z])": "肉",
        r"(?<=[母美酥椒淑嫩哺娇双左右粉玉白面浴酸牛钟])(r[uǔ])|(r[uǔ])(?=[牛酪酸业腺燕臭鸽猪制名母牙白头峰肉房晕球尖])": "乳",
        # s
        r"(?i)(?:(?<=[好发牢风闷真淫])|(?<=这么)|(?<=他妈的))(s[aā]o|搔)|(s[aā]o|搔)(?=[碧穴动气乱扰气客话得货叫心])": "骚",
        r"(?i)(?<![a-zA-Z\s])s[èe](?![a-zA-Z\s])": "色",
        r"(?i)(?<![a-zA-Z\s])sh[aà]ng(?![a-zA-Z\s])": "上",
        r"(?i)(杀|sh[aā])\s?(戮|l[uù])": "杀戮",
        r"(?i)sh[aā]\s*?r[eé]n": "杀人",
        r"(?i)(?<=[弹发暗颜影注喷反辐放散])涉|涉(?=[精婧箭日击程手向弓往回在去哪那这不手射给墙到了进出入])|(?<![a-z\s])sh[eè](?![a-z\s])": "射",
        r"(?i)sh[eē]n\s?y[ií]n|(?<=再一次)\*\*": "呻吟",
        r"(?i)sh[eē]n(?=[展手出开过舌])|(?<=[延])sh[eē]n": "伸",
        r"(?i)(?<![a-zA-Z\s])sh[eē]n(?![a-zA-Z\s])": "身",
        # t
        r"(?i)(?<![a-zA-Z\s])t[aà]o(?![a-zA-Z\s])": "套",
        r"(?i)(?<=[大小])tu[iǐ]|tu[iǐ](?=[部上软])": "腿",
        # x
        r"(?i)xi[aáǎ]o\s*?ji[eě]": "小姐",
        r"(?i)(?<=[好真])xi[aǎ]o|xi[aǎ]o(?=[小姐看穴瞧逼人心])": "小",
        r"(?i)(?:(?<=[大丰白的心鸡])|(?<=成竹在|昂首挺))(xi[oō]ng|詾)|(xi[oō]ng|詾)(?=[罩前膛腔口脯部肌围大有针怀襟府闷腹膛腔贴甲毛])": "胸",
        # r"(?i)(?<![a-zA-Z\s])(x[iì]ng|xg)(?![a-zA-Z\s])|(?:(?<=[种属中共惰根知本记心随习悟生恶毒定德弹邪雅男女品烈水血任惯同诗养])|(?<=可能|象征|扫了|真实|重要|自发|正当|地域|排他|务实|排斥|幻想|骚扰))": "性",
        r"(?i)x[iì]ng\s*?g[aǎ]n": "性感",
        r"(?i)(?<=oo)\*\*|\*\*(?=oo)": "xx",
        # y
        r"(?i)(?<=[奇手奸邪侵意宣荒])(y[ií]n|银)|(y[ií]n|银)(?=[声水液腋辱呻浪靡糜猥亵叫邪媚荡乱秽穴具僧魔妇贼娃搔骚贱威逸祠祀技词才窝毒棍巧乐])|婬": "淫",
        r"(?<=[太光元女遮真下外内])(y[iī]n|\*|陰)|(y[iī]n|(?<!\*)\*|陰)(?=[唇核部森沉蒂道户穴阳精历霾暗干面凉影谋毒险湿天魂寒文晦冷骘唇毛世间风囊茎洞])": "阴",
        r"(y[áa]ng|\*)(?=[物气根刚光具])": "阳",
        r"(?i)y[īi]n\s?j[īi]ng": "阴茎",
        r"(?i)y[oò]u\s*?hu[oò]": "诱惑",
        r"(?i)(?:(?<=[情思私淫节肉贪爱性姓纵兽])|(?<=求生))(y[uù]|裕|\*\*?|慾)|(y[uù]|裕|\*\*?|慾)(?=[火情心求虑试望壑寡欲女仙色拒念海焰])": "欲",
        r"(?i)y[uù]\s?w[aà]ng|欲w[aà]ng|(?:(?<=[的么和])|(?<=攻击))\*\*(?!\*)": "欲望",
        # z
        r"(?i)(?<=[真])zh[eè]ng": "正",
        r"(?i)(?<=[求帮])zh[ùu]": "助",
        r"(?i)z[ìi]\s?y[óo]u": "自由",
        r"(?i)zu[oò](?=[爱])": "做",
        # *
        # (?<=a|bc) 应重写为 (?:(?<=a)|(?<=bc)))
        r"(?:(?<=捏我的|撅起了))\*\*": "屁股",
        r"巨\*": "巨大",
        r"\*轮": "法轮",
        r"(?:(?<=两只|粉色)|(?<=饱满的))\*\*|\*\*(?=乱颤)": "乳房",
        r"(?:(?<=[洞巢虎深小美嫩墓窍])|(?<=百会|神庭|玉枕|膻中|[巨神]阙|气海|关元|中极|尾闾|天[突柱]|璇玑|紫宫|肩进|太渊|涌泉|[风曲]池|灵台|眉心|[周通]天))\*|宍": "穴",
        # 合并
        r"氵朝": "潮",
        # 全角字符转换为半角字符
        r"Ａ": "A",
        r"Ｂ": "B",
        r"Ｃ": "C",
        r"Ｄ": "D",
        r"Ｅ": "E",
        r"Ｆ": "F",
        r"Ｇ": "G",
        r"Ｈ": "H",
        r"Ｉ": "I",
        r"Ｊ": "J",
        r"Ｋ": "K",
        r"Ｌ": "L",
        r"Ｍ": "M",
        r"Ｎ": "N",
        r"Ｏ": "O",
        r"Ｐ": "P",
        r"Ｑ": "Q",
        r"Ｒ": "R",
        r"Ｓ": "S",
        r"Ｔ": "T",
        r"Ｕ": "U",
        r"Ｖ": "V",
        r"Ｗ": "W",
        r"Ｘ": "X",
        r"Ｙ": "Y",
        r"Ｚ": "Z",
        r"ａ": "a",
        r"ｂ": "b",
        r"ｃ": "c",
        r"ｄ": "d",
        r"ｅ": "e",
        r"ｆ": "f",
        r"ｇ": "g",
        r"ｈ": "h",
        r"ｉ": "i",
        r"ｊ": "j",
        r"ｋ": "k",
        r"ｌ": "l",
        r"ｍ": "m",
        r"ｎ": "n",
        r"ｏ": "o",
        r"ｐ": "p",
        r"ｑ": "q",
        r"ｒ": "r",
        r"ｓ": "s",
        r"ｔ": "t",
        r"ｕ": "u",
        r"ｖ": "v",
        r"ｗ": "w",
        r"ｘ": "x",
        r"ｙ": "y",
        r"ｚ": "z",
        r"１": "1",
        r"２": "2",
        r"３": "3",
        r"４": "4",
        r"５": "5",
        r"６": "6",
        r"７": "7",
        r"８": "8",
        r"９": "9",
        r"０": "0",
        r"＋": "+",
        r"／": "/",
        r"＃": "#",
        r"％": "%",
        r"￥": "¥",
        r"＠": "@",
        r"＄": "$",
        r"＆": "&",
        # 垃圾去除
        r"免费电子书下载": "",
        r"[电子书|免费小说]在线阅读": "",
        r"(?i)免费txt小说下载": "",
        r"(?i)txt电子书下载": "",
        r"(?i)好看的txt电子书": "",
        r"九味书屋": "",
        r"笔下文学": "",
        r"(?i)www.bxwx.[a-zA-Z][a-zA-Z]": "",
        r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""": "",
        # 符号
        r"\(）": "",
        r"（\)": "",
        r"\(\)": "",
        r"（）": "",
        r"```": "",
        # 替换冒号
        r":": "：",
        # 替换逗号
        r",": "，",
        # 将数字里带着的o改为0
        r"(?<=\d)o": "0",
    }

    @staticmethod
    def clean(content):
        for key, value in KWords.data.items():
            content = re.sub(key, value, content)
        return content


class Symbol(object):
    lquote = "「"
    rquote = "」"
    lquoter = "♕"
    rquoter = "♔"
    wrap = "\n\n"
    period = "。"
    comma = "，"
    speak = "："
    end = "。 ？ ！ ； ： … ——"


class GNovelFormator(object):
    def __init__(self, odirname: str = ".", merge_short=False) -> None:
        self.odirname = os.path.normpath(os.path.abspath(odirname))
        self.is_merge_short = bool(merge_short)

        self.title = ""
        self.author = ""

    def load_book(self, fullname):
        lines = []
        for ecd in ("gbk", "utf-8", "gb18030", "utf-16", "utf-32"):
            try:
                with open(fullname, "r", encoding=ecd) as f:
                    lines = f.readlines()
            except UnicodeDecodeError as e:
                pass
            else:
                break
        if not lines:
            print(f"读取 {fullname} 编码错误")
        return lines

    def match_replace_init(self):
        self.m_pos = 0
        self.m_flag = True

    def match_replace_half(self, match: re.Match):
        if match.start() - self.m_pos > 88:
            self.m_flag = True
        self.m_pos = match.start()
        if self.m_pos > 3:
            t = match.string[self.m_pos - 3 : self.m_pos]
            if t.endswith("："):
                self.m_flag = True
            elif t.endswith(Symbol.wrap):
                self.m_flag = True
        result = Symbol.lquoter if self.m_flag else Symbol.rquoter
        self.m_flag = not self.m_flag
        return result

    def format_speak(self, content: str):
        """将无左右符号区分的改为说话字符"""
        for char in ("`", '"'):
            self.match_replace_init()
            # 1. 将所有字符统一改为左引号符号
            content = re.sub(char, Symbol.lquoter, content)
            # 2. 隔一个将左字符替换为右，如果超过了80个字符，不变
            content = re.sub(Symbol.lquoter, self.match_replace_half, content)
            # 3. 如果有字符前面是：，将右字符替换为左字符
            # 4. 替换左右引号符号替换为真正的引号字符
            content = re.sub(Symbol.lquoter, Symbol.lquote, content)
            content = re.sub(Symbol.rquoter, Symbol.rquote, content)
        # 将 rquote 前面的 wrap 替换掉
        # 这个最好多次比较好
        content = re.sub(f"{Symbol.wrap}{Symbol.rquote}", f"{Symbol.rquote}", content)
        content = re.sub(f"{Symbol.wrap}{Symbol.rquote}", f"{Symbol.rquote}", content)
        content = re.sub(f"{Symbol.wrap}{Symbol.rquote}", f"{Symbol.rquote}", content)
        return content

    def format_line(self, line: str):
        """清理每一行的字符"""
        nnn = zhconv.convert(line.strip(), "zh-cn")
        # 归一化处理所有 http 的字符
        nnn = unicodedata.normalize("NFC", nnn)
        if nnn.startswith(self.title):
            nnn = nnn.replace(self.title, "", 1)
        if nnn.startswith(f"【{self.title}】"):
            nnn = nnn.replace(f"【{self.title}】", "", 1)
        nnn = re.sub(r"[　]", "", nnn)
        nnn = re.sub(r"[“\[]", Symbol.lquote, nnn)
        nnn = re.sub(r"[”\]]", Symbol.rquote, nnn)
        nnn = re.sub(r"‘", Symbol.lquote, nnn)
        nnn = re.sub(r"’", Symbol.rquote, nnn)
        nnn = re.sub(r"(~{3,})", r"~~", nnn)  # markdown 注释格式
        return nnn

    def clean_title(self, line: str):
        line = " ".join(line.replace("章，", "章").replace("章", "章 ", 1).split()).strip()
        line = line.replace("{", "·").replace("}", "")
        line = line.replace("｛", "·").replace("｝", "")
        line = line.replace("（", "·").replace("）", "")
        line = line.replace("(", "·").replace(")", "")
        line = line.replace("、", "").replace("：", "")
        line = line.replace("章 ·", "章 ")
        line = line.replace("章 章", "章 ")
        line = line.replace(" ·", "·")
        line = line.replace(":", "")
        return "## " + line

    def format_if_long(self, line: str):
        """清理过长的字符串"""
        if len(line) < 300:
            return line
        add_period = True if line.endswith(Symbol.period) else False
        nwords = re.split(f"({Symbol.period})", line)
        nline = ""
        length = 0
        for word in nwords:
            if word == Symbol.period:
                if length >= 80:
                    nline += word + Symbol.wrap
                    length = 0
                continue
            if word.startswith(Symbol.rquote):
                if nline.endswith(Symbol.wrap):
                    nline = nline.rstrip(Symbol.wrap) + word[0] + Symbol.wrap
                    word = word[1:]
            nline += word
            length += len(word)
        if add_period:
            nline += Symbol.period
        return nline

    def format_if_title(self, line: str):
        """识别并标题字符"""
        if line.startswith("#"):
            return line
        # 1. 简介标题
        for x in ("正文简介", "内容简介"):
            if line.find(x) <= -1:
                continue
            laterline = line[line.find(x) + len(x) :].strip("【】：，[]:,")
            line = f"## 内容简介\n\n{laterline}".strip()
            return line
        # 2. 正文标题
        if line.startswith("正文"):
            if len(line) <= 2:
                return ""
            if line[2] == " ":
                line = line.replace("正文", "", 1).strip()
            if len(line) > 2 and line[2].isdecimal():
                i = 2
                for i in range(2, 10, 1):
                    if len(line) <= i:
                        break
                    if not line[i].isdecimal():
                        break

                line = line[:i] + "章 " + line[i:]
                line = line.replace("正文", "第", 1)
                line = line.replace("；", "")
                line = self.clean_title(line)
                return line
        # 3. 第 xxx 章 xxxx
        patterns1 = (
            r"^第[\d０-９零一二三四五六七八九十百千万]+章",
            r"^第[\d０-９零一二三四五六七八九十百千万]+章\s*([\u4e00-\u9fa5]+[\u4e00-\u9fa5\s]*)$",
        )
        # 4. （xxxxx） xxxx
        patterns2 = (r"^\（[\d０-９零一二三四五六七八九十百千万]+\）.*",)
        for pattern in patterns1:
            m = re.match(pattern, line)
            if not bool(m):
                continue
            line = self.clean_title(line)
            return line
        for pattern in patterns2:
            m = re.match(pattern, line)
            if not bool(m):
                continue
            line = line.replace("（", "第", 1).replace("）", "章", 1)
            line = self.clean_title(line)
            return line
        return line

    def format_if_end(self, line: str):
        """修正最后的完结字符"""
        for x in ("全书完", "全文完", "【完结】", "【完】", "（完）"):
            if line.find(x) >= 0:
                line = line[: line.find(x)].strip("【】") + Symbol.wrap + "## 全书完"
                break
        for x in ("【待续】", "（待续）", "【未完待续】"):
            if line.find(x) >= 0:
                line = line[: line.find(x)].strip("【】") + Symbol.wrap + "## 待续"
                break
        return line

    def format_wrap(self, line: str):
        """默认情况下换行，如果为特殊字符，则不应该换行"""
        if not self.is_merge_short:
            if line.endswith("，"):
                return line.rstrip()
            return line + Symbol.wrap
        if line.startswith("#"):
            return Symbol.wrap + line + Symbol.wrap
        for ends in ("。", "！", "？", ".", "”", "」", "……"):
            if line.endswith(ends):
                return line + Symbol.wrap
        return line.rstrip()

    def get_title_author(self, bname: str):
        """从文件名获取标题和作者名称"""
        title = bname
        index = bname.find("作者")
        if index > 0:
            title = bname[:index]
            self.author = bname[index + 2 :].strip(" \r\n\t【】[]()-：")
        # 如果有《》则直接取里面的内容作为标题
        ntitle = re.findall(r"《(.*?)》", title)
        if ntitle:
            self.title = ntitle[0]
            return
        # 去除【】及其中间的内容
        title = re.sub(r"\【.*?\】", "", title)
        self.title = title.strip(" \r\n\t《》[]()-")

    def try_add_title_author(self, content: str):
        index = content.find(Symbol.wrap)
        line = content[:index]
        if line.startswith("#"):
            return content
        if not self.title:
            return content
        title = ""
        if line.find(self.title) >= 0 and len(line) < len(self.title) + 5:
            line = ""
        title = f"# {self.title}"
        if not self.author:
            return title + content[index:]
        title = title + Symbol.wrap + f"作者：{self.author}"
        return title + content[index:]

    def get_suffix(self, fullname) -> str:
        fsize = os.path.getsize(fullname)
        if fsize < 100 * 1024:
            return "短篇·"
        return ""

    def reformat(self, fullname: str):
        nlines = []
        title, _ = os.path.splitext(os.path.basename(fullname))
        self.get_title_author(title)
        for _line in self.load_book(fullname):
            line = self.format_line(_line)
            if not line:
                continue
            line = self.format_if_title(line)
            line = self.format_if_end(line)
            line = self.format_if_long(line)
            line = self.format_wrap(line)
            nlines.append(line)
        banename, _ = os.path.splitext(os.path.basename(fullname))

        suffix = self.get_suffix(fullname)
        ofile = suffix + self.title + ".md" if self.title else banename + ".md"
        nfullname = os.path.join(self.odirname, ofile)
        # 最后再整体进行字符串替换修改
        content = "".join(nlines)
        content = KWords.clean(content)
        content = self.format_speak(content)
        content = self.try_add_title_author(content)
        with open(nfullname, "w+", encoding="utf-8") as f:
            f.write(content)

    def work(self, fullpath: str):
        if os.path.isfile(fullpath) and fullpath.lower().endswith(".txt"):
            self.reformat(fullpath)
            return
        if not os.path.isdir(fullpath):
            return
        for entry in os.scandir(fullpath):
            if not entry.is_file():
                continue
            if not entry.name.endswith(".txt"):
                continue
            if entry.name == "requirements.txt":
                continue
            self.reformat(entry.path)


def g_file_format_text(ifile="", odir="", merge_short=False):
    """
    ifile: 输入文件或者输入文件夹
    odir: 输出文件夹
    merge_short: 是否自动合并短句
    """
    if not os.path.exists(ifile):
        return
    if os.path.isfile(ifile):
        if not ifile.lower().endswith(".txt"):
            return
    if not odir:
        odir = ifile if os.path.isdir(ifile) else os.path.dirname(ifile)
    formator = GNovelFormator(odir, merge_short=merge_short)
    formator.work(ifile)
