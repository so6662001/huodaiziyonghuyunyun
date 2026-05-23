"""
生成「100 家商家财务影响测算」Excel。

输出：docs/10-执行落地工具/财务影响测算/100家财务影响测算.xlsx

包含 6 个 Sheet：
1. 现状基线
2. 单引擎预测（无改革）
3. 双引擎预测（改革后）
4. 成本投入
5. 敏感性分析
6. 含新用户全景
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, Reference, LineChart


THIN = Side(border_style="thin", color="CCCCCC")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

HEADER_FILL = PatternFill("solid", fgColor="1F4E78")
HEADER_FONT = Font(name="微软雅黑", size=11, bold=True, color="FFFFFF")
TOTAL_FILL = PatternFill("solid", fgColor="FFF2CC")
HIGHLIGHT_FILL = PatternFill("solid", fgColor="D1FAE5")
DANGER_FILL = PatternFill("solid", fgColor="FEE2E2")
WARNING_FILL = PatternFill("solid", fgColor="FEF3C7")
NORMAL_FONT = Font(name="微软雅黑", size=10)
BOLD_FONT = Font(name="微软雅黑", size=10, bold=True)
WRAP = Alignment(wrap_text=True, vertical="center", horizontal="center")


def style_header(ws, row, n_cols=None):
    if n_cols is None:
        for cell in ws[row]:
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = WRAP
            cell.border = BORDER
    else:
        for col in range(1, n_cols + 1):
            cell = ws.cell(row=row, column=col)
            cell.fill = HEADER_FILL
            cell.font = HEADER_FONT
            cell.alignment = WRAP
            cell.border = BORDER


def style_data(ws, start_row, end_row, end_col):
    for row in ws.iter_rows(min_row=start_row, max_row=end_row, min_col=1, max_col=end_col):
        for cell in row:
            if cell.font.bold:
                continue
            cell.font = NORMAL_FONT
            cell.alignment = WRAP
            cell.border = BORDER


def set_column_widths(ws, widths):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


# ============= Sheet 1: 现状基线 =============
def create_baseline_sheet(wb):
    ws = wb.active
    ws.title = "1-现状基线"

    ws["A1"] = "M0 现状（改革前）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:F1")
    ws.append([])

    ws.append(["分层", "家数", "月活", "月发库存", "年会员费(每家)", "年付费(合计)"])
    style_header(ws, 3)

    data = [
        ["A 核心活跃", 25, "≥10 次", "≥20 条", 6000, 150000],
        ["B 稳定活跃", 35, "5-9 次", "5-19 条", 6000, 210000],
        ["C 低频", 25, "1-4 次", "<5 条", 6000, 150000],
        ["D 休眠", 15, "0 次", "0 条", 6000, 90000],
    ]
    for row in data:
        ws.append(row)

    ws.append(["合计", 100, "-", "-", "-", 600000])
    style_data(ws, 4, ws.max_row, 6)

    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = TOTAL_FILL

    ws.append([])
    ws.append(["核心结论", "M0 年营收 ¥60 万", "月均 ¥5 万", "纯会员费", "", ""])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT

    set_column_widths(ws, [14, 10, 12, 12, 16, 18])


# ============= Sheet 2: 单引擎预测 =============
def create_single_engine_sheet(wb):
    ws = wb.create_sheet("2-单引擎(无改革)")

    ws["A1"] = "单引擎预测（不做改革，自然衰减）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="C53030")
    ws.merge_cells("A1:E1")
    ws.append([])

    ws.append(["分层", "初始家数", "续费率", "12 月留存", "年营收"])
    style_header(ws, 3)

    data = [
        ["A", 25, 0.85, 21.25, 21.25 * 6000],
        ["B", 35, 0.70, 24.50, 24.50 * 6000],
        ["C", 25, 0.50, 12.50, 12.50 * 6000],
        ["D", 15, 0.10, 1.50, 1.50 * 6000],
    ]
    for row in data:
        ws.append(row)

    total_keep = sum(r[3] for r in data)
    total_rev = sum(r[4] for r in data)
    ws.append(["合计", 100, "-", total_keep, total_rev])
    style_data(ws, 4, ws.max_row, 5)

    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = DANGER_FILL

    ws.append([])
    ws.append(["结论", "12 月后留存 60 家", f"营收 ¥{int(total_rev):,}", "vs M0 降幅 -40%", "进入衰退期"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT

    set_column_widths(ws, [14, 14, 12, 14, 18])


# ============= Sheet 3: 双引擎预测 =============
def create_dual_engine_sheet(wb):
    ws = wb.create_sheet("3-双引擎(改革后)")

    ws["A1"] = "双引擎预测（改革后 12 个月）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="047857")
    ws.merge_cells("A1:H1")
    ws.append([])

    ws.append(["分层", "初始家数", "续费率", "12 月留存", "会员费", "流量费", "增值服务", "黑金升级", "年营收合计"])
    style_header(ws, 3, n_cols=9)

    # A 类
    a_keep = 25 * 0.95  # 23.75
    a_member = a_keep * 3000
    a_traffic = a_keep * 0.80 * 18000
    a_value = a_keep * 0.60 * 2388
    a_gold = a_keep * 0.50 * 3800
    a_total = a_member + a_traffic + a_value + a_gold

    # B
    b_keep = 35 * 0.80  # 28
    b_member = b_keep * 3000
    b_traffic = b_keep * 0.50 * 9600
    b_value = b_keep * 0.30 * 2388
    b_gold = b_keep * 0.20 * 3800
    b_total = b_member + b_traffic + b_value + b_gold

    # C
    c_keep = 25 * 0.60  # 15
    c_member = c_keep * 3000
    c_traffic = c_keep * 0.25 * 4800
    c_value = c_keep * 0.10 * 2388
    c_gold = c_keep * 0.05 * 3800
    c_total = c_member + c_traffic + c_value + c_gold

    # D
    d_keep = 15 * 0.25  # 3.75
    d_member = d_keep * 3000
    d_traffic = d_keep * 0.05 * 2400
    d_value = 0
    d_gold = 0
    d_total = d_member + d_traffic + d_value + d_gold

    rows = [
        ["A", 25, 0.95, a_keep, a_member, a_traffic, a_value, a_gold, a_total],
        ["B", 35, 0.80, b_keep, b_member, b_traffic, b_value, b_gold, b_total],
        ["C", 25, 0.60, c_keep, c_member, c_traffic, c_value, c_gold, c_total],
        ["D", 15, 0.25, d_keep, d_member, d_traffic, d_value, d_gold, d_total],
    ]
    for r in rows:
        ws.append(r)

    total_keep = sum(r[3] for r in rows)
    total_rev = sum(r[8] for r in rows)
    ws.append(["合计", 100, "-", total_keep,
              sum(r[4] for r in rows),
              sum(r[5] for r in rows),
              sum(r[6] for r in rows),
              sum(r[7] for r in rows),
              total_rev])

    style_data(ws, 4, ws.max_row, 9)

    for cell in ws[ws.max_row]:
        cell.font = BOLD_FONT
        cell.fill = HIGHLIGHT_FILL

    ws.append([])
    ws.append(["结论", f"12 月后留存 {total_keep} 家", f"营收 ¥{int(total_rev):,}",
              "vs 单引擎 +131%", "vs M0 +39%", "新引擎贡献 75%", "", "", ""])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT

    set_column_widths(ws, [10, 12, 10, 12, 14, 14, 14, 14, 18])

    # 添加对比柱状图
    chart = BarChart()
    chart.title = "各分层年营收构成"
    chart.y_axis.title = "金额（元）"
    chart.x_axis.title = "分层"
    data_ref = Reference(ws, min_col=5, min_row=3, max_col=8, max_row=7)
    cats = Reference(ws, min_col=1, min_row=4, max_row=7)
    chart.add_data(data_ref, titles_from_data=True)
    chart.set_categories(cats)
    chart.type = "col"
    chart.style = 12
    chart.width = 18
    chart.height = 10
    ws.add_chart(chart, "K3")


# ============= Sheet 4: 成本投入 =============
def create_cost_sheet(wb):
    ws = wb.create_sheet("4-成本投入")

    ws["A1"] = "12 个月总投入（双引擎过渡期）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:D1")
    ws.append([])

    # 一次性投入
    ws.append(["类型", "项目", "金额（元）", "说明"])
    style_header(ws, 3)

    onetime = [
        ["一次性", "CEO 拜访行程", 50000, "4-5 天 + 礼品"],
        ["一次性", "客户成功培训", 30000, "5 人 + 培训师"],
        ["一次性", "老用户专属礼包", 100000, "50 条线索 × 100 家 × ¥20"],
        ["一次性", "UI 改版 + 开发", 800000, "双引擎模块全部开发"],
        ["一次性", "AI 服务(前6月)", 30000, "OCR + LLM 试用"],
        ["一次性", "反作弊系统", 50000, "36 条规则上线"],
    ]
    for row in onetime:
        ws.append(row)

    onetime_total = sum(r[2] for r in onetime)
    ws.append(["一次性合计", "", onetime_total, ""])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.cell(row=ws.max_row, column=3).font = BOLD_FONT
    for col in range(1, 5):
        ws.cell(row=ws.max_row, column=col).fill = WARNING_FILL

    ws.append([])

    # 持续投入
    ws.append(["持续", "客户成功（5 人）", 600000, "月 ¥5 万 × 12"])
    ws.append(["持续", "AI 服务（成熟）", 120000, "月 ¥1 万 × 12"])
    ws.append(["持续", "老用户群运营", 240000, "月 ¥2 万 × 12"])
    ws.append(["持续", "反向邀请激励", 360000, "月 ¥3 万 × 12"])
    ws.append(["持续", "客服 SLA 升级", 120000, "月 ¥1 万 × 12"])

    persistent_total = 1440000
    ws.append(["持续合计", "", persistent_total, ""])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.cell(row=ws.max_row, column=3).font = BOLD_FONT
    for col in range(1, 5):
        ws.cell(row=ws.max_row, column=col).fill = WARNING_FILL

    ws.append([])
    ws.append(["12 月总投入", "", onetime_total + persistent_total, "¥250 万"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.cell(row=ws.max_row, column=3).font = BOLD_FONT
    for col in range(1, 5):
        ws.cell(row=ws.max_row, column=col).fill = DANGER_FILL

    style_data(ws, 4, ws.max_row, 4)
    set_column_widths(ws, [12, 26, 16, 26])


# ============= Sheet 5: 敏感性分析 =============
def create_sensitivity_sheet(wb):
    ws = wb.create_sheet("5-敏感性分析")

    ws["A1"] = "三大关键变量敏感性"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:D1")
    ws.append([])

    # 变量 1
    ws.append(["敏感性 1：A 类流量费付费转化率"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["付费率", "年营收（万）", "影响", "情景"])
    style_header(ws, ws.max_row, n_cols=4)
    ws.append(["50%", 72.0, "-14%", "保守"])
    ws.append(["65%", 78.0, "-6%", "略保守"])
    ws.append(["80%（基准）", 83.3, "基准", "常规"])
    ws.append(["90%", 87.5, "+5%", "乐观"])

    ws.append([])
    ws.append(["敏感性 2：流量费单价"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["卖家月均消费", "年营收（万）", "影响", "情景"])
    style_header(ws, ws.max_row, n_cols=4)
    ws.append(["¥800", 63.0, "-24%", "市场弱"])
    ws.append(["¥1200", 74.0, "-11%", "中等"])
    ws.append(["¥1500（基准）", 83.3, "基准", "常规"])
    ws.append(["¥2000", 98.0, "+18%", "市场强"])

    ws.append([])
    ws.append(["敏感性 3：A 类续费率"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["A 续费率", "留存", "年营收（万）", "影响"])
    style_header(ws, ws.max_row, n_cols=4)
    ws.append(["85%（不改革）", 21.25, 74.4, "-11%"])
    ws.append(["90%（改革打折扣）", 22.50, 78.9, "-5%"])
    ws.append(["95%（基准）", 23.75, 83.3, "基准"])

    ws.append([])
    ws.append(["3 大情景对比"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["情景", "年营收（万）", "变化", "对策"])
    style_header(ws, ws.max_row, n_cols=4)
    ws.append(["基准", 83.3, "0%", "按计划推进"])
    ws.append(["悲观（执行不到位）", 68.7, "-18%", "加强培训 + 客户成功"])
    ws.append(["极端（反弹 + 抵制）", 35.0, "-58%", "立即回滚 + 委员会"])

    style_data(ws, 4, ws.max_row, 4)
    set_column_widths(ws, [22, 18, 14, 22])


# ============= Sheet 6: 含新用户全景 =============
def create_full_view_sheet(wb):
    ws = wb.create_sheet("6-含新用户全景")

    ws["A1"] = "12 个月全景预测（含新用户增长）"
    ws["A1"].font = Font(name="微软雅黑", size=16, bold=True, color="1F4E78")
    ws.merge_cells("A1:F1")
    ws.append([])

    ws.append(["月份", "老 100 家月营收", "新增卖家累计", "新用户月营收", "总月营收", "累计营收"])
    style_header(ws, 3)

    # 数据来自 06-1 测算
    cumulative = 0
    data = [
        ("M1", 50000, 50, 17500, 67500),
        ("M3", 60000, 300, 27000, 87000),
        ("M6", 65000, 1500, 62000, 127000),
        ("M9", 67000, 3000, 149000, 216000),
        ("M12", 69440, 5000, 280000, 349440),
    ]
    rows = []
    for month, old, new_cnt, new_rev, total in data:
        cumulative += total
        rows.append([month, old, new_cnt, new_rev, total, cumulative])
        ws.append([month, old, new_cnt, new_rev, total, cumulative])

    style_data(ws, 4, ws.max_row, 6)

    ws.append([])
    ws.append(["核心数字"])
    ws.cell(row=ws.max_row, column=1).font = BOLD_FONT
    ws.append(["指标", "数值", "", "", "", ""])
    ws.append(["M12 月总营收", "¥34.9 万", "其中老 100 家贡献", "¥7 万（20%）", "新用户贡献", "¥28 万（80%）"])
    ws.append(["12 月累计", "¥246 万", "vs 单引擎累计 ¥150 万", "+64%", "", ""])
    ws.append(["增量 ROI", "12 月 +¥96 万 / 投入 ¥250 万", "= 38%", "", "", ""])

    set_column_widths(ws, [10, 18, 16, 18, 16, 18])


# ============= main =============
def main():
    wb = Workbook()
    create_baseline_sheet(wb)
    create_single_engine_sheet(wb)
    create_dual_engine_sheet(wb)
    create_cost_sheet(wb)
    create_sensitivity_sheet(wb)
    create_full_view_sheet(wb)

    output = "docs/10-执行落地工具/财务影响测算/100家财务影响测算.xlsx"
    wb.save(output)
    print(f"✓ 已生成 {output}")
    print(f"✓ Sheets: 6 个")


if __name__ == "__main__":
    main()
