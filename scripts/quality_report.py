# -*- coding: utf-8 -*-
"""
StarMap 质量仪表盘生成器

每天由 R7 姜文彬 运行，生成准确率报告并通报。
也用于每日集成时验证"演示就绪"。

用法：
  python scripts/quality_report.py --golden data/golden/ --output reports/
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def compute_f1(precision, recall):
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def evaluate_jd_extraction(golden_file, system_file):
    """评估 JD 解析准确率（按字段加权）。"""
    # TODO(R7 W3-W4): 实现完整的评估逻辑
    # 字段权重：job_title 0.15 / required_skills 0.30 / bonus_skills 0.20
    #          experience 0.15 / education 0.20
    return {
        "metric": "JD解析准确率",
        "target": ">=90%",
        "current": None,
        "status": "pending",
        "detail": "待 R7 实现 evaluate.py 后接入"
    }


def evaluate_resume_extraction(golden_file, system_file):
    """评估简历提取准确率（技能集 F1）。"""
    return {
        "metric": "简历提取准确率",
        "target": ">=90%",
        "current": None,
        "status": "pending",
        "detail": "待 R7 实现"
    }


def evaluate_matching(golden_file, system_file):
    """评估人岗匹配准确率（阈值二元判定）。"""
    return {
        "metric": "人岗匹配准确率",
        "target": ">=90%",
        "current": None,
        "status": "pending",
        "detail": "待 R7 实现"
    }


def check_warning_level(results):
    """根据准确率返回预警级别（D8 决策）。"""
    # TODO: 当准确率有值时检查
    # <85% 黄色 / <80% 橙色 / <75% 红色
    return "green"  # 当前无数据，默认绿色


def main():
    parser = argparse.ArgumentParser(description="StarMap 质量报告生成")
    parser.add_argument("--golden", default="data/golden/", help="Golden Set 目录")
    parser.add_argument("--system", default="data/output/", help="系统输出目录")
    parser.add_argument("--output", default="reports/", help="报告输出目录")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = {
        "generated_at": datetime.now().isoformat(),
        "golden_dir": args.golden,
        "system_dir": args.system,
        "metrics": [
            evaluate_jd_extraction(
                Path(args.golden) / "jd_golden.jsonl",
                Path(args.system) / "jd_output.jsonl"
            ),
            evaluate_resume_extraction(
                Path(args.golden) / "resume_golden.jsonl",
                Path(args.system) / "resume_output.jsonl"
            ),
            evaluate_matching(
                Path(args.golden) / "match_golden.jsonl",
                Path(args.system) / "match_output.jsonl"
            ),
        ],
        "warning_level": check_warning_level([]),
    }

    # JSON 报告
    json_path = output_dir / "quality_report.json"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Markdown 报告
    md_lines = [
        f"# StarMap 质量报告",
        f"",
        f"生成时间：{report['generated_at']}",
        f"",
        f"| 指标 | 目标 | 当前 | 状态 |",
        f"|------|------|------|------|",
    ]
    for m in report["metrics"]:
        current = m["current"] if m["current"] is not None else "-"
        status_icon = {"pending": "⬜", "pass": "✅", "fail": "❌"}.get(m["status"], "⬜")
        md_lines.append(f"| {m['metric']} | {m['target']} | {current} | {status_icon} |")

    md_lines.append(f"")
    md_lines.append(f"**预警级别**：{report['warning_level']}")
    md_path = output_dir / "quality_report.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    print(f"质量报告已生成：")
    print(f"  JSON: {json_path}")
    print(f"  Markdown: {md_path}")
    print()
    for line in md_lines:
        print(line)


if __name__ == "__main__":
    main()
