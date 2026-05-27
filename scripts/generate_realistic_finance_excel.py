"""
生成「务实版财务测算」Excel
- 3 年三档对比（旧 vs 务实）
- 100 家测算（务实版）

输出：
- docs/11-务实版财务测算/3年营收测算-务实版.xlsx
- docs/11-务实版财务测算/100家测算-务实版.xlsx
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
OLD_FILL = PatternFill("solid", fgColor="FEE2E2")
NEW_FILL = PatternFill("solid", fgColor="D1FAE5")
HIGHLIGHT_FILL = PatternFill("solid", fgColor="FFF2CC")


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


# ================ Excel 1: 3 年测算-务实版 ================
def create_3year_excel():
    wb = Workbook()

    # Sheet 1: 总览对比
    ws = wb.active
    ws.title = "0-总览(对比)"
    ws["A1"] = "3 年营收测算 - 旧版（乐观）vs 务实版（内部用）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["", "旧版常规", "务实版常规", "差距", "说明"])
    style_header(ws, 3, 5)

    data = [
        ["Y1 营收", "¥1340 万", "¥659 万", "-51%", "现实校准"],
        ["Y2 营收", "¥7600 万", "¥3920 万", "-48%", "团队效能折扣"],
        ["Y3 营收", "¥30860 万", "¥13900 万", "-55%", "市场渗透折扣"],
        ["3 年累计", "¥3.98 亿", "¥1.85 亿", "-54%", ""],
        ["", "", "", "", ""],
        ["Y1 成本", "¥2038 万", "¥942 万", "-54%", "精益团队"],
        ["Y2 成本", "¥5400 万", "¥2510 万", "-54%", ""],
        ["Y3 成本", "¥15000 万", "¥4740 万", "-68%", ""],
        ["", "", "", "", ""],
        ["Y1 净亏", "-¥698 万", "-¥282 万", "少烧 60%", "资金压力大幅缓解"],
        ["Y2 净利", "+¥2200 万", "+¥1410 万", "-36%", "提前盈利"],
        ["Y3 净利", "+¥15860 万", "+¥9160 万", "-42%", "丰收期"],
        ["", "", "", "", ""],
        ["M12 月营收", "¥270 万", "¥130 万", "-52%", ""],
        ["M24 月营收", "¥1190 万", "¥530 万", "-55%", ""],
        ["M36 月营收", "¥4080 万", "¥2100 万", "-49%", ""],
        ["", "", "", "", ""],
        ["M36 估值", "¥40-60 亿", "¥20-30 亿", "-50%", "PS 倍数不变"],
        ["总融资需求", "¥1.3 亿", "¥7000 万", "-46%", "少稀释 + 估值更高"],
    ]
    for r in data:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)

    # 标记关键行
    for row_idx in [13, 22]:  # Y1 净亏、总融资
        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).fill = HIGHLIGHT_FILL
            ws.cell(row=row_idx, column=col).font = BOLD_FONT

    set_widths(ws, [18, 16, 16, 14, 30])

    # Sheet 2: 务实版 Y1 月度
    ws2 = wb.create_sheet("1-Y1月度详细")
    ws2["A1"] = "Y1 月度详细预测（务实版常规档）"
    ws2["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="047857")
    ws2.merge_cells("A1:J1")
    ws2.append([])

    ws2.append(["月", "会员费", "流量费", "订阅", "增值服务", "买家SaaS", "月营收", "月成本", "月净利", "累计净利"])
    style_header(ws2, 3, 10)

    monthly_data = [
        ["M1", 8, 0, 0, 0, 0, 8, 30.5, -22.5, -22.5],
        ["M2", 8.5, 0.3, 0, 0, 0, 8.8, 32, -23.2, -45.7],
        ["M3", 10, 1.5, 0.5, 0, 0, 12, 42, -30, -75.7],
        ["M4", 11, 3, 1, 0.5, 0, 15.5, 48, -32.5, -108.2],
        ["M5", 13, 5, 2, 1, 0, 21, 55, -34, -142.2],
        ["M6", 16, 10, 3, 2, 1, 32, 76, -44, -186.2],
        ["M7", 19, 15, 4, 3, 2, 43, 84, -41, -227.2],
        ["M8", 22, 22, 6, 5, 3, 58, 90, -32, -259.2],
        ["M9", 27, 30, 8, 7, 5, 77, 100, -23, -282.2],
        ["M10", 32, 40, 11, 10, 8, 101, 115, -14, -296.2],
        ["M11", 38, 50, 14, 13, 12, 127, 128, -1, -297.2],
        ["M12", 45, 60, 17, 16, 18, 156, 141, 15, -282.2],
    ]
    for r in monthly_data:
        ws2.append(r)

    ws2.append(["合计", 249.5, 236.8, 66.5, 57.5, 49, 659.3, 941.5, -282.2, "-"])
    style_data(ws2, 4, ws2.max_row, 10)

    for cell in ws2[ws2.max_row]:
        cell.font = BOLD_FONT
        cell.fill = HIGHLIGHT_FILL

    set_widths(ws2, [8, 10, 10, 10, 12, 12, 10, 10, 10, 14])

    # Sheet 3: 务实版 Y2-Y3 季度
    ws3 = wb.create_sheet("2-Y2Y3季度")
    ws3["A1"] = "Y2-Y3 季度预测（务实版常规档）"
    ws3["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="047857")
    ws3.merge_cells("A1:F1")
    ws3.append([])

    ws3.append(["季度", "累计卖家", "月营收(起→末)", "季度营收", "季度成本", "季度净利"])
    style_header(ws3, 3, 6)

    y2_y3 = [
        ["Y2-Q1 (M13-15)", 2400, "¥175→210 万", "¥570 万", "¥460 万", "+¥110 万"],
        ["Y2-Q2 (M16-18)", 3200, "¥240→290 万", "¥800 万", "¥570 万", "+¥230 万"],
        ["Y2-Q3 (M19-21)", 4000, "¥330→400 万", "¥1100 万", "¥680 万", "+¥420 万"],
        ["Y2-Q4 (M22-24)", 5000, "¥450→530 万", "¥1450 万", "¥800 万", "+¥650 万"],
        ["Y2 合计", "-", "-", "¥3920 万", "¥2510 万", "+¥1410 万"],
        ["", "", "", "", "", ""],
        ["Y3-Q1 (M25-27)", 6000, "¥600→730 万", "¥2000 万", "¥1050 万", "+¥950 万"],
        ["Y3-Q2 (M28-30)", 7000, "¥830→1000 万", "¥2700 万", "¥1140 万", "+¥1560 万"],
        ["Y3-Q3 (M31-33)", 8500, "¥1150→1400 万", "¥3700 万", "¥1230 万", "+¥2470 万"],
        ["Y3-Q4 (M34-36)", 10000, "¥1600→2100 万", "¥5500 万", "¥1320 万", "+¥4180 万"],
        ["Y3 合计", "-", "-", "¥13900 万", "¥4740 万", "+¥9160 万"],
    ]
    for r in y2_y3:
        ws3.append(r)

    style_data(ws3, 4, ws3.max_row, 6)
    for row_idx in [8, 14]:  # 合计行
        for col in range(1, 7):
            ws3.cell(row=row_idx, column=col).fill = HIGHLIGHT_FILL
            ws3.cell(row=row_idx, column=col).font = BOLD_FONT

    set_widths(ws3, [18, 14, 18, 14, 14, 14])

    # Sheet 4: 务实版三档情景
    ws4 = wb.create_sheet("3-三档情景")
    ws4["A1"] = "务实版三档情景对比"
    ws4["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="1F4E78")
    ws4.merge_cells("A1:E1")
    ws4.append([])

    ws4.append(["维度", "保守", "常规（基准）", "乐观", "差异说明"])
    style_header(ws4, 3, 5)

    scenarios = [
        ["Y1 营收", "¥460 万", "¥659 万", "¥920 万", "买家增长速度差异"],
        ["Y2 营收", "¥2350 万", "¥3920 万", "¥6500 万", "+流量费付费率"],
        ["Y3 营收", "¥7800 万", "¥13900 万", "¥21300 万", "+SaaS 渗透"],
        ["3 年累计", "¥1.06 亿", "¥1.85 亿", "¥2.87 亿", ""],
        ["", "", "", "", ""],
        ["M36 月营收", "¥1200 万", "¥2100 万", "¥3500 万", ""],
        ["M36 团队", 100, 150, 200, "按需扩"],
        ["M36 估值", "¥6-10 亿", "¥20-30 亿", "¥50-70 亿", "PS 5-15x"],
        ["", "", "", "", ""],
        ["总融资需求", "¥3500 万", "¥7000 万", "¥1.3 亿", ""],
        ["LTV/CAC", "8x", "12x", "16x", ""],
    ]
    for r in scenarios:
        ws4.append(r)

    style_data(ws4, 4, ws4.max_row, 5)
    set_widths(ws4, [16, 14, 18, 14, 22])

    # Sheet 5: 融资计划
    ws5 = wb.create_sheet("4-融资计划")
    ws5["A1"] = "务实版融资节奏"
    ws5["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="1F4E78")
    ws5.merge_cells("A1:E1")
    ws5.append([])

    ws5.append(["阶段", "旧版时点", "务实版时点", "旧版金额", "务实版金额"])
    style_header(ws5, 3, 5)

    funding = [
        ["种子（已完成）", "M0", "M0", "¥300 万", "¥300 万"],
        ["Pre-A", "M5-M6", "M8-M10", "¥1000 万", "¥500-800 万"],
        ["A 轮", "M14-M16", "M18-M22", "¥4000 万", "¥2000-3000 万"],
        ["B 轮", "M30", "M30+（可选）", "¥8000 万", "¥5000 万"],
        ["3 年总融资", "-", "-", "¥1.3 亿", "¥7000 万"],
        ["", "", "", "", ""],
        ["关键洞察", "", "", "", ""],
        ["现金跑道（启动金）", "4 个月", "10 个月", "急迫", "从容"],
        ["创始团队稀释", "50-60%", "30-45%", "压力大", "压力小"],
        ["Pre-A 估值", "¥7000 万", "¥5000-8000 万", "差不多", "差不多"],
        ["A 轮估值", "¥3-5 亿", "¥1.5-2.5 亿", "高", "略低"],
        ["B 轮估值", "¥10-15 亿", "¥8-15 亿", "差不多", "差不多"],
    ]
    for r in funding:
        ws5.append(r)

    style_data(ws5, 4, ws5.max_row, 5)
    for col in range(1, 6):
        ws5.cell(row=8, column=col).fill = HIGHLIGHT_FILL
        ws5.cell(row=8, column=col).font = BOLD_FONT

    set_widths(ws5, [22, 18, 18, 16, 18])

    output = "docs/11-务实版财务测算/3年营收测算-务实版.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")


# ================ Excel 2: 100 家测算-务实版 ================
def create_100_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "0-务实版对比"

    ws["A1"] = "100 家财务影响 - 旧版 vs 务实版"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["指标", "旧版", "务实版", "差距", "说明"])
    style_header(ws, 3, 5)

    data = [
        ["M0 真实付费家数", 100, 100, "0", "保持"],
        ["M0 平均会员费", "¥6000", "¥4500", "-25%", "高低混合"],
        ["M0 年营收", "¥60 万", "¥45.5 万", "-24%", ""],
        ["", "", "", "", ""],
        ["A 类家数", 25, 20, "-20%", "重新分层"],
        ["B 类家数", 35, 30, "-14%", ""],
        ["C 类家数", 25, 30, "+20%", ""],
        ["D 类家数", 15, 20, "+33%", ""],
        ["", "", "", "", ""],
        ["单引擎12月年营收", "¥36 万", "¥24.7 万", "-31%", "续费率下调"],
        ["单引擎12月留存", 60, 47, "-22%", ""],
        ["", "", "", "", ""],
        ["双引擎12月年营收", "¥83 万", "¥42.9 万", "-48%", "更现实"],
        ["双引擎12月留存", 70, 61, "-13%", ""],
        ["", "", "", "", ""],
        ["改革 ROI", "+131%", "+74%", "-57pp", "仍显著正向"],
        ["", "", "", "", ""],
        ["改革投入", "¥250 万", "¥147 万", "-41%", "精益"],
        ["增量营收（含新用户）", "¥521 万", "¥468 万", "-10%", ""],
        ["综合 ROI", "30 倍", "3.2 倍", "更合理", ""],
    ]
    for r in data:
        ws.append(r)

    style_data(ws, 4, ws.max_row, 5)

    # 标记关键
    for row_idx in [13, 18, 21]:
        for col in range(1, 6):
            ws.cell(row=row_idx, column=col).fill = HIGHLIGHT_FILL
            ws.cell(row=row_idx, column=col).font = BOLD_FONT

    set_widths(ws, [22, 16, 16, 12, 24])

    # Sheet 2: 务实版分层
    ws2 = wb.create_sheet("1-务实版分层")
    ws2["A1"] = "100 家务实版分层结构"
    ws2["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws2.merge_cells("A1:G1")
    ws2.append([])

    ws2.append(["分层", "家数", "月活", "月发库存", "平均会员费", "单引擎续费率", "双引擎续费率"])
    style_header(ws2, 3, 7)

    layers = [
        ["A 核心活跃", 20, "≥10 次", "≥20 条", "¥7000", "80%", "90%"],
        ["B 稳定活跃", 30, "5-9 次", "5-19 条", "¥5000", "60%", "75%"],
        ["C 低频", 30, "1-4 次", "<5 条", "¥3500", "40%", "55%"],
        ["D 休眠", 20, "0 次", "0 条", "¥3000", "5%", "20%"],
        ["合计", 100, "-", "-", "-", "-", "-"],
    ]
    for r in layers:
        ws2.append(r)

    style_data(ws2, 4, ws2.max_row, 7)
    for cell in ws2[ws2.max_row]:
        cell.font = BOLD_FONT
        cell.fill = HIGHLIGHT_FILL

    set_widths(ws2, [14, 10, 10, 12, 14, 16, 16])

    # Sheet 3: 务实版双引擎详细
    ws3 = wb.create_sheet("2-双引擎详细")
    ws3["A1"] = "务实版双引擎 12 月营收（按分层）"
    ws3["A1"].font = Font(name="微软雅黑", size=14, bold=True, color="047857")
    ws3.merge_cells("A1:F1")
    ws3.append([])

    ws3.append(["分层", "留存家数", "会员费", "流量费", "增值+黑金", "年营收合计"])
    style_header(ws3, 3, 6)

    dual = [
        ["A", 18, 54000, 129600, 31684, 215284],
        ["B", 22.5, 67500, 56700, 16956, 141156],
        ["C", 16.5, 49500, 8910, 1973, 60383],
        ["D", 4, 12000, 288, 0, 12288],
        ["合计", 61, 183000, 195498, 50613, 429111],
    ]
    for r in dual:
        ws3.append(r)

    style_data(ws3, 4, ws3.max_row, 6)
    for cell in ws3[ws3.max_row]:
        cell.font = BOLD_FONT
        cell.fill = HIGHLIGHT_FILL

    set_widths(ws3, [10, 10, 14, 14, 16, 16])

    # Sheet 4: 成本
    ws4 = wb.create_sheet("3-改革成本")
    ws4["A1"] = "改革成本（务实版）"
    ws4["A1"].font = Font(name="微软雅黑", size=14, bold=True)
    ws4.merge_cells("A1:D1")
    ws4.append([])

    ws4.append(["类型", "项目", "金额", "vs 旧版"])
    style_header(ws4, 3, 4)

    costs = [
        ["一次性", "CEO 拜访行程", 40000, "-20%"],
        ["一次性", "客户成功培训", 20000, "-33%"],
        ["一次性", "老用户专属礼包", 60000, "-40%"],
        ["一次性", "UI 改版 + 开发", 500000, "-38%"],
        ["一次性", "AI 服务（前6月）", 18000, "-40%"],
        ["一次性", "反作弊系统", 30000, "-40%"],
        ["一次性合计", "", 668000, "-37%"],
        ["", "", "", ""],
        ["持续/月", "客户成功（3 人）", 30000, "-40%"],
        ["持续/月", "AI 服务", 6000, "-40%"],
        ["持续/月", "老用户群运营", 10000, "-50%"],
        ["持续/月", "反向邀请激励", 15000, "-50%"],
        ["持续/月", "客服 SLA", 6000, "-40%"],
        ["持续合计/月", "", 67000, "-44%"],
        ["持续合计/年", "", 804000, ""],
        ["", "", "", ""],
        ["12 月总投入", "", 1472000, "-41%（vs 旧版 ¥250 万）"],
    ]
    for r in costs:
        ws4.append(r)

    style_data(ws4, 4, ws4.max_row, 4)
    for row_idx in [10, 17, 20]:  # 合计行
        for col in range(1, 5):
            ws4.cell(row=row_idx, column=col).fill = HIGHLIGHT_FILL
            ws4.cell(row=row_idx, column=col).font = BOLD_FONT

    set_widths(ws4, [16, 26, 14, 24])

    output = "docs/11-务实版财务测算/100家测算-务实版.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")


def main():
    create_3year_excel()
    create_100_excel()
    print("✓ 2 个 Excel 文件已生成")


if __name__ == "__main__":
    main()
