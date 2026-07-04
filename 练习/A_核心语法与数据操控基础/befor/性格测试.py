# 性格分析问卷（含年龄、性别+个性化人生建议版）- 交互式Python程序
def personality_questionnaire_with_advice():
    # ========== 新增：采集年龄和性别 ==========
    def collect_basic_info():
        """收集用户年龄和性别信息"""
        print("=" * 60)
        print("📋 基础信息采集")
        print("=" * 60)

        # 采集年龄（验证合理性）
        while True:
            age_input = input("请输入你的年龄（1-100）：").strip()
            if age_input.isdigit():
                age = int(age_input)
                if 1 <= age <= 100:
                    break
                else:
                    print("❌ 年龄需在1-100之间，请重新输入！")
            else:
                print("❌ 输入无效，请输入数字！")

        # 采集性别（提供选项，支持自定义）
        while True:
            gender = input("请输入你的性别（男/女/其他）：").strip()
            if gender in ["男", "女", "沃尔玛购物袋"]:
                break
            else:
                confirm = input(f"你输入的是「{gender}」，是否确认？（是/否）：").strip()
                if confirm == "是":
                    break
                else:
                    print("请重新输入（推荐选项：男/女/其他）")

        print("=" * 60 + "\n")
        return age, gender

    # ========== 问卷题目 ==========
    questions = [
        # 外向(E)/内向(I)
        "1. 与人交往时，我更享受和少数挚友深聊，而非在人群中应酬。",
        "2. 我享受成为焦点的感觉，比如在聚会中发言或表演节目。",
        "3. 我不介意独处，独处时反而能更好地整理思绪和充电。",
        "4. 遇到有趣的活动，我会主动邀请他人一起参与。",

        # 计划型(J)/灵活型(P)
        "5. 制定计划后，我会严格按计划执行，不喜欢临时变更。",
        "6. 我习惯把物品摆放得井井有条，杂乱的环境会让我心烦。",
        "7. 我更倾向于随机应变，而非提前制定详细计划。",
        "8. 面对突发状况，我能快速适应并调整行动方案。",

        # 理性(T)/感性(F)
        "9. 我做事更看重逻辑和事实，而非个人情感和主观感受。",
        "10. 我容易被他人的情绪感染，看到别人难过自己也会跟着低落。",
        "11. 做决定时，我更依赖直觉和内心感受，而非理性分析。",
        "12. 我会主动记住他人的喜好，在合适的时机给对方小惊喜。",

        # 探索型(N)/稳定型(S)
        "13. 我喜欢尝试新鲜事物，比如新的美食、旅行目的地或兴趣爱好。",
        "14. 我喜欢挑战有难度的任务，越有挑战性越能激发我的斗志。",
        "15. 我更偏好熟悉的环境和流程，避免不必要的风险。",
        "16. 我习惯从过往经验中总结规律，指导未来的行动。"
    ]

    # 计分规则
    score_direction = [
        -1, 1, -1, 1,  # 外向(E)维度
        1, 1, -1, -1,  # 计划型(J)维度
        1, -1, -1, -1,  # 理性(T)维度
        1, 1, -1, -1  # 探索型(N)维度
    ]

    # ========== 个性化人生建议配置 ==========
    def get_personal_advice(age, gender, extrovert_trait, plan_trait, rational_trait, explore_trait):
        """结合年龄、性别、性格特质生成建议"""
        # 按年龄分段定义核心发展重点
        age_stage = ""
        age_focus = ""
        if age <= 20:  # 青少年期
            age_stage = "小屁孩，啥啥干不好，活着干啥。"
            age_focus = "毛都没长齐就敢当自己是个人物？去死吧乐子"
        elif 21 <= age <= 35:  # 青年期
            age_stage = "青年期"
            age_focus = "职业发展、独立能力、人际关系构建"
        elif 36 <= age <= 50:  # 中年期
            age_stage = "中年期"
            age_focus = "责任担当、事业深耕、家庭平衡"
        else:  # 中老年期
            age_stage = "中老年期"
            age_focus = "老不死活着干啥，赶快去死"

        # 结合性格+年龄的建议
        advice_list = []

        # 1. 社交模式建议
        if extrovert_trait == "外向开朗":
            if age <= 35:
                advice_list.append(
                    "你的社交优势突出，可多参与行业交流、社团活动，拓展人脉的同时注意筛选优质圈子，避免过度社交消耗精力。")
            else:
                advice_list.append(
                    "善用你的社交能力维系亲友关系，但不必勉强自己参与不必要的应酬，把时间留给真正重要的人。")
        else:  # 内向沉稳
            if age <= 35:
                advice_list.append(
                    "你的专注和思考力是优势，可通过专业领域深耕建立个人品牌，同时尝试主动拓展1-2个核心社交圈，避免错过机会。")
            else:
                advice_list.append(
                    "享受独处的同时，记得多与家人朋友沟通近况，不必追求社交数量，高质量的深度连接更能滋养心灵。")

        # 2. 做事风格建议
        if plan_trait == "计划有序":
            if age <= 35:
                advice_list.append(
                    "你的规划能力能帮你稳步成长，但偶尔可尝试打破计划，接受适度的不确定性，培养灵活应变的能力。")
            else:
                advice_list.append("保持规划习惯的同时，可适当放权给他人，不必事事亲力亲为，给自己留更多弹性空间享受生活。")
        else:  # 灵活随性
            if age <= 35:
                advice_list.append("你的适应力很强，但重要目标（如职业晋升、考证）需制定基础计划，避免因拖延错过关键节点。")
            else:
                advice_list.append("享受随性生活的同时，可给健康管理、家庭陪伴等核心事项设定简单规则，平衡自由与责任。")

        # 3. 决策方式建议
        if rational_trait == "理性客观":
            advice_list.append(
                "你的逻辑判断能力突出，做重要决策时可多倾听他人的情感诉求（尤其是家人关系中），让结果更周全。")
        else:  # 感性共情
            advice_list.append(
                "你善于理解他人，但做关键选择（如职业变动、财务决策）时，可尝试用理性分析辅助判断，避免被情绪左右。")

        # 4. 生活态度建议
        if explore_trait == "探索创新":
            if age <= 50:
                advice_list.append("保持好奇心和创造力，可将兴趣转化为副业或技能优势，但注意聚焦核心方向，避免精力分散。")
            else:
                advice_list.append("探索新事物（如智能设备、兴趣爱好）能丰富晚年生活，但注意选择低风险、适合身体状况的方式。")
        else:  # 稳定务实
            if age <= 50:
                advice_list.append("你的踏实可靠让人放心，可偶尔尝试小范围突破（如学习新技能、短途旅行），为生活增添新鲜感。")
            else:
                advice_list.append("享受稳定生活的同时，可分享过往经验给晚辈，在传承中获得新的价值感。")

        # 5. 结合性别的补充建议（中性客观，不刻板）
        gender_advice = {
            "男": "建议多关注情绪表达，不必过度追求'坚强'，适当示弱和倾诉也是一种智慧。",
            "女": "建议多重视自我需求，不必过度在意他人评价，学会优先照顾自己的感受和成长。",
            "其他": "建议保持自我认同，在兼顾他人感受的同时，勇敢追求自己想要的生活状态。"
        }
        advice_list.append(gender_advice.get(gender, "建议保持真实的自己，在生活中找到适合自己的节奏和平衡。"))

        return age_stage, age_focus, advice_list

    # ========== 核心答题逻辑 ==========
    scores = []
    option_scores = {"A": 1, "B": 2, "C": 3, "D": 4}

    # 采集基础信息
    age, gender = collect_basic_info()

    # 显示问卷说明
    print("📝 性格分析问卷")
    print("答题说明：请根据实际情况选择最符合你的选项")
    print("选项：A.非常符合  B.比较符合  C.不太符合  D.完全不符合")
    print("=" * 60 + "\n")

    # 逐题答题
    for i, question in enumerate(questions):
        while True:
            print(question)
            answer = input("请选择（A/B/C/D）：").strip().upper()
            if answer in ["A", "B", "C", "D"]:
                if score_direction[i] == -1:
                    scores.append(5 - option_scores[answer])
                else:
                    scores.append(option_scores[answer])
                print()
                break
            else:
                print("❌ 输入错误！请重新选择A/B/C/D\n")

    # 计算维度得分
    e_score = sum(scores[0:4])  # 外向(E)维度
    j_score = sum(scores[4:8])  # 计划型(J)维度
    t_score = sum(scores[8:12])  # 理性(T)维度
    n_score = sum(scores[12:16])  # 探索型(N)维度

    # 获取性格特质（含优缺点）
    def get_personality_detail(score, dimension_type):
        if dimension_type == "extrovert":
            if score >= 10:
                return {"trait": "外向开朗", "strength": "擅长社交、乐于分享，容易快速融入集体，人脉资源丰富",
                        "weakness": "可能过度依赖他人陪伴，独处时容易感到无聊，有时会因冲动发言"}
            else:
                return {"trait": "内向沉稳", "strength": "专注深入、善于思考，能独立完成复杂任务，情感更细腻",
                        "weakness": "社交主动性不足，容易给人距离感，遇到问题可能不愿主动求助"}
        elif dimension_type == "plan":
            if score >= 10:
                return {"trait": "计划有序", "strength": "目标明确、执行力强，做事有条理，不易出错",
                        "weakness": "过于刻板，难以适应突发变化，对不确定性的容忍度低"}
            else:
                return {"trait": "灵活随性", "strength": "随机应变能力强，心态放松，能快速适应新环境",
                        "weakness": "缺乏规划性，容易拖延，重要事情可能因临时变动出错"}
        elif dimension_type == "rational":
            if score >= 10:
                return {"trait": "理性客观", "strength": "逻辑清晰、决策果断，能基于事实判断，不易被情绪影响",
                        "weakness": "共情能力较弱，容易忽略他人感受，显得有些冷漠"}
            else:
                return {"trait": "感性共情", "strength": "善于理解他人、懂得照顾情绪，人际关系更融洽",
                        "weakness": "做决定时容易被情绪左右，不够果断，可能因心软妥协"}
        elif dimension_type == "explore":
            if score >= 10:
                return {"trait": "探索创新", "strength": "好奇心强、敢于尝试，容易发现新机会，创造力突出",
                        "weakness": "缺乏耐心，容易半途而废，对重复的日常事务感到枯燥"}
            else:
                return {"trait": "稳定务实", "strength": "踏实可靠、耐心细致，擅长深耕细作，做事让人放心",
                        "weakness": "不愿突破舒适区，接受新事物较慢，可能错过潜在机会"}

    # 获取各维度详情
    extrovert_detail = get_personality_detail(e_score, "extrovert")
    plan_detail = get_personality_detail(j_score, "plan")
    rational_detail = get_personality_detail(t_score, "rational")
    explore_detail = get_personality_detail(n_score, "explore")

    # 生成个性化建议
    age_stage, age_focus, personal_advice = get_personal_advice(
        age, gender,
        extrovert_detail["trait"],
        plan_detail["trait"],
        rational_detail["trait"],
        explore_detail["trait"]
    )

    # ========== 输出最终报告 ==========
    print("=" * 60)
    print("🎯 个性化性格分析+人生建议报告")
    print("=" * 60)
    print(f"📌 基础信息：年龄 {age} 岁 | 性别 {gender}")
    print(f"📌 人生阶段：{age_stage}（核心发展重点：{age_focus}）")
    print(f"\n🏷️  核心性格标签：{extrovert_detail['trait']}、{plan_detail['trait']}、"
          f"{rational_detail['trait']}、{explore_detail['trait']}")

    print("\n📊 性格优缺点解析：")
    print(f"1. 社交模式 - {extrovert_detail['trait']}")
    print(f"   ✅ 优点：{extrovert_detail['strength']}")
    print(f"   ❌ 待改进：{extrovert_detail['weakness']}")
    print(f"2. 做事风格 - {plan_detail['trait']}")
    print(f"   ✅ 优点：{plan_detail['strength']}")
    print(f"   ❌ 待改进：{plan_detail['weakness']}")
    print(f"3. 决策方式 - {rational_detail['trait']}")
    print(f"   ✅ 优点：{rational_detail['strength']}")
    print(f"   ❌ 待改进：{rational_detail['weakness']}")
    print(f"4. 生活态度 - {explore_detail['trait']}")
    print(f"   ✅ 优点：{explore_detail['strength']}")
    print(f"   ❌ 待改进：{explore_detail['weakness']}")

    print("\n💡 专属人生建议（结合年龄、性别、性格）：")
    for i, advice in enumerate(personal_advice, 1):
        print(f"{i}. {advice}")

    print("\n✨ 总结：什么鬼性格，没见过这么暴躁的，跟大猩猩有什么区别。重开吧，乐子")
    print("=" * 60)


# 运行问卷
if __name__ == "__main__":
    personality_questionnaire_with_advice()