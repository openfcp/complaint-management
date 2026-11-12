#!/usr/bin/env python3
"""投诉数据快速统计分析脚本（投诉管理 Skill 配套工具）。

用法:
    python3 complaint_stats.py <投诉数据.csv|xlsx> [--period-col 投诉时间] [--client-col 客户编号]

输入数据字段建议至少包含: 投诉时间, 投诉渠道, 投诉业务类别, 投诉原因,
客户类型, 处理状态, 处理时效（详见 references/api_reference.md 输入规范）。

输出:
    1. 关键指标（总量、环比、重复投诉率、按月趋势）
    2. 帕累托分析（按投诉原因的频次、占比、累计占比、核心根因集）
    3. 异常波动标记（月度投诉量超出历史均值 ±2σ）
    4. 交叉矩阵（业务类别 × 投诉原因）

依赖: pandas, openpyxl（读 xlsx 时需要）。所有结果仅供人工复核。
"""

from __future__ import annotations

import argparse
import sys

try:
    import pandas as pd
except ImportError:
    sys.exit("需要 pandas：pip install pandas openpyxl")


def load_data(path: str) -> "pd.DataFrame":
    if path.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(path)
    try:
        return pd.read_csv(path, encoding="utf-8-sig")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="gbk")  # 兼容 Excel 导出的 GBK 编码 CSV


def coerce_period(df: "pd.DataFrame", col: str) -> "pd.DataFrame":
    if col not in df.columns:
        print(f"⚠ 未找到时间字段「{col}」，跳过月度趋势与异常波动分析（可用 --period-col 指定）")
        return df
    df[col] = pd.to_datetime(df[col], errors="coerce")
    df["月份"] = df[col].dt.to_period("M").astype(str)
    return df


def key_metrics(df: "pd.DataFrame", client_col: str | None) -> None:
    total = len(df)
    print(f"\n== 关键指标 ==")
    print(f"投诉总量: {total}")
    if "处理状态" in df.columns:
        closed = (df["处理状态"].astype(str).str.contains("结案|完成")).sum()
        print(f"结案率: {closed / total:.1%}")
    if "处理时效" in df.columns:
        t = pd.to_numeric(df["处理时效"], errors="coerce").dropna()
        if len(t):
            print(f"平均处理时效: {t.mean():.1f}，P50={t.median():.1f}，P90={t.quantile(0.9):.1f}，P99={t.quantile(0.99):.1f}")
    if client_col and client_col in df.columns and total:
        print(f"去重客户数: {df[client_col].nunique()}（投诉发生率 = 投诉总量/有效客户数，请代入客户基数口径后计算）")


def monthly_trend(df: "pd.DataFrame") -> None:
    if "月份" not in df.columns:
        return
    m = df.groupby("月份").size().sort_index()
    print(f"\n== 月度趋势 ==")
    prev = None
    for k, v in m.items():
        huanbi = f"{(v - prev) / prev:+.1%}" if prev else "-"
        print(f"{k}: {v}  环比 {huanbi}")
        prev = v
    if len(m) >= 3:
        mean, std = m.mean(), m.std()
        anomalies = m[(m - mean).abs() > 2 * std]
        if len(anomalies):
            print(f"⚠ 异常波动（±2σ，均值={mean:.1f}）: {dict(anomalies)}")
            print("  注意：须交叉验证客户基数变化等伪异常因素后再归因。")


def pareto(df: "pd.DataFrame", col: str) -> None:
    if col not in df.columns:
        return
    cnt = df[col].value_counts()
    cum = cnt.cumsum() / cnt.sum()
    core = cnt[cum <= 0.8].index.tolist()
    print(f"\n== 帕累托分析（{col}）==")
    out = pd.DataFrame({"频次": cnt, "占比": cnt / cnt.sum(), "累计占比": cum})
    print(out.round(3).to_string())
    print(f"核心根因集（累计占比≤80%）: {core}")
    if col == "投诉原因":
        print("⚠ 提醒：'服务态度'类投诉须二次分类还原真实诉求后再下根因结论。")


def cross_matrix(df: "pd.DataFrame", rows: str, cols: str) -> None:
    if rows in df.columns and cols in df.columns:
        print(f"\n== 交叉矩阵（{rows} × {cols}）==")
        print(pd.crosstab(df[rows], df[cols]).to_string())


def main() -> None:
    ap = argparse.ArgumentParser(description="投诉数据快速统计分析")
    ap.add_argument("data", help="CSV 或 Excel 投诉数据文件路径")
    ap.add_argument("--period-col", default="投诉时间", help="时间字段名")
    ap.add_argument("--client-col", default="客户编号", help="客户标识字段名（可选）")
    ap.add_argument("--reason-col", default="投诉原因", help="投诉原因字段名")
    ap.add_argument("--biz-col", default="投诉业务类别", help="业务类别字段名")
    args = ap.parse_args()

    df = coerce_period(load_data(args.data), args.period_col)
    key_metrics(df, args.client_col)
    monthly_trend(df)
    pareto(df, args.reason_col)
    cross_matrix(df, args.biz_col, args.reason_col)
    print("\n* 本脚本输出由 AI 辅助生成，建议人工复核关键结论。")


if __name__ == "__main__":
    main()
