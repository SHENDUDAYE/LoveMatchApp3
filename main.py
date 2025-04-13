import streamlit as st
from datetime import datetime, date

# 基础数据和映射
stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
zodiac_map = {"子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔", "辰": "龙", "巳": "蛇", "午": "马", "未": "羊", "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"}
cycle60 = [stems[i % 10] + branches[i % 12] for i in range(60)]
solar_term_start = {1: 5, 2: 4, 3: 6, 4: 5, 5: 5, 6: 6, 7: 7, 8: 7, 9: 7, 10: 8, 11: 7, 12: 7}
branch_to_monthnum = {"寅": 1, "卯": 2, "辰": 3, "巳": 4, "午": 5, "未": 6, "申": 7, "酉": 8, "戌": 9, "亥": 10, "子": 11, "丑": 12}
stem_to_element = {'甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土', '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'}
nayin_list = [
    ("海中金", "金"), ("炉中火", "火"), ("大林木", "木"), ("路旁土", "土"), ("剑锋金", "金"),
    ("山头火", "火"), ("涧下水", "水"), ("城头土", "土"), ("白蜡金", "金"), ("杨柳木", "木"),
    ("泉中水", "水"), ("屋上土", "土"), ("霹雳火", "火"), ("松柏木", "木"), ("长流水", "水"),
    ("砂中金", "金"), ("山下火", "火"), ("平地木", "木"), ("壁上土", "土"), ("金箔金", "金"),
    ("覆灯火", "火"), ("天河水", "水"), ("大驿土", "土"), ("钗钏金", "金"), ("桑柘木", "木"),
    ("大溪水", "水"), ("沙中土", "土"), ("天上火", "火"), ("石榴木", "木"), ("大海水", "水")
]
# 生肖配对关系
liuhe_pairs = {("鼠", "牛"), ("虎", "猪"), ("兔", "狗"), ("龙", "鸡"), ("蛇", "猴"), ("马", "羊")}
liuchong_pairs = {("鼠", "马"), ("牛", "羊"), ("虎", "猴"), ("兔", "鸡"), ("龙", "狗"), ("蛇", "猪")}
liuhai_pairs = {("鼠", "羊"), ("牛", "马"), ("虎", "蛇"), ("兔", "龙"), ("狗", "鸡"), ("猴", "猪")}
all_liuhe = liuhe_pairs.union({(b, a) for a, b in liuhe_pairs})
all_liuchong = liuchong_pairs.union({(b, a) for a, b in liuchong_pairs})
all_liuhai = liuhai_pairs.union({(b, a) for a, b in liuhai_pairs})
liuhai_active = {("鼠", "羊"): "羊", ("牛", "马"): "牛", ("虎", "蛇"): "蛇", ("兔", "龙"): "兔", ("狗", "鸡"): "鸡", ("猴", "猪"): "猪"}
for (a, b), val in list(liuhai_active.items()):
    liuhai_active[(b, a)] = val
liuchong_dom = {("鼠", "马"): "鼠", ("虎", "猴"): "猴", ("兔", "鸡"): "鸡", ("蛇", "猪"): "猪", ("牛", "羊"): None, ("龙", "狗"): None}
for (a, b), val in list(liuchong_dom.items()):
    liuchong_dom[(b, a)] = val
