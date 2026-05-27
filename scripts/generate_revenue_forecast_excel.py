"""
生成「3 年营收测算」Excel 工作版（保守/常规/乐观三档）。

输出：docs/06-财务预测/3年营收测算-三档情景.xlsx
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
SUBHEADER_FILL = PatternFill("solid", fgColor="D9E1F2")
TOTAL_FILL = PatternFill("solid", fgColor="FFF2CC")
NORMAL_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="center")
LEFT = Alignment(wrap_text=True, vertical="center", horizontal="left")


def style_header(ws, row):
    for cell in ws[row]:
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP
        cell.border = BORDER


def style_data(ws, start_row, end_row, end_col, align=WRAP):
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, min_col=1, max_col=end_col):
        for cell in row:
            if cell.font.bold:
                continue
            cell.font = NORMAL_FONT
            cell.alignment = align
            cell.border = BORDER


# ============== Y1 月度营收（万元） ==============
# 12 个月 × 5 个收入项 × 3 档
Y1_DATA = {
    "保守": {
        "会员费": [17, 18, 20, 22, 25, 28, 32, 38, 45, 55, 65, 75],
        "流量费": [0, 0, 1, 3, 4, 6, 9, 14, 20, 28, 38, 50],
        "订阅": [0, 0, 0, 0, 1, 2, 2, 3, 5, 7, 9, 12],
        "增值服务": [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 5, 8],
        "买家 SaaS": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    },
    "常规": {
        "会员费": [17.5, 20, 22.5, 25, 30, 37.5, 45, 55, 70, 85, 100, 120],
        "流量费": [0, 1, 3, 6, 10, 16, 25, 38, 55, 75, 90, 105],
        "订阅": [0, 0, 1, 2, 4, 6, 8, 12, 16, 20, 25, 30],
        "增值服务": [0, 0, 0.5, 1, 1.5, 2.5, 4, 5, 8, 10, 12, 15],
        "买家 SaaS": [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 10],
    },
    "乐观": {
        "会员费": [18, 22, 26, 32, 40, 50, 65, 80, 100, 125, 150, 170],
        "流量费": [0, 2, 5, 10, 17, 25, 40, 60, 90, 125, 155, 180],
        "订阅": [0, 0, 1, 3, 6, 10, 15, 20, 26, 35, 42, 50],
        "增值服务": [0, 0, 1, 2, 3, 5, 8, 11, 15, 20, 24, 28],
        "买家 SaaS": [0, 0, 0, 0, 0, 0, 0, 1, 3, 8, 15, 25],
    },
}

Y1_COST = {
    "保守": [70, 72, 75, 80, 85, 90, 100, 110, 130, 150, 170, 200],
    "常规": [72, 76, 82, 90, 100, 110, 125, 145, 170, 195, 220, 263],
    "乐观": [78, 85, 95, 105, 120, 140, 160, 180, 205, 240, 280, 330],
}


# ============== Y2-Y3 半年汇总（万元/月，季度抽样） ==============
Y23_SAMPLE = {
    "保守": {
        "M13": {"会员费": 80, "流量费": 55, "订阅": 14, "增值服务": 9, "买家 SaaS": 3, "数据/金融": 0},
        "M18": {"会员费": 105, "流量费": 100, "订阅": 28, "增值服务": 20, "买家 SaaS": 12, "数据/金融": 5},
        "M24": {"会员费": 160, "流量费": 180, "订阅": 55, "增值服务": 45, "买家 SaaS": 50, "数据/金融": 25},
        "M30": {"会员费": 240, "流量费": 320, "订阅": 90, "增值服务": 90, "买家 SaaS": 120, "数据/金融": 70},
        "M36": {"会员费": 360, "流量费": 540, "订阅": 150, "增值服务": 175, "买家 SaaS": 245, "数据/金融": 175},
    },
    "常规": {
        "M13": {"会员费": 130, "流量费": 115, "订阅": 33, "增值服务": 17, "买家 SaaS": 15, "数据/金融": 0},
        "M18": {"会员费": 170, "流量费": 200, "订阅": 65, "增值服务": 45, "买家 SaaS": 55, "数据/金融": 25},
        "M24": {"会员费": 260, "流量费": 380, "订阅": 130, "增值服务": 120, "买家 SaaS": 180, "数据/金融": 120},
        "M30": {"会员费": 400, "流量费": 680, "订阅": 220, "增值服务": 240, "买家 SaaS": 380, "数据/金融": 280},
        "M36": {"会员费": 600, "流量费": 1200, "订阅": 380, "增值服务": 480, "买家 SaaS": 800, "数据/金融": 620},
    },
    "乐观": {
        "M13": {"会员费": 185, "流量费": 200, "订阅": 56, "增值服务": 32, "买家 SaaS": 35, "数据/金融": 5},
        "M18": {"会员费": 250, "流量费": 380, "订阅": 120, "增值服务": 95, "买家 SaaS": 130, "数据/金融": 60},
        "M24": {"会员费": 400, "流量费": 720, "订阅": 250, "增值服务": 250, "买家 SaaS": 400, "数据/金融": 280},
        "M30": {"会员费": 660, "流量费": 1380, "订阅": 460, "增值服务": 510, "买家 SaaS": 880, "数据/金融": 660},
        "M36": {"会员费": 1050, "流量费": 2650, "订阅": 820, "增值服务": 1080, "买家 SaaS": 1850, "数据/金融": 1500},
    },
}

# 年度汇总（手算）
YEARLY_SUMMARY = {
    "保守": {"Y1 营收": 702, "Y1 成本": 1830, "Y1 净利": -1128,
            "Y2 营收": 3642, "Y2 成本": 3900, "Y2 净利": -258,
            "Y3 营收": 12960, "Y3 成本": 8500, "Y3 净利": 4460},
    "常规": {"Y1 营收": 1340, "Y1 成本": 2038, "Y1 净利": -698,
            "Y2 营收": 7600, "Y2 成本": 5400, "Y2 净利": 2200,
            "Y3 营收": 30860, "Y3 成本": 15000, "Y3 净利": 15860},
    "乐观": {"Y1 营收": 1930, "Y1 成本": 2300, "Y1 净利": -370,
            "Y2 营收": 14170, "Y2 成本": 8000, "Y2 净利": 6170,
            "Y3 营收": 64720, "Y3 成本": 28000, "Y3 净利": 36720},
}


def create_summary_sheet(wb):
    ws = wb.active
    ws.title = "三档总览"

    ws["A1"] = "货袋子 3 年营收测算 - 三档情景对比"
    ws["A1"].font = Font(name="微软雅黑", size=18, bold=True, color="1F4E78")
    ws.merge_cells("A1:E1")

    ws.append([])
    ws.append(["指标", "保守", "常规", "乐观", "差异说明"])
    style_header(ws, 3)

    rows = [
        ["3 年累计营收（万元）", 17310, 39800, 80800, "乐观 = 保守 × 4.7x"],
        ["3 年累计净利（万元）", 3074, 17362, 42520, "Y3 净利率 34% / 51% / 57%"],
        ["M12 月营收（万元）", 147, 280, 453, ""],
        ["M24 月营收（万元）", 515, 1190, 2300, ""],
        ["M36 月营收（万元）", 1645, 4080, 8950, ""],
        ["", "", "", "", ""],
        ["M36 卖家数", 18000, 30000, 60000, ""],
        ["M36 月活买家", 120000, 300000, 700000, ""],
        ["M36 月撮合需求", 250000, 700000, 1800000, ""],
        ["M36 月平台 GMV（亿）", 150, 400, 1000, ""],
        ["", "", "", "", ""],
        ["启动金（万元）", 300, 300, 300, "已有"],
        ["Pre-A 时点", "M9-M10", "M5-M6", "M5", ""],
        ["Pre-A 金额（万元）", 500, 1000, 1800, ""],
        ["Pre-A 估值（万元）", 4000, 7000, 12000, ""],
        ["A 轮时点", "M20-M24", "M14-M16", "M12-M14", ""],
        ["A 轮金额（万元）", 2500, 4000, 6000, ""],
        ["A 轮估值（万元）", 17500, 40000, 100000, ""],
        ["B 轮金额（万元）", 0, 8000, 15000, "保守可不做"],
        ["3 年总融资（万元）", 3000, 13000, 22800, ""],
        ["", "", "", "", ""],
        ["M36 估值（B 轮口径，亿元）", 12, 50, 200, ""],
    ]
    for r in rows:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)

    # 标黄关键行
    for row_idx in [4, 5, 8, 15, 25]:
        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).fill = TOTAL_FILL
            ws.cell(row=row_idx, column=col).font = BOLD_FONT

    widths = [28, 14, 14, 14, 32]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.row_dimensions[1].height = 32


def create_y1_sheet(wb, name):
    """Year 1 详细月度营收（按档）"""
    ws = wb.create_sheet(f"Y1 月度-{name}")

    ws["A1"] = f"Year 1 月度营收预测（{name}档）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:N1")
    ws.append([])

    headers = ["收入项"] + [f"M{i}" for i in range(1, 13)] + ["Y1 累计"]
    ws.append(headers)
    style_header(ws, 3)

    data = Y1_DATA[name]
    for category, vals in data.items():
        row = [category] + vals + [round(sum(vals), 1)]
        ws.append(row)

    # 合计行
    monthly_total = []
    for i in range(12):
        s = sum(data[cat][i] for cat in data)
        monthly_total.append(round(s, 1))
    total_row = ["月营收合计"] + monthly_total + [round(sum(monthly_total), 1)]
    ws.append(total_row)

    # 成本行
    cost = Y1_COST[name]
    ws.append(["月成本"] + cost + [sum(cost)])

    # 净利
    net = [round(monthly_total[i] - cost[i], 1) for i in range(12)]
    ws.append(["月净利"] + net + [round(sum(net), 1)])

    # 累计净利
    cum = []
    s = 0
    for v in net:
        s += v
        cum.append(round(s, 1))
    ws.append(["累计净利"] + cum + [""])

    style_data(ws, 4, ws.max_row, 14)

    # 加粗合计、净利、累计净利行
    for row_idx in [ws.max_row - 3, ws.max_row - 2, ws.max_row - 1, ws.max_row]:
        for col in range(1, 15):
            ws.cell(row=row_idx, column=col).font = BOLD_FONT
            ws.cell(row=row_idx, column=col).fill = TOTAL_FILL

    widths = [14] + [10] * 12 + [12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def create_y2y3_sheet(wb, name):
    """Y2-Y3 季度抽样营收（按档）"""
    ws = wb.create_sheet(f"Y2-Y3 抽样-{name}")

    ws["A1"] = f"Year 2-3 月度营收预测（{name}档，季度抽样）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:H1")
    ws.append([])

    headers = ["收入项", "M13", "M18", "M24", "M30", "M36", "Y2 累计", "Y3 累计"]
    ws.append(headers)
    style_header(ws, 3)

    data = Y23_SAMPLE[name]
    categories = ["会员费", "流量费", "订阅", "增值服务", "买家 SaaS", "数据/金融"]

    # 简化估算 Y2/Y3 累计：用 M13/M18/M24 估算 Y2，M25/M30/M36 估算 Y3
    # 这里直接给出预测值
    y2_total = YEARLY_SUMMARY[name]["Y2 营收"]
    y3_total = YEARLY_SUMMARY[name]["Y3 营收"]

    for cat in categories:
        # 月度抽样
        m13 = data["M13"][cat]
        m18 = data["M18"][cat]
        m24 = data["M24"][cat]
        m30 = data["M30"][cat]
        m36 = data["M36"][cat]

        # 各品类占比近似（手算）
        # 这里使用简化估算
        y2_cat = round((m13 + m18 + m24) * 4, 0)  # 近似 Y2 累计
        y3_cat = round((m24 + m30 + m36) * 4, 0)  # 近似 Y3 累计
        ws.append([cat, m13, m18, m24, m30, m36, y2_cat, y3_cat])

    # 月合计行
    m13_t = sum(data["M13"].values())
    m18_t = sum(data["M18"].values())
    m24_t = sum(data["M24"].values())
    m30_t = sum(data["M30"].values())
    m36_t = sum(data["M36"].values())
    ws.append(["月营收合计", m13_t, m18_t, m24_t, m30_t, m36_t, y2_total, y3_total])

    # 净利
    summary = YEARLY_SUMMARY[name]
    ws.append([])
    ws.append(["年度", "", "营收", "成本", "净利", "净利率", "", ""])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["Y2", "", summary["Y2 营收"], summary["Y2 成本"], summary["Y2 净利"],
              f"{summary['Y2 净利']/summary['Y2 营收']*100:.0f}%", "", ""])
    ws.append(["Y3", "", summary["Y3 营收"], summary["Y3 成本"], summary["Y3 净利"],
              f"{summary['Y3 净利']/summary['Y3 营收']*100:.0f}%", "", ""])

    style_data(ws, 4, ws.max_row, 8)

    # 标黄合计行
    total_row = 3 + len(categories) + 1
    for col in range(1, 9):
        ws.cell(row=total_row, column=col).font = BOLD_FONT
        ws.cell(row=total_row, column=col).fill = TOTAL_FILL

    widths = [16, 11, 11, 11, 11, 11, 12, 12]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def create_cashflow_sheet(wb):
    ws = wb.create_sheet("现金流与融资")

    ws["A1"] = "三档现金流与融资节奏"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["时点", "事件", "保守现金（万元）", "常规现金（万元）", "乐观现金（万元）"])
    style_header(ws, 3)

    rows = [
        ["M0", "启动金到账", 300, 300, 300],
        ["M3", "前 3 月烧钱", 120, 150, 180],
        ["M5", "现金告急/Pre-A 启动", -100, -25, 80],
        ["M6", "Pre-A 到账（保:¥500w 常:¥1000w 乐:¥1800w）", 600, 975, 1700],
        ["M9", "保守 Pre-A 到账", 600, 800, 1400],
        ["M12", "Y1 末", 200, 975, 1880],
        ["M15", "A 轮（常/乐）", 0, 3500, 6500],
        ["M18", "稳定运营", 0, 4200, 8500],
        ["M22", "A 轮（保守）", 2400, 5800, 11500],
        ["M24", "Y2 末", 2442, 7175, 14000],
        ["M28", "B 轮（乐观）", 4500, 12000, 30000],
        ["M30", "B 轮（常规）", 5500, 23000, 38000],
        ["M36", "Y3 末", 6800, 23000, 51000],
    ]
    for r in rows:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)

    # 红色高亮 M5（最危险时点）
    for col in range(1, 6):
        ws.cell(row=6, column=col).fill = PatternFill("solid", fgColor="FFE6E6")
        ws.cell(row=6, column=col).font = BOLD_FONT

    # 标黄关键里程碑
    for row_idx in [7, 9, 12, 15]:
        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).fill = TOTAL_FILL

    widths = [10, 38, 18, 18, 18]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def create_sensitivity_sheet(wb):
    ws = wb.create_sheet("敏感性分析")

    ws["A1"] = "三个最敏感变量"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:D1")
    ws.append([])

    ws.append(["敏感性 1：流量费付费渗透率（M24）"])
    ws.cell(row=3, column=1).font = BOLD_FONT
    ws.append(["付费率", "M24 月营收差异（万）", "年营收影响（万）", "影响等级"])
    style_header(ws, 4)
    ws.append(["50%", -180, -2160, "保守-1pp"])
    ws.append(["70%（基准）", 0, 0, "常规"])
    ws.append(["85%", 220, 2640, "乐观"])

    ws.append([])
    ws.append(["敏感性 2：单买家 LTV"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["单买家 LTV（元）", "LTV/CAC", "营收影响", "情景"])
    style_header(ws, ws.max_row)
    ws.append([18000, 6.0, "-40%", "保守"])
    ws.append([30000, 9.9, "0", "基准"])
    ws.append([48000, 15.9, "+60%", "乐观"])

    ws.append([])
    ws.append(["敏感性 3：卖家续费率"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["续费率", "卖家流失率/年", "M24 卖家数", "情景"])
    style_header(ws, ws.max_row)
    ws.append(["60%", "40%", 7000, "保守"])
    ws.append(["75%", "25%", 12000, "基准"])
    ws.append(["85%", "15%", 18000, "乐观"])

    ws.append([])
    ws.append(["风险预案"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["风险", "概率", "影响", "预案"])
    style_header(ws, ws.max_row)
    risks = [
        ["M5 数据不达预期，融资延迟", "30%", "致命", "紧缩预案 A"],
        ["卖家集体反弹（区域抵制）", "20%", "严重", "卖家委员会紧急会议+CEO 走访"],
        ["钢铁行业大幅下行（>15%）", "25%", "中", "行情服务反而成为新引擎"],
        ["找钢网/欧冶反扑", "15%", "中", "服务深度差异化"],
        ["AI 厂商成本上涨", "25%", "小", "多供应商竞标"],
        ["监管政策变化（金融/数据）", "10%", "大", "法务持续跟进"],
    ]
    for r in risks:
        ws.append(r)

    style_data(ws, 5, ws.max_row, 4)

    widths = [32, 14, 16, 36]
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def main():
    wb = Workbook()
    create_summary_sheet(wb)
    for name in ["保守", "常规", "乐观"]:
        create_y1_sheet(wb, name)
    for name in ["保守", "常规", "乐观"]:
        create_y2y3_sheet(wb, name)
    create_cashflow_sheet(wb)
    create_sensitivity_sheet(wb)

    output = "docs/06-财务预测/3年营收测算-三档情景.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")
    print(f"✓ Sheets: 总览 / Y1×3 档 / Y2-Y3×3 档 / 现金流 / 敏感性 = 9 sheets")


if __name__ == "__main__":
    main()
