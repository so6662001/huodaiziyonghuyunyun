"""
生成用户增长方案 Excel 工具：
1. 渠道 ROI 计算器
2. 12 个月预算分配
3. 月度对账模板
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
SUCCESS_FILL = PatternFill("solid", fgColor="D1FAE5")
WARNING_FILL = PatternFill("solid", fgColor="FEF3C7")
DANGER_FILL = PatternFill("solid", fgColor="FEE2E2")


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


def main():
    wb = Workbook()

    # Sheet 0: 总览
    ws = wb.active
    ws.title = "0-总览"
    ws["A1"] = "用户增长方案 Excel 工具（资金约束版）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:F1")
    ws.append([])

    ws.append(["核心约束", "", "", "", "", ""])
    ws.cell(row=3, column=1).font = Font(name="微软雅黑", size=12, bold=True)

    rows = [
        ["Y1 总预算", "¥150 万", "占总成本 22%", "", "", ""],
        ["卖家 CAC 上限", "¥1286/家", "Y1 新增 700 家", "", "", ""],
        ["买家 CAC 上限", "¥50/家", "Y1 新增 12000 家", "", "", ""],
        ["LTV/CAC", "卖家 14x / 买家 30x", "极健康", "", "", ""],
    ]
    for r in rows:
        ws.append(r)

    ws.append([])
    ws.append(["📋 5 大引擎"])
    ws.cell(row=ws.max_row, column=1).font = Font(name="微软雅黑", size=12, bold=True)
    ws.append(["#", "引擎", "Y1 预算", "占比", "卖家产出", "买家产出"])
    style_header(ws, ws.max_row, 6)

    engines = [
        [1, "反向邀请", "¥30 万", "20%", "150", "2000"],
        [2, "企微群运营", "¥40 万", "27%", "50", "6000"],
        [3, "内容+短视频", "¥20 万", "13%", "20", "2000"],
        [4, "区域地推", "¥50 万", "33%", "400", "500"],
        [5, "PR+行业活动", "¥10 万", "7%", "80", "1500"],
        ["合计", "", "¥150 万", "100%", "700", "12000"],
    ]
    for r in engines:
        ws.append(r)

    style_data(ws, 12, ws.max_row, 6)
    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = SUCCESS_FILL

    set_widths(ws, [14, 18, 14, 12, 14, 14])

    # Sheet 1: 月度预算分配
    ws1 = wb.create_sheet("1-月度预算分配")
    ws1["A1"] = "12 个月预算分配（按引擎×月份）"
    ws1["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws1.merge_cells("A1:H1")
    ws1.append([])

    headers = ["月份", "反向邀请", "群运营", "内容+短视频", "区域地推", "PR+活动", "月总", "累计"]
    ws1.append(headers)
    style_header(ws1, 3, 8)

    # 单位：万元
    monthly = [
        ["M1", 0.5, 1.0, 0.5, 0.5, 0.5, 3.0, 3.0],
        ["M2", 0.5, 1.0, 0.5, 0.5, 0.5, 3.0, 6.0],
        ["M3", 3.0, 3.0, 2.0, 3.0, 1.0, 12.0, 18.0],  # 实际 ¥10 万但试点期略松
        ["M4", 2.0, 3.0, 3.0, 2.0, 1.0, 11.0, 29.0],
        ["M5", 3.0, 3.0, 2.0, 3.0, 1.0, 12.0, 41.0],
        ["M6", 4.0, 3.0, 2.0, 4.0, 1.0, 14.0, 55.0],
        ["M7", 3.0, 4.0, 3.0, 4.0, 1.0, 15.0, 70.0],
        ["M8", 3.0, 3.0, 3.0, 4.0, 3.0, 16.0, 86.0],
        ["M9", 3.0, 3.0, 2.0, 4.0, 3.0, 15.0, 101.0],
        ["M10", 4.0, 3.0, 2.0, 5.0, 2.0, 16.0, 117.0],
        ["M11", 4.0, 3.0, 1.0, 5.0, 4.0, 17.0, 134.0],
        ["M12", 3.0, 3.0, 0.5, 5.0, 5.5, 17.0, 151.0],
    ]
    for r in monthly:
        ws1.append(r)

    # 合计
    totals = ["Y1 合计"]
    for col_idx in range(2, 8):
        totals.append(sum(r[col_idx-1] for r in monthly))
    ws1.append(totals[:7] + [""])  # 累计列留空

    style_data(ws1, 4, ws1.max_row, 8)

    for cell in ws1[ws1.max_row]:
        cell.font = BOLD_FONT
        cell.fill = SUCCESS_FILL

    set_widths(ws1, [10, 12, 12, 14, 12, 12, 12, 12])

    # Sheet 2: 渠道 ROI 计算器
    ws2 = wb.create_sheet("2-渠道ROI计算器")
    ws2["A1"] = "每月渠道 ROI 监控（自填）"
    ws2["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws2.merge_cells("A1:H1")
    ws2.append([])

    ws2.append(["渠道", "月预算(万)", "月触达", "月转化(家)", "CAC(元)", "LTV(元)", "LTV/CAC", "ROI 等级"])
    style_header(ws2, 3, 8)

    channels = [
        ["反向邀请", 2.5, "", "", "", 30000, "", "🟢/🟡/🟠/🔴"],
        ["群运营", 3.3, "", "", "", 1500, "", "🟢/🟡/🟠/🔴"],
        ["内容+短视频", 1.7, "", "", "", 1500, "", "🟢/🟡/🟠/🔴"],
        ["区域地推", 4.2, "", "", "", 18000, "", "🟢/🟡/🟠/🔴"],
        ["PR+活动", 0.8, "", "", "", 0, "难量化", "-"],
    ]
    for r in channels:
        ws2.append(r)

    style_data(ws2, 4, ws2.max_row, 8)

    ws2.append([])
    ws2.append(["ROI 等级判定标准"])
    ws2.cell(row=ws2.max_row, column=1).font = BOLD_FONT

    standards = [
        ["LTV/CAC > 15x", "🟢 加投", "下月预算 +50%"],
        ["LTV/CAC 8-15x", "🟡 维持", "下月预算不变"],
        ["LTV/CAC 5-8x", "🟠 砍减", "下月预算 -30%"],
        ["LTV/CAC < 5x", "🔴 砍掉", "立即停投"],
    ]
    ws2.append(["LTV/CAC", "等级", "动作", "", "", "", "", ""])
    style_header(ws2, ws2.max_row, 3)
    for r in standards:
        ws2.append(r + ["", "", "", "", ""])

    style_data(ws2, ws2.max_row - 4, ws2.max_row, 8)

    set_widths(ws2, [14, 12, 12, 12, 14, 12, 12, 16])

    # Sheet 3: 裂变机制详细
    ws3 = wb.create_sheet("3-裂变机制详细")
    ws3["A1"] = "5 大裂变机制（务实精细版）"
    ws3["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws3.merge_cells("A1:G1")
    ws3.append([])

    ws3.append(["机制", "目标", "单次成本", "Y1 预算", "预期产出", "LTV/CAC", "优先级"])
    style_header(ws3, 3, 7)

    mechanisms = [
        ["A 卖家邀请买家", "拉买家", "¥890", "¥30 万", "200 M4 + 1000 M1-M3", "34x", "⭐⭐⭐⭐⭐"],
        ["B 买家邀请买家", "买家裂变", "¥250", "¥10 万", "400 家", "6x", "⭐⭐⭐"],
        ["C 内测合伙人推荐", "高质量卖家", "¥500-2000", "¥10 万", "90 家", "9-36x", "⭐⭐⭐⭐⭐"],
        ["D 群主带群", "群裂变", "¥1000/群", "¥15 万", "4000 家买家", "45x", "⭐⭐⭐⭐⭐"],
        ["E KOL 引荐", "品牌+卖家", "难量化", "¥5 万", "30-50 家", "难量化", "⭐⭐⭐"],
        ["合计", "", "", "¥70 万", "~5500 家", "", ""],
    ]
    for r in mechanisms:
        ws3.append(r)

    style_data(ws3, 4, ws3.max_row, 7)

    for cell in ws3[ws3.max_row]:
        cell.font = BOLD_FONT
        cell.fill = SUCCESS_FILL

    # 详细金额
    ws3.append([])
    ws3.append(["卖家邀请买家 5 级里程碑"])
    ws3.cell(row=ws3.max_row, column=1).font = BOLD_FONT
    ws3.append(["里程碑", "卖家奖励", "买家奖励", "触发条件", "", "", ""])
    style_header(ws3, ws3.max_row, 4)

    milestones = [
        ["M1 注册", "¥20", "¥30 (运费券)", "营业执照认证"],
        ["M2 首发需求", "¥30", "¥20 (积分)", "7 日内首次询盘"],
        ["M3 有效互动", "¥80", "/", "14 日内 ≥3 次沟通"],
        ["M4 首单成交", "¥200", "¥150 (券)", "30 日内 ≥¥5 万"],
        ["M5 月活买家", "¥120/月×3", "优质认证", "次月活跃"],
        ["总价值", "¥690", "¥200", ""],
    ]
    for r in milestones:
        ws3.append(r + ["", "", ""])

    style_data(ws3, ws3.max_row - 6, ws3.max_row, 7)
    for cell in ws3[ws3.max_row]:
        cell.font = BOLD_FONT
        cell.fill = WARNING_FILL

    set_widths(ws3, [22, 16, 14, 14, 22, 12, 12])

    # Sheet 4: 12 月增长目标
    ws4 = wb.create_sheet("4-增长目标")
    ws4["A1"] = "12 个月增长目标（务实精细版）"
    ws4["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws4.merge_cells("A1:F1")
    ws4.append([])

    ws4.append(["月份", "新增卖家", "新增买家", "累计活跃卖家", "累计买家", "月营收(万)"])
    style_header(ws4, 3, 6)

    targets = [
        ["M1", 8, 50, 206, 250, 8.65],
        ["M2", 10, 80, 214, 330, 8.99],
        ["M3", 20, 300, 232, 630, 10.64],
        ["M4", 35, 600, 264, 1230, 12.83],
        ["M5", 35, 800, 296, 2030, 15.22],
        ["M6", 40, 1200, 333, 3230, 18.84],
        ["M7", 60, 1500, 389, 4730, 23.62],
        ["M8", 70, 1800, 454, 6530, 29.46],
        ["M9", 80, 2000, 528, 8530, 36.46],
        ["M10", 100, 1700, 621, 10230, 45.15],
        ["M11", 120, 1500, 733, 11730, 55.88],
        ["M12", 130, 1300, 854, 13030, 67.67],
        ["Y1 合计", 708, 12830, "-", "-", "¥333 万"],
    ]
    for r in targets:
        ws4.append(r)

    style_data(ws4, 4, ws4.max_row, 6)

    for cell in ws4[ws4.max_row]:
        cell.font = BOLD_FONT
        cell.fill = SUCCESS_FILL

    set_widths(ws4, [10, 12, 12, 14, 14, 14])

    # Sheet 5: 应急预案
    ws5 = wb.create_sheet("5-应急预案")
    ws5["A1"] = "应急预案（B/C 计划）"
    ws5["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws5.merge_cells("A1:D1")
    ws5.append([])

    ws5.append(["计划", "触发条件", "预算调整", "保留渠道"])
    style_header(ws5, 3, 4)

    plans = [
        ["A 基准", "数据达成精细务实版", "¥150 万", "全部 5 大引擎"],
        ["B 计划（-30%）", "M3 末增长 < 50% 计划 / 单渠道 ROI < 5x 持续 2 月 / 现金 < 4 月", "¥105 万", "反向+群（30+30 万）+ 部分地推（30 万）+ 部分内容（10 万）+ 减半 PR（5 万）"],
        ["C 计划（-67%）", "B 计划仍不达预期 / 资金链断裂", "¥50 万", "仅反向（20 万）+ 群主带群（15 万）+ 1 人地推（10 万）+ 极少 PR（5 万）"],
    ]
    for r in plans:
        ws5.append(r)

    style_data(ws5, 4, ws5.max_row, 4)

    # B 计划黄色，C 计划红色
    for col in range(1, 5):
        ws5.cell(row=5, column=col).fill = WARNING_FILL
        ws5.cell(row=6, column=col).fill = DANGER_FILL

    set_widths(ws5, [14, 40, 16, 50])

    output = "docs/12-用户增长终版/渠道ROI计算器.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")
    print(f"✓ 6 个 Sheet")


if __name__ == "__main__":
    main()