triad_groups = [
    (["鼠", "龙", "猴"], "水"),
    (["牛", "蛇", "鸡"], "金"),
    (["虎", "马", "狗"], "火"),
    (["兔", "羊", "猪"], "木")
]
# 五行配对诗句
verses = {
    "金": {
        "金": "好处多、夫妻恩爱笑呵呵、儿女随心又满意、晚年康乐福寿多。",
        "木": "合得来、两人和好笑颜开、如果双双再一起、五男两女有高颜。",
        "火": "不相当、半路相克离故乡、两人相吵不安康，互相原谅呈吉祥。",
        "土": "多美好、荣华富贵白老一生幸福多欢乐，一对夫妻白头老。",
        "水": "老高强，夫妻相合寿命长，五男两女金满堂，手中有钱又有粮。"
    },
    "水": {
        "水": "共平衡，两人欢乐再一起，各水溪流呈最底，呈不吉利，但守财。",
        "金": "好夫妻、双双荣华共一处，女穿金多高贤，皆把福德传儿孙。",
        "火": "不成双，水火相遇似虎狼，男水女火更不成，有似钱财多损伤。",
        "土": "不相配，夫妻言语争高强，生儿育女多辛苦，相互原谅呈吉祥。",
        "木": "多相好、才华玉地自然来、同床金发相和好，田园牛马满仓宅。"
    },
    "木": {
        "木": "不相当，两木相比不一样，越是夫妻随心愿，自然相克受损伤。",
        "水": "同合愿，一双如水鱼，男女相合且安康，金银财宝是钱粮。",
        "土": "不和心，牛马相合不安分，外交友费口舌，夫妻之间不安分。",
        "火": "能成双，木火相遇能运旺，儿女双全好风光，夫妻和睦好逍遥。",
        "金": "不相配，半路争吵去他乡，结合一处不安康，子女稀少不相当。"
    },
    "火": {
        "火": "两不详，两火之间有高强，人人都说相当好，到头总是不安宁。",
        "土": "是守财，福禄鸳鸯送颜开，夫妻同床仁帷帐，总是青梅竹马婿。",
        "金": "两不详，犹如针尖对麦芒，男女到老无依靠，离分悲惨悔断肠。",
        "木": "似可成，相互原谅福终生，有了贵子贵孙旺，福禄鸳鸯得安宁。",
        "水": "相当好，两戏两鱼两鸳鸯，财粮好衣多多进，儿女双全好风光。"
    },
    "土": {
        "土": "好夫妻、夫妻和好与齐全，男女穿金有代玉，百年夫妻不分离。",
        "水": "难成行、牛马相逢不相当，口舌常见多吵闹，影响家中儿女郎。",
        "金": "合得来、男女和好笑颜开，五男两女富贵财，前生配得好成双。",
        "木": "似不昌、夫妻相克不安当，全家不安儿女少，财来财去不安康。",
        "火": "发大财、金银财宝满仓宅，奉得贵子贤孙旺，福禄双旺伴颜良。"
    }
}

def get_four_pillars(y: int, m: int, d: int, h: int, mi: int) -> dict:
    """将阳历年月日时转换为四柱八字（年、月、日、时）。"""
    # 年柱：根据立春调整年份
    year_for_bazi = y
    if (m < 2) or (m == 2 and d < 4):
        year_for_bazi -= 1
    year_index = (year_for_bazi - 4) % 60
    year_pillar = stems[year_index % 10] + branches[year_index % 12]
    # 月柱：根据节气确定月支
    if m == 1:
        month_branch = "丑" if d >= solar_term_start[1] else "子"
    else:
        mb = None
        sd = solar_term_start.get(m)
        if sd:
            if d >= sd:
                # 当月节气已过，取当月地支
                mb = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"][m - 2]
            else:
                # 节气未到，仍用上个月地支
                mb = ["丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子"][m - 2]
        else:
            # 保底处理（通常不会执行到）
            mb = ["丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子"][m - 2]
        month_branch = mb
    # 月干：根据当年年干推算
    year_stem_index = (year_for_bazi - 4) % 10
    tiger_stem_index = ((year_stem_index % 5) * 2 + 2) % 10  # 立春（寅月）天干索引
    month_num = branch_to_monthnum[month_branch]
    month_stem = stems[(tiger_stem_index + month_num - 1) % 10]
    month_pillar = month_stem + month_branch
    # 日柱：以1900-01-31为起点（甲子日），计算偏移
    base_date = date(1900, 1, 31)
    diff_days = (date(y, m, d) - base_date).days
    day_index = diff_days % 60
    day_pillar = stems[day_index % 10] + branches[day_index % 12]
    # 时柱：根据日干和出生小时确定
    if h == 23 or h == 0:
        hour_branch = "子"
    elif 1 <= h <= 2:
        hour_branch = "丑"
    elif 3 <= h <= 4:
        hour_branch = "寅"
    elif 5 <= h <= 6:
        hour_branch = "卯"
    elif 7 <= h <= 8:
        hour_branch = "辰"
    elif 9 <= h <= 10:
        hour_branch = "巳"
    elif 11 <= h <= 12:
        hour_branch = "午"
    elif 13 <= h <= 14:
        hour_branch = "未"
    elif 15 <= h <= 16:
        hour_branch = "申"
    elif 17 <= h <= 18:
        hour_branch = "酉"
    elif 19 <= h <= 20:
        hour_branch = "戌"
    elif 21 <= h <= 22:
        hour_branch = "亥"
    else:
        hour_branch = "子"
    day_stem = day_pillar[0]
    if day_stem in ["甲", "己"]:
        base_hour_stem = "甲"
    elif day_stem in ["乙", "庚"]:
        base_hour_stem = "丙"
    elif day_stem in ["丙", "辛"]:
        base_hour_stem = "戊"
    elif day_stem in ["丁", "壬"]:
        base_hour_stem = "庚"
    elif day_stem in ["戊", "癸"]:
        base_hour_stem = "壬"
    base_index = stems.index(base_hour_stem)
    hour_index = branches.index(hour_branch)
    hour_stem = stems[(base_index + hour_index) % 10]
    hour_pillar = hour_stem + hour_branch
    return {"year": year_pillar, "month": month_pillar, "day": day_pillar, "hour": hour_pillar}

