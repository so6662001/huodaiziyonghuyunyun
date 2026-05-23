"""
生成「精细务实版营收拆解」Excel 工作版

输出：docs/11-务实版财务测算/营收精细拆解-工作底稿.xlsx

特点：
- 8 个 Sheet 完整拆解
- 含可调参数（黄色单元格）
- 含每月明细
- CFO 工作底稿
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
PARAM_FILL = PatternFill("solid", fgColor="FFF2CC")  # 可调参数：黄色
RESULT_FILL = PatternFill("solid", fgColor="D1FAE5")  # 结果：绿色
HIGHLIGHT_FILL = PatternFill("solid", fgColor="FEE2E2")  # 重点：红色
NORMAL_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="center")


def style_header(ws, row, n_cols):
    for col in range(1, n_cols + 1):
        cell = ws.cell(row=row, column=col)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP
        cell.border = BORDER


def style_data(ws, start_row, end_row, n_cols, align=WRAP):
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, min_col=1, max_col=n_cols):
        for cell in row:
            if not cell.font.bold:
                cell.font = NORMAL_FONT
            cell.alignment = align
            cell.border = BORDER


def set_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ============ Sheet 0: 使用说明 ============
def create_intro(wb):
    ws = wb.active
    ws.title = "0-使用说明"

    rows = [
        ["货袋子营收精细拆解 - 工作底稿", "", "", ""],
        ["", "", "", ""],
        ["版本", "v1.0 务实精细版", "", ""],
        ["用途", "CFO 内部预算 + CEO 决策依据", "", ""],
        ["更新", "每月一次复盘 vs 实际", "", ""],
        ["", "", "", ""],
        ["📋 Sheet 说明", "", "", ""],
        ["0", "使用说明", "本表", ""],
        ["1", "起点参数（M0 现状）", "200 家活跃 + 加权年费", ""],
        ["2", "可调参数（黄色单元格）", "CFO 调这里", ""],
        ["3", "Y1 卖家数推算", "M1-M12 每月活跃数", ""],
        ["4", "Y1 月营收明细", "5 项收入 × 12 月", ""],
        ["5", "Y1 现金流", "营收/成本/净亏/累计", ""],
        ["6", "Y2-Y3 概览", "季度抽样", ""],
        ["7", "敏感性分析", "参数 ±10% 影响", ""],
        ["", "", "", ""],
        ["📋 关键数字", "", "", ""],
        ["Y1 营收", "¥333 万", "", ""],
        ["Y1 成本", "¥690 万", "", ""],
        ["Y1 净亏", "-¥357 万", "", ""],
        ["M12 月营收", "¥67.7 万", "", ""],
        ["M12 月度盈亏", "-¥22 万（尚未平衡）", "", ""],
        ["盈亏平衡时点", "M15-16", "", ""],
        ["3 年累计", "¥0.84 亿", "", ""],
        ["", "", "", ""],
        ["📋 关键认知", "", "", ""],
        ["1", "M3 真实流量费仅 ¥9000（30 家种子 × ¥300）", "", ""],
        ["2", "M12 真实付费卖家 854 家（不是 2000+ 家）", "", ""],
        ["3", "Y1 营收 66% 来自会员费（流量费仍是 28%）", "", ""],
        ["4", "盈亏平衡推迟到 M15-16（不是 M12）", "", ""],
        ["5", "Pre-A 必须 M7-M8 完成，¥500-800 万", "", ""],
        ["", "", "", ""],
        ["📋 颜色约定", "", "", ""],
        ["黄色 (FFF2CC)", "可调参数", "CFO 可修改", ""],
        ["绿色 (D1FAE5)", "重要结果", "公式自动算", ""],
        ["红色 (FEE2E2)", "警示/总计", "重点关注", ""],
    ]

    for r in rows:
        ws.append(r)

    ws["A1"].font = Font(name="微软雅黑", size=18, bold=True, color="1F4E78")
    ws.merge_cells("A1:D1")

    for row_idx in [7, 17, 26, 32]:
        for col in range(1, 5):
            cell = ws.cell(row=row_idx, column=col)
            cell.font = Font(name="微软雅黑", size=12, bold=True, color="1F4E78")

    set_widths(ws, [16, 28, 22, 12])


# ============ Sheet 1: 起点参数 ============
def create_starting_params(wb):
    ws = wb.create_sheet("1-起点参数(M0)")
    ws["A1"] = "M0 起点参数"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:D1")
    ws.append([])

    ws.append(["分类", "字段", "值", "依据"])
    style_header(ws, 3, 4)

    rows = [
        ["卖家结构", "累计入驻", 300, "你提供的真实数据"],
        ["卖家结构", "真正付费活跃", 200, "300 × 67%（行业典型）"],
        ["卖家结构", "  基础会员（¥3000）", 80, "40% 价格敏感小卖家"],
        ["卖家结构", "  标准会员（¥6000）", 100, "50% 主流"],
        ["卖家结构", "  黑金会员（¥9800）", 20, "10% 头部"],
        ["卖家结构", "加权平均年费", 5040, "(80×3000+100×6000+20×9800)/200"],
        ["", "", "", ""],
        ["流失率", "A 类自然流失", "1.5%/月", "高活跃"],
        ["流失率", "B 类自然流失", "3.0%/月", "中等"],
        ["流失率", "C 类自然流失", "5.0%/月", "低活跃"],
        ["流失率", "加权平均（无改革）", "2.6%/月", "-"],
        ["流失率", "改革后（前6月）", "1.0%/月", "客户成功干预"],
        ["流失率", "改革后（后6月）", "1.5%/月", "-"],
        ["", "", "", ""],
        ["新增", "M1 新增", "5-10 家", "团队准备期"],
        ["新增", "M3 新增", "20 家/月", "新功能上线"],
        ["新增", "M6 新增", "40 家/月", "增长期"],
        ["新增", "M9 新增", "80 家/月", "提速"],
        ["新增", "M12 新增", "130 家/月", "规模化前夜"],
    ]
    for r in rows:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 4)
    set_widths(ws, [14, 24, 16, 28])


# ============ Sheet 2: 可调参数 ============
def create_params(wb):
    ws = wb.create_sheet("2-可调参数")
    ws["A1"] = "可调参数（CFO 在这里调整）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["参数代号", "参数名", "默认值", "可调范围", "敏感性"])
    style_header(ws, 3, 5)

    params = [
        ["P1", "M0 活跃付费卖家数", 200, "150-250", "高"],
        ["P2", "卖家加权年费", 5040, "¥4200-¥5500", "中"],
        ["P3", "月新增（M1）", 8, "5-15", "高"],
        ["P4", "月新增（M6）", 40, "25-60", "高"],
        ["P5", "月新增（M12）", 130, "80-180", "高"],
        ["P6", "月流失率（前6月）", "1.0%", "0.5%-2%", "中"],
        ["P7", "月流失率（后6月）", "1.5%", "1%-2.5%", "中"],
        ["P8", "流量费付费率（M12）", "50%", "30%-65%", "中"],
        ["P9", "流量费均价", 540, "¥400-¥800", "中"],
        ["P10", "订阅率（M12）", "9%", "5%-15%", "低"],
        ["P11", "增值服务渗透（M12）", "17%", "10%-25%", "低"],
        ["P12", "买家 SaaS 签约率", "5%", "3%-10%", "低"],
    ]
    for r in params:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)

    # 默认值列高亮（黄色）
    for row_idx in range(4, ws.max_row + 1):
        ws.cell(row=row_idx, column=3).fill = PARAM_FILL

    set_widths(ws, [10, 24, 14, 14, 12])


# ============ Sheet 3: Y1 卖家数推算 ============
def create_seller_count(wb):
    ws = wb.create_sheet("3-Y1卖家数推算")
    ws["A1"] = "Y1 每月活跃付费卖家数推算"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:G1")
    ws.append([])

    ws.append(["月份", "上月末活跃", "本月新增", "本月流失", "本月末活跃", "加权年费", "月会员费"])
    style_header(ws, 3, 7)

    data = [
        ["M0", "-", "-", "-", 200, 5040, "-"],
        ["M1", 200, 8, 2, 206, 5040, 86520],
        ["M2", 206, 10, 2, 214, 5040, 89880],
        ["M3", 214, 20, 2, 232, 5040, 97440],
        ["M4", 232, 35, 3, 264, 5050, 111100],
        ["M5", 264, 35, 3, 296, 5060, 124813],
        ["M6", 296, 40, 4, 333, 5080, 140970],
        ["M7", 333, 60, 4, 389, 5100, 165325],
        ["M8", 389, 70, 5, 454, 5120, 193707],
        ["M9", 454, 80, 6, 528, 5150, 226600],
        ["M10", 528, 100, 7, 621, 5180, 268065],
        ["M11", 621, 120, 8, 733, 5200, 317633],
        ["M12", 733, 130, 9, 854, 5230, 372201],
    ]
    for r in data:
        ws.append(r)

    ws.append(["Y1 合计", "-", 708, 55, "-", "-", 2194254])
    style_data(ws, 4, ws.max_row, 7)

    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = RESULT_FILL

    set_widths(ws, [8, 14, 12, 12, 14, 12, 14])


# ============ Sheet 4: Y1 月营收明细 ============
def create_revenue_detail(wb):
    ws = wb.create_sheet("4-Y1月营收明细")
    ws["A1"] = "Y1 月营收 5 项明细（务实精细版）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:H1")
    ws.append([])

    ws.append(["月份", "活跃卖家", "会员费", "流量费", "订阅", "增值", "SaaS", "月营收"])
    style_header(ws, 3, 8)

    # 数据来自前面的拆解（单位：元）
    data = [
        ["M1", 206, 86520, 0, 0, 0, 0, 86520],
        ["M2", 214, 89880, 0, 0, 0, 0, 89880],
        ["M3", 232, 97440, 9000, 0, 0, 0, 106440],
        ["M4", 264, 111100, 16450, 0, 750, 0, 128300],
        ["M5", 296, 124813, 26000, 0, 1350, 0, 152163],
        ["M6", 333, 140970, 41850, 3000, 2550, 0, 188370],
        ["M7", 389, 165325, 61440, 5120, 4320, 0, 236205],
        ["M8", 454, 193707, 86500, 7820, 6560, 0, 294587],
        ["M9", 528, 226600, 115440, 11200, 9860, 1500, 364600],
        ["M10", 621, 268065, 150660, 15480, 13770, 3500, 451475],
        ["M11", 733, 317633, 193600, 21830, 19800, 6000, 558863],
        ["M12", 854, 372201, 239120, 29260, 26100, 10000, 676681],
    ]
    for r in data:
        ws.append(r)

    # 合计行
    total_row = ["Y1 累计", "-",
                 sum(r[2] for r in data),
                 sum(r[3] for r in data),
                 sum(r[4] for r in data),
                 sum(r[5] for r in data),
                 sum(r[6] for r in data),
                 sum(r[7] for r in data)]
    ws.append(total_row)

    style_data(ws, 4, ws.max_row, 8)

    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = RESULT_FILL

    # 数字格式
    for row_idx in range(4, ws.max_row + 1):
        for col_idx in range(3, 9):
            ws.cell(row=row_idx, column=col_idx).number_format = '#,##0'

    set_widths(ws, [10, 12, 12, 12, 10, 10, 10, 14])

    # 添加比例总结
    ws.append([])
    ws.append(["Y1 收入结构占比"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    total = sum(r[7] for r in data)
    ws.append(["会员费", "", f"{sum(r[2] for r in data)/total*100:.1f}%", "", "", "", "", ""])
    ws.append(["流量费", "", f"{sum(r[3] for r in data)/total*100:.1f}%", "", "", "", "", ""])
    ws.append(["订阅", "", f"{sum(r[4] for r in data)/total*100:.1f}%", "", "", "", "", ""])
    ws.append(["增值服务", "", f"{sum(r[5] for r in data)/total*100:.1f}%", "", "", "", "", ""])
    ws.append(["买家 SaaS", "", f"{sum(r[6] for r in data)/total*100:.1f}%", "", "", "", "", ""])


# ============ Sheet 5: Y1 现金流 ============
def create_cashflow(wb):
    ws = wb.create_sheet("5-Y1现金流")
    ws["A1"] = "Y1 现金流（务实精细版）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:F1")
    ws.append([])

    ws.append(["月份", "月营收", "月成本", "月净亏", "累计净亏", "现金余额"])
    style_header(ws, 3, 6)

    cash = 3000000  # ¥300 万启动金
    data = [
        ["M1", 86520, 300000, -213480, -213480],
        ["M2", 89880, 320000, -230120, -443600],
        ["M3", 106440, 380000, -273560, -717160],
        ["M4", 128300, 420000, -291700, -1008860],
        ["M5", 152163, 480000, -327837, -1336697],
        ["M6", 188370, 550000, -361630, -1698327],
        ["M7", 236205, 650000, -413795, -2112122],
        ["M8", 294587, 730000, -435413, -2547535],
        ["M9", 364600, 820000, -455400, -3002935],
        ["M10", 451475, 900000, -448525, -3451460],
        ["M11", 558863, 900000, -341137, -3792597],
        ["M12", 676681, 900000, -223319, -4015916],
    ]
    for r in data:
        balance = cash + r[4]
        ws.append(r + [balance])
        # 红色高亮负数
        if balance < 500000:
            for col in range(1, 7):
                ws.cell(row=ws.max_row, column=col).fill = HIGHLIGHT_FILL

    style_data(ws, 4, ws.max_row, 6)

    for row_idx in range(4, ws.max_row + 1):
        for col_idx in range(2, 7):
            ws.cell(row=row_idx, column=col_idx).number_format = '#,##0'

    set_widths(ws, [10, 14, 14, 14, 14, 16])

    # 关键洞察
    ws.append([])
    ws.append(["关键洞察"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["现金跑道", "M9 现金告急，必须 M7-M8 完成 Pre-A"])
    ws.append(["Pre-A 募集额", "¥500-800 万（含安全垫）"])
    ws.append(["M15-16 盈亏平衡", "（不是 M12）"])


# ============ Sheet 6: Y2-Y3 概览 ============
def create_y23(wb):
    ws = wb.create_sheet("6-Y2Y3概览")
    ws["A1"] = "Y2-Y3 季度概览（务实精细版）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:D1")
    ws.append([])

    ws.append(["月份", "活跃卖家", "月营收", "季度累计"])
    style_header(ws, 3, 4)

    data = [
        ["M13", 980, 750000, 750000],
        ["M15", 1180, 950000, 2550000],
        ["M18", 1500, 1350000, 5850000],
        ["M21", 1830, 1800000, 10550000],
        ["M24", 2200, 2350000, 16600000],
        ["—Y2 累计 ¥1660 万—", "", "", ""],
        ["M27", 2800, 3200000, 25400000],
        ["M30", 3500, 4400000, 38800000],
        ["M33", 4200, 5800000, 55600000],
        ["M36", 5000, 7600000, 76000000],
        ["—Y3 累计 ¥6400 万—", "", "", ""],
        ["", "", "", ""],
        ["3 年累计", "", "", 83930000],
    ]
    for r in data:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 4)

    for row_idx in [9, 14, 16]:
        for col in range(1, 5):
            ws.cell(row=row_idx, column=col).fill = RESULT_FILL
            ws.cell(row=row_idx, column=col).font = BOLD_FONT

    for row_idx in range(4, ws.max_row + 1):
        for col_idx in range(2, 5):
            cell = ws.cell(row=row_idx, column=col_idx)
            if cell.value and isinstance(cell.value, (int, float)):
                cell.number_format = '#,##0'

    set_widths(ws, [22, 14, 16, 16])


# ============ Sheet 7: 敏感性分析 ============
def create_sensitivity(wb):
    ws = wb.create_sheet("7-敏感性分析")
    ws["A1"] = "敏感性分析（务实精细版）"
    ws["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws.merge_cells("A1:D1")
    ws.append([])

    ws.append(["参数", "基准", "-10% Y1 影响", "+10% Y1 影响"])
    style_header(ws, 3, 4)

    data = [
        ["月新增卖家数", "见 Sheet 2", "-¥35 万", "+¥35 万"],
        ["卖家加权年费", "¥5040", "-¥22 万", "+¥22 万"],
        ["流量费付费率", "M12: 50%", "-¥9 万", "+¥9 万"],
        ["流量费均价", "¥540", "-¥9 万", "+¥9 万"],
        ["月流失率", "1%/1.5%", "+¥10 万", "-¥10 万"],
    ]
    for r in data:
        ws.append(r)

    ws.append([])
    ws.append(["组合情景"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT

    ws.append(["情景", "Y1 营收", "Y1 净亏", "盈亏平衡"])
    style_header(ws, ws.max_row, 4)
    ws.append(["保守（-30%）", "¥225 万", "-¥465 万", "M20"])
    ws.append(["基准", "¥333 万", "-¥357 万", "M15-16"])
    ws.append(["乐观（+30%）", "¥465 万", "-¥250 万", "M11-12"])

    style_data(ws, 4, ws.max_row, 4)
    set_widths(ws, [22, 16, 18, 16])


def main():
    wb = Workbook()
    create_intro(wb)
    create_starting_params(wb)
    create_params(wb)
    create_seller_count(wb)
    create_revenue_detail(wb)
    create_cashflow(wb)
    create_y23(wb)
    create_sensitivity(wb)

    output = "docs/11-务实版财务测算/营收精细拆解-工作底稿.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")
    print(f"✓ 8 个 Sheet（含使用说明+起点参数+可调参数+卖家数+月营收+现金流+Y2Y3+敏感性）")


if __name__ == "__main__":
    main()
