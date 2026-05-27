"""
生成压力测试版 + 周月报模板 Excel
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
NORMAL_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="center")
PARAM_FILL = PatternFill("solid", fgColor="FFF2CC")
DANGER_FILL = PatternFill("solid", fgColor="FEE2E2")
WARNING_FILL = PatternFill("solid", fgColor="FED7AA")
SUCCESS_FILL = PatternFill("solid", fgColor="D1FAE5")


def style_header(ws, row, n_cols):
    for col in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP
        cell.border = BORDER


def style_data(ws, start_row, end_row, n_cols):
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, min_col=1, max_col=n_cols):
        for cell in row:
            if not cell.font.bold:
                cell.font = NORMAL_FONT
            cell.alignment = WRAP
            cell.border = BORDER


def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ================ 压力测试 Excel ================
def create_stress_test_excel():
    wb = Workbook()

    # Sheet 0: 三版本对比
    ws = wb.active
    ws.title = "0-三版本对比"
    ws["A1"] = "压力测试版 vs 精细务实版 vs 旧版"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["维度", "旧版(乐观)", "精细务实版", "压力测试版", "压力 vs 精细"])
    style_header(ws, 3, 5)

    data = [
        ["Y1 营收", "¥1340 万", "¥333 万", "¥202 万", "-39%"],
        ["Y1 净亏", "-¥698 万", "-¥357 万", "-¥425 万", "净亏增大 19%"],
        ["M12 月营收", "¥270 万", "¥67.7 万", "¥37 万", "-45%"],
        ["M12 累计卖家", "5000", "854", "558", "-35%"],
        ["盈亏平衡", "M12", "M15-16", "M20+", "推迟 5 个月"],
        ["3 年累计", "¥3.98 亿", "¥0.84 亿", "¥0.45 亿", "-46%"],
        ["必要 Pre-A", "¥1000 万 @M5", "¥500-800 万 @M7-8", "¥1000-1500 万 @M6", "提前+加大"],
        ["", "", "", "", ""],
        ["压力测试关键调整", "", "", "", ""],
        ["流失率（前6月）", "1%", "1%", "2%", "翻倍"],
        ["月新增（M6）", "40", "40", "25", "-38%"],
        ["流量费付费率(M12)", "60%", "50%", "30%", "-40%"],
        ["流量费均价", "¥800+", "¥540", "¥380", "-30%"],
    ]
    for r in data:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)
    set_widths(ws, [22, 18, 18, 18, 18])

    # Sheet 1: 压力测试月营收
    ws2 = wb.create_sheet("1-Y1月营收")
    ws2["A1"] = "Y1 月营收（压力测试版）"
    ws2["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="C53030")
    ws2.merge_cells("A1:H1")
    ws2.append([])

    ws2.append(["月份", "活跃", "会员费", "流量费", "订阅", "增值", "SaaS", "月营收(万元)"])
    style_header(ws2, 3, 8)

    monthly = [
        ["M1", 201, 7.54, 0, 0, 0, 0, 7.54],
        ["M2", 203, 7.61, 0, 0, 0, 0, 7.61],
        ["M3", 211, 7.91, 0.40, 0, 0, 0, 8.31],
        ["M4", 227, 8.51, 0.80, 0, 0.04, 0, 9.35],
        ["M5", 242, 9.08, 1.30, 0, 0.07, 0, 10.45],
        ["M6", 262, 9.83, 2.10, 0.15, 0.13, 0, 12.21],
        ["M7", 292, 10.95, 3.10, 0.26, 0.22, 0, 14.53],
        ["M8", 331, 12.41, 4.40, 0.40, 0.34, 0, 17.55],
        ["M9", 374, 14.03, 5.90, 0.57, 0.51, 0.08, 21.09],
        ["M10", 427, 16.01, 7.70, 0.79, 0.71, 0.18, 25.39],
        ["M11", 488, 18.30, 9.90, 1.12, 1.01, 0.30, 30.63],
        ["M12", 558, 20.93, 12.70, 1.51, 1.34, 0.50, 36.98],
    ]
    for r in monthly:
        ws2.append(r)

    ws2.append(["Y1 累计", "-", 143.1, 48.3, 4.8, 4.4, 1.1, 201.7])
    style_data(ws2, 4, ws2.max_row, 8)

    for cell in ws2[ws2.max_row]:
        cell.font = BOLD_FONT
        cell.fill = DANGER_FILL

    set_widths(ws2, [10, 10, 12, 12, 10, 10, 10, 14])

    # Sheet 2: 现金流
    ws3 = wb.create_sheet("2-现金流(危险)")
    ws3["A1"] = "Y1 现金流（极度紧张）"
    ws3["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="C53030")
    ws3.merge_cells("A1:F1")
    ws3.append([])

    ws3.append(["月份", "月营收(万)", "月成本(万,-15%)", "月净亏(万)", "累计净亏(万)", "现金余额(万)"])
    style_header(ws3, 3, 6)

    cash = 300
    cumulative = 0
    data = [
        ["M1", 7.54, 26, -18.46],
        ["M2", 7.61, 27, -19.39],
        ["M3", 8.31, 32, -23.69],
        ["M4", 9.35, 36, -26.65],
        ["M5", 10.45, 41, -30.55],
        ["M6", 12.21, 47, -34.79],
        ["M7", 14.53, 55, -40.47],
        ["M8", 17.55, 62, -44.45],
        ["M9", 21.09, 70, -48.91],
        ["M10", 25.39, 77, -51.61],
        ["M11", 30.63, 77, -46.37],
        ["M12", 36.98, 77, -40.02],
    ]

    for r in data:
        cumulative += r[3]
        balance = cash + cumulative
        ws3.append(r + [round(cumulative, 1), round(balance, 1)])
        # 余额 < 50 万红色
        if balance < 50:
            for col in range(1, 7):
                ws3.cell(row=ws3.max_row, column=col).fill = DANGER_FILL

    style_data(ws3, 4, ws3.max_row, 6)

    ws3.append([])
    ws3.append(["关键警示"])
    ws3.cell(row=ws3.max_row, column=1).font = BOLD_FONT
    ws3.append(["M9 现金即将枯竭", "必须 M6-M7 完成 Pre-A"])
    ws3.append(["Pre-A 募集额", "¥1000-1500 万（含安全垫）"])
    ws3.append(["盈亏平衡", "M20+"])

    set_widths(ws3, [10, 14, 16, 14, 14, 14])

    # Sheet 3: 应对预案
    ws4 = wb.create_sheet("3-应对预案")
    ws4["A1"] = "压力测试应对预案"
    ws4["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws4.merge_cells("A1:D1")
    ws4.append([])

    ws4.append(["阶段", "触发条件", "立即动作", "Owner"])
    style_header(ws4, 3, 4)

    plans = [
        ["M3 末警示", "月营收 < ¥10 万", "复盘+客户成功加码", "COO"],
        ["M4 末警告", "月营收 < ¥9 万", "拉群+成本压缩", "CEO"],
        ["M5 末紧急", "月营收 < ¥10 万", "启动 B 计划", "CEO"],
        ["", "", "", ""],
        ["B 计划：成本压缩", "", "", ""],
        ["人员", "团队冻结到 M8", "停止扩招", "HR"],
        ["服务器", "升级延迟", "节省 ¥5,000/月", "CTO"],
        ["数据采购", "改用免费", "节省 ¥8,000/月", "运营"],
        ["市场地推", "砍 50%", "节省 ¥15,000/月", "CMO"],
        ["行政", "缩小办公", "节省 ¥10,000/月", "HR"],
        ["", "", "", ""],
        ["B 计划：加速融资", "", "", ""],
        ["Pre-A 提前", "M6（不是 M8）", "接受较低估值", "CEO"],
        ["Pre-A 金额", "¥1000-1500 万", "含安全垫", "CFO"],
        ["可转债", "如 Pre-A 不顺", "桥贷支撑 6 个月", "CFO"],
        ["", "", "", ""],
        ["C 计划：战略转向（极端）", "", "", ""],
        ["业务方向", "纯数据 + 工具", "降低 GMV 焦虑", "CEO"],
        ["规模收缩", "聚焦唐山+热轧", "区域内 80% 渗透", "COO"],
        ["被战略投资", "宝武/沙钢/南钢", "保留运营权", "CEO"],
    ]

    for r in plans:
        ws4.append(r)

    style_data(ws4, 4, ws4.max_row, 4)
    set_widths(ws4, [22, 22, 26, 12])

    output = "docs/11-务实版财务测算/营收压力测试版.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")


# ================ 周月报模板 Excel ================
def create_report_templates_excel():
    wb = Workbook()

    # Sheet 0: 使用说明
    ws = wb.active
    ws.title = "0-使用说明"
    ws["A1"] = "货袋子周报/月报对账模板"
    ws["A1"].font = Font(name="微软雅黑", size=18, bold=True, color="1F4E78")
    ws.merge_cells("A1:D1")

    rows = [
        [""],
        ["报告类型", "频率", "受众", "Owner"],
        ["日报", "每日", "运营", "运营负责人"],
        ["周报", "每周一 9:00", "全员", "运营负责人"],
        ["月报", "月初 5 个工作日", "CEO+VP+投资人", "CFO"],
        ["季度报", "季末 7 个工作日", "董事会", "CEO"],
        ["半年报", "半年末", "投资人", "CEO"],
        ["年度报", "年末", "全员+投资人", "CEO+CFO"],
        [""],
        ["📋 红绿灯标准", "", "", ""],
        ["🟢 绿色", "±10%", "正常", "-"],
        ["🟡 黄色", "10-20%", "关注+月底复盘", "-"],
        ["🟠 橙色", "20-50%", "周复盘+调整", "-"],
        ["🔴 红色", ">50%", "立即拉群+紧急复盘", "-"],
        ["🟣 紫色", "持续 3 月红色", "战略级调整/触发压力测试预案", "-"],
        [""],
        ["📋 报表对应", "", "", ""],
        ["Sheet 1", "周报模板", "每周复制使用", ""],
        ["Sheet 2", "月报模板", "每月复制使用", ""],
        ["Sheet 3", "偏差归因模板", "发现偏差填写", ""],
    ]

    for r in rows:
        ws.append(r)

    for row_idx in [3, 11, 18]:
        for col in range(1, 5):
            ws.cell(row=row_idx, column=col).font = Font(name="微软雅黑", size=12, bold=True, color="1F4E78")

    set_widths(ws, [18, 20, 28, 14])

    # Sheet 1: 周报模板
    ws1 = wb.create_sheet("1-周报模板")
    ws1["A1"] = "《货袋子周报 - W## 2026》"
    ws1["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws1.merge_cells("A1:G1")
    ws1.append([])

    # 核心 KPI
    ws1.append(["A. 核心 KPI"])
    ws1.cell(row=ws1.max_row, column=1).font = BOLD_FONT
    ws1.append(["指标", "本周", "上周", "周环比", "计划", "偏差", "颜色"])
    style_header(ws1, ws1.max_row, 7)

    kpis = [
        ["新增卖家数", "", "", "", "", "", ""],
        ["流失卖家数", "", "", "", "", "", ""],
        ["周末活跃付费", "", "", "", "", "", ""],
        ["周营收(万)", "", "", "", "", "", ""],
        ["现金余额(万)", "", "", "", "", "", ""],
    ]
    for r in kpis:
        ws1.append(r)

    # 业务漏斗
    ws1.append([])
    ws1.append(["B. 业务漏斗（卖家端）"])
    ws1.cell(row=ws1.max_row, column=1).font = BOLD_FONT
    ws1.append(["指标", "本周", "上周", "转化率", "", "", ""])
    style_header(ws1, ws1.max_row, 4)

    funnels = [
        ["新增报价数", "", "", ""],
        ["询价→报价", "", "", ""],
        ["报价→联系", "", "", ""],
        ["联系→成交", "", "", ""],
    ]
    for r in funnels:
        ws1.append(r + ["", "", ""])

    # 100 家健康度
    ws1.append([])
    ws1.append(["C. 100 家健康度"])
    ws1.cell(row=ws1.max_row, column=1).font = BOLD_FONT
    ws1.append(["分层", "活跃", "高潜", "危险", "流失", "回流", ""])
    style_header(ws1, ws1.max_row, 6)
    ws1.append(["A (20)", "", "", "", "", "", ""])
    ws1.append(["B (30)", "", "", "", "", "", ""])
    ws1.append(["C (30)", "", "", "", "", "", ""])
    ws1.append(["D (20)", "", "", "", "", "", ""])

    # 红色预警
    ws1.append([])
    ws1.append(["D. 红色/黄色预警"])
    ws1.cell(row=ws1.max_row, column=1).font = BOLD_FONT
    ws1.append(["颜色", "描述", "Owner", "处置", "截止", "", ""])
    style_header(ws1, ws1.max_row, 5)
    for i in range(3):
        ws1.append(["", "", "", "", "", "", ""])

    # 下周计划
    ws1.append([])
    ws1.append(["E. 下周计划"])
    ws1.cell(row=ws1.max_row, column=1).font = BOLD_FONT
    ws1.append(["#", "计划", "Owner", "完成标准", "优先级", "", ""])
    style_header(ws1, ws1.max_row, 5)
    for i in range(5):
        ws1.append([i+1, "", "", "", "", "", ""])

    style_data(ws1, 3, ws1.max_row, 7)
    set_widths(ws1, [16, 14, 14, 14, 14, 14, 12])

    # Sheet 2: 月报模板
    ws2 = wb.create_sheet("2-月报模板")
    ws2["A1"] = "《货袋子月报 - YYYY-MM》"
    ws2["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws2.merge_cells("A1:F1")
    ws2.append([])

    # Page 1: 执行摘要
    ws2.append(["Page 1: 执行摘要"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT
    ws2.append(["项", "内容", "", "", "", ""])
    style_header(ws2, ws2.max_row, 2)
    ws2.append(["本月一句话", ""])
    ws2.append(["3 个关键数字", "月营收 ¥XX 万 / 月活 XXX / 现金 ¥XX 万"])
    ws2.append(["3 个关键事件", "1)... 2)... 3)..."])
    ws2.append(["3 个关键决策", "1)... 2)... 3)..."])

    # Page 2: 财务详情
    ws2.append([])
    ws2.append(["Page 2: 财务详情（营收）"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT
    ws2.append(["收入项", "本月实际", "本月计划", "达成率", "上月", "环比"])
    style_header(ws2, ws2.max_row, 6)
    for item in ["会员费", "流量费", "订阅", "增值服务", "买家 SaaS", "总计"]:
        ws2.append([item, "", "", "", "", ""])

    # Page 2: 成本
    ws2.append([])
    ws2.append(["Page 2: 财务详情（成本）"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT
    ws2.append(["成本项", "本月实际", "本月预算", "达成率", "上月", "环比"])
    style_header(ws2, ws2.max_row, 6)
    for item in ["人员", "服务器", "数据", "邀请激励", "市场地推", "行政", "总计"]:
        ws2.append([item, "", "", "", "", ""])

    # 损益
    ws2.append([])
    ws2.append(["Page 2: 损益与现金"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT
    for item in ["净亏", "累计净亏", "现金余额", "剩余跑道（月）"]:
        ws2.append([item, "", "", "", "", ""])

    # 财务红线
    ws2.append([])
    ws2.append(["Page 2: 财务红线检查"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT
    ws2.append(["红线", "标准", "实际", "✅/❌"])
    style_header(ws2, ws2.max_row, 4)
    redlines = [
        ["现金跑道", "> 4 个月"],
        ["流量费付费率", "> 30%"],
        ["卖家月续费率", "> 70%"],
        ["月成本未超预算", "≤ 120%"],
        ["应收账款", "< 30 天"],
    ]
    for r in redlines:
        ws2.append(r + ["", ""])

    style_data(ws2, 3, ws2.max_row, 6)
    set_widths(ws2, [22, 16, 16, 14, 14, 14])

    # Sheet 3: 偏差归因模板
    ws3 = wb.create_sheet("3-偏差归因模板")
    ws3["A1"] = "偏差归因分析模板"
    ws3["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws3.merge_cells("A1:D1")
    ws3.append([])

    rows = [
        ["基本信息"],
        ["指标", ""],
        ["计划值", ""],
        ["实际值", ""],
        ["偏差", ""],
        ["颜色", "🔴/🟠/🟡"],
        ["报告日期", ""],
        [""],
        ["原因分析（按概率排序）"],
        ["原因 #", "描述", "概率%", "证据"],
        [1, "", "", ""],
        [2, "", "", ""],
        [3, "", "", ""],
        [""],
        ["最可能原因", ""],
        ["详细依据", ""],
        [""],
        ["应对动作"],
        ["时间窗", "动作", "Owner", "截止"],
        ["立即（24h内）", "", "", ""],
        ["短期（本周）", "", "", ""],
        ["中期（本月）", "", "", ""],
        ["长期（本季度）", "", "", ""],
        [""],
        ["跟进"],
        ["跟进时点", ""],
        ["跟进人", ""],
        ["结案条件", ""],
    ]
    for r in rows:
        ws3.append(r)

    for row_idx in [3, 11, 21, 27]:
        for col in range(1, 5):
            ws3.cell(row=row_idx, column=col).font = Font(name="微软雅黑", size=12, bold=True, color="1F4E78")

    set_widths(ws3, [18, 26, 16, 24])

    # Sheet 4: 红绿灯参考
    ws4 = wb.create_sheet("4-红绿灯参考")
    ws4["A1"] = "对账红绿灯标准"
    ws4["A1"].font = Font(name="微软雅黑", size=16, bold=True)
    ws4.merge_cells("A1:D1")
    ws4.append([])

    ws4.append(["颜色", "偏差范围", "处置", "示例"])
    style_header(ws4, 3, 4)

    colors = [
        ["🟢 绿色", "±10%", "正常运营", "月营收偏差 5%"],
        ["🟡 黄色", "±10-20%", "关注 + 月底复盘", "月新增偏差 15%"],
        ["🟠 橙色", "±20-50%", "周复盘 + 调整", "月营收偏差 30%"],
        ["🔴 红色", ">50%", "24h 内紧急复盘", "月营收偏差 60%"],
        ["🟣 紫色", "持续 3 月红色", "战略级调整/触发压力测试预案", "连续 3 月营收 < 50% 计划"],
    ]
    for r in colors:
        ws4.append(r)

    # 染色对应行
    fills = [SUCCESS_FILL, WARNING_FILL, WARNING_FILL, DANGER_FILL, DANGER_FILL]
    for i, fill in enumerate(fills, start=4):
        for col in range(1, 5):
            ws4.cell(row=i, column=col).fill = fill

    style_data(ws4, 4, ws4.max_row, 4)
    set_widths(ws4, [12, 18, 30, 32])

    output = "docs/11-务实版财务测算/周月报对账模板.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")


def main():
    create_stress_test_excel()
    create_report_templates_excel()
    print("✓ 2 个 Excel 文件已生成")


if __name__ == "__main__":
    main()