# 配置 Streamlit 页面
st.set_page_config(page_title="Love Match 婚配分析系统", layout="centered")
st.title("Love Match 婚配分析系统")
st.write("请输入男女双方的出生阳历日期和时间，然后点击 **开始分析**，即可查看婚配分析结果。")

# 输入栏
col1, col2 = st.columns(2)
with col1:
    st.markdown("**男方出生日期和时间**")
    male_date = st.date_input("男方出生日期", value=date(1990, 1, 1), key="male_date")
    male_time = st.time_input("男方出生时间", value=datetime(1990, 1, 1, 0, 0).time(), key="male_time")
with col2:
    st.markdown("**女方出生日期和时间**")
    female_date = st.date_input("女方出生日期", value=date(1990, 1, 1), key="female_date")
    female_time = st.time_input("女方出生时间", value=datetime(1990, 1, 1, 0, 0).time(), key="female_time")

# 点击分析按钮
if st.button("开始分析"):
    male_bazi = get_four_pillars(male_date.year, male_date.month, male_date.day, male_time.hour, male_time.minute)
    female_bazi = get_four_pillars(female_date.year, female_date.month, female_date.day, female_time.hour, female_time.minute)
    male_zodiac = zodiac_map[male_bazi['year'][1]]
    female_zodiac = zodiac_map[female_bazi['year'][1]]
    male_element = stem_to_element[male_bazi['year'][0]]
    female_element = stem_to_element[female_bazi['year'][0]]
    male_year_idx = cycle60.index(male_bazi['year'])
    female_year_idx = cycle60.index(female_bazi['year'])
    male_nayin_name, male_nayin_elem = nayin_list[male_year_idx // 2]
    female_nayin_name, female_nayin_elem = nayin_list[female_year_idx // 2]
    verse_text = verses[male_element][female_element]
    # 五行诗句现代解读
    relation_desc = ""
    gen_map = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    ovr_map = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
    if male_element == female_element:
        relation_desc = f"双方五行同属{male_element}，"
    elif gen_map[male_element] == female_element:
        relation_desc = f"男方{male_element}生女方{female_element}，"
    elif gen_map[female_element] == male_element:
        relation_desc = f"女方{female_element}生男方{male_element}，"
    elif ovr_map[male_element] == female_element:
        relation_desc = f"男方{male_element}克女方{female_element}，"
    elif ovr_map[female_element] == male_element:
        relation_desc = f"女方{female_element}克男方{male_element}，"
    # 判断诗句正负倾向
    is_positive = any(word in verse_text for word in ["合得来", "好夫妻", "相当好", "和睦", "恩爱", "富贵", "满堂", "寿命长", "儿女双全", "五男两女"])
    is_negative = any(word in verse_text for word in ["不相", "不成", "不和", "不安", "相克", "争", "吵", "离", "无依靠", "难成", "不吉利"])
    expl = ""
    if is_positive:
        expl = "二人性情相合，婚姻美满，家运兴旺。"
    elif is_negative:
        expl = "二人关系不够融洽，婚后容易产生矛盾，需要多包容理解。"
    else:
        expl = "二人关系中等，婚姻需要双方用心经营。"
    expl = relation_desc + expl
    # 生肖配对分析文本
    relation_text = ""
    if (male_zodiac, female_zodiac) in all_liuhe:
        relation_text = f"男方属{male_zodiac}，女方属{female_zodiac}，双方生肖构成**六合**关系，是一对上等婚配。冥冥之中两人相处和谐融洽，彼此愿意付出，婚姻生活幸福甜美。"
    elif (male_zodiac, female_zodiac) in all_liuchong:
        dom = liuchong_dom.get((male_zodiac, female_zodiac))
        if dom is None:
            dom_info = "势均力敌，难分高下，"
        else:
            dom_info = f"{dom}方往往占上风，"
        relation_text = f"男方属{male_zodiac}，女方属{female_zodiac}，双方生肖**六冲**，天生不合。{dom_info}婚姻中冲突频繁，争吵将成为主旋律，感情易在矛盾中受伤。"
    elif (male_zodiac, female_zodiac) in all_liuhai:
        active = liuhai_active.get((male_zodiac, female_zodiac), "")
        active_info = f"{active}方常为主动挑起矛盾，" if active else ""
        relation_text = f"男方属{male_zodiac}，女方属{female_zodiac}，属于**六害**组合，暗含分离和冲突之象，{active_info}感情基础不稳，需格外珍惜维系。"
    else:
        same_trio_elem = None
        for trio, elem in triad_groups:
            if male_zodiac in trio and female_zodiac in trio:
                same_trio_elem = elem
                break
        if same_trio_elem:
            relation_text = f"男方属{male_zodiac}，女方属{female_zodiac}，双方生肖为**三合**关系，志趣相投，容易和睦相处，共创美满生活。"
        else:
            relation_text = f"男方属{male_zodiac}，女方属{female_zodiac}，生肖无刑冲害合，配对属中等平配。婚姻好坏取决于双方用心经营。"
    # 婚配评分计算
    score = 60
    if (male_zodiac, female_zodiac) in all_liuhe:
        score += 20
    if (male_zodiac, female_zodiac) in all_liuchong:
        score -= 20
    if (male_zodiac, female_zodiac) in all_liuhai:
        score -= 15
    same_trio = any(male_zodiac in trio and female_zodiac in trio for trio, elem in triad_groups)
    if same_trio:
        score += 15
    if gen_map[male_element] == female_element or gen_map[female_element] == male_element:
        score += 10
    if ovr_map[male_element] == female_element or ovr_map[female_element] == male_element:
        score -= 10
    if male_nayin_elem == female_nayin_elem:
        score += 5
    elif gen_map.get(male_nayin_elem) == female_nayin_elem or gen_map.get(female_nayin_elem) == male_nayin_elem:
        score += 5
    elif ovr_map.get(male_nayin_elem) == female_nayin_elem or ovr_map.get(female_nayin_elem) == male_nayin_elem:
        score -= 5
    score = max(0, min(100, score))
    if score >= 85:
        score_comment = "极佳"
    elif score >= 70:
        score_comment = "较好"
    elif score >= 50:
        score_comment = "中等"
    elif score >= 30:
        score_comment = "较差"
    else:
        score_comment = "极差"
    score_text = f"{score} / 100（{score_comment}）"
    # 推荐婚期
    wedding_text = ""
    recommended = []
    for trio, elem in triad_groups:
        if male_zodiac in trio and female_zodiac in trio:
            third = [x for x in trio if x not in [male_zodiac, female_zodiac]][0]
            season = {"火": "夏季", "木": "春季", "水": "冬季", "金": "秋季"}[elem]
            wedding_text = f"建议选择**{third}年**完婚，可与双方属相形成三合局，寓意五行{elem}旺，婚后运势更佳。婚礼择在{season}举行，更加吉利。"
            recommended.append(third)
            break
    if not wedding_text:
        if (male_zodiac, female_zodiac) in all_liuhe:
            male_trio = next(trio for trio, elem in triad_groups if male_zodiac in trio)
            female_trio = next(trio for trio, elem in triad_groups if female_zodiac in trio)
            male_opt = [x for x in male_trio if x != male_zodiac][0]
            female_opt = [x for x in female_trio if x != female_zodiac][0]
            wedding_text = f"可考虑在{male_opt}年或{female_opt}年结婚，这些年份与双方生肖构成三合，助旺婚姻运势。婚期以春秋两季为宜。"
            recommended.extend([male_opt, female_opt])
        else:
            avoid_text = ""
            if (male_zodiac, female_zodiac) in all_liuchong or (male_zodiac, female_zodiac) in all_liuhai:
                avoid_text = f"避免选择{male_zodiac}年或{female_zodiac}年结婚，以免不利因素。"
            # 男女各自六合年份
            male_opt = next((b for a, b in liuhe_pairs if a == male_zodiac), None) or next((a for a, b in liuhe_pairs if b == male_zodiac), None)
            female_opt = next((b for a, b in liuhe_pairs if a == female_zodiac), None) or next((a for a, b in liuhe_pairs if b == female_zodiac), None)
            rec_years = set()
            if male_opt:
                rec_years.add(male_opt)
            if female_opt:
                rec_years.add(female_opt)
            if rec_years:
                years_str = "、".join(rec_years)
                wedding_text = f"宜择{years_str}等与双方属相相合的年份完婚。{avoid_text}婚礼季节可优先选在春秋两季。"
            else:
                wedding_text = avoid_text or "婚期选择无特别禁忌，一般可选在春季或秋季举办婚礼，更为吉利。"
            recommended.extend(list(rec_years))
    # 子嗣预测
    child_ancient = ""
    child_modern = ""
    if any(x in verse_text for x in ["五男", "儿女", "子女", "贵子", "儿孙", "无依靠"]):
        if "五男两女" in verse_text:
            child_ancient = "五男两女金满堂"
            child_modern = "子女众多，家业满堂。"
        elif "儿女双全" in verse_text:
            child_ancient = "儿女双全好风光"
            child_modern = "子女双全，福气满满。"
        elif "子女稀少" in verse_text or "儿女少" in verse_text:
            child_ancient = "子女稀少不相当"
            child_modern = "子嗣可能较少，需多努力。"
        elif "无依靠" in verse_text:
            child_ancient = "男女到老无依靠"
            child_modern = "暗示晚年子女缘薄，须及早规划。"
        elif "贵子贵孙旺" in verse_text or "贵子贤孙旺" in verse_text:
            child_ancient = "贵子贤孙旺"
            child_modern = "将来子孙贤贵兴旺。"
        elif "传儿孙" in verse_text:
            child_ancient = "福德传儿孙"
            child_modern = "儿孙承福，家族昌盛。"
        elif "生儿育女多辛苦" in verse_text:
            child_ancient = "生儿育女多辛苦"
            child_modern = "养育子女过程较为艰辛。"
        elif "儿女郎" in verse_text:
            child_ancient = "影响家中儿女郎"
            child_modern = "恐对子女运势产生不利影响。"
    else:
        if is_positive:
            child_modern = "子女运颇佳，儿女皆可期。"
        elif is_negative:
            child_modern = "子女运平平，需要双方共同努力营造良好家风。"
        else:
            child_modern = "子女运中等，平平稳稳。"
    # 输出结果
    st.header("配对分析结果")
    st.subheader("生辰八字")
    st.markdown(f"**男方八字：**{male_bazi['year']}年　{male_bazi['month']}月　{male_bazi['day']}日　{male_bazi['hour']}时")
    st.markdown(f"**女方八字：**{female_bazi['year']}年　{female_bazi['month']}月　{female_bazi['day']}日　{female_bazi['hour']}时")
    st.subheader("生肖属相配对分析")
    st.write(relation_text)
    st.subheader("纳音五行匹配")
    st.markdown(f"**男方年命纳音：**{male_nayin_name}（五行属{male_nayin_elem}）")
    st.markdown(f"**女方年命纳音：**{female_nayin_name}（五行属{female_nayin_elem}）")
    if male_nayin_elem == female_nayin_elem:
        st.write("两人年命纳音同属一行，易产生共鸣，同气连枝。")
    else:
        if gen_map.get(male_nayin_elem) == female_nayin_elem:
            st.write(f"男命纳音{male_nayin_elem}生女命纳音{female_nayin_elem}，一方能够滋养另一方。")
        elif gen_map.get(female_nayin_elem) == male_nayin_elem:
            st.write(f"女命纳音{female_nayin_elem}生男命纳音{male_nayin_elem}，一方对另一方有所成就扶持。")
        elif ovr_map.get(male_nayin_elem) == female_nayin_elem:
            st.write(f"男命纳音{male_nayin_elem}克女命纳音{female_nayin_elem}，需要注意平衡双方关系。")
        elif ovr_map.get(female_nayin_elem) == male_nayin_elem:
            st.write(f"女命纳音{female_nayin_elem}克男命纳音{male_nayin_elem}，需要双方多加包容。")
    st.subheader("五行生克分析")
    st.markdown(f"**古法批语：**{verse_text}")
    st.markdown(f"**白话解读：**{expl}")
    st.subheader("婚配评分")
    st.write(f"婚配综合得分：**{score_text}**")
    st.subheader("推荐婚期")
    st.write(wedding_text)
    st.subheader("子嗣预测")
    if child_ancient:
        st.markdown(f"**古法预示：**{child_ancient}。")
    st.markdown(f"**现代解读：**{child_modern}")

