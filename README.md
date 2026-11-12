# 投诉管理 Skill（Complaint Management）

> 金融机构投诉处理管理岗位的专业技能模块 · 作者：八大权益 · 版本：v1.0.1

## 简介

面向金融机构投诉管理岗、消保管理岗、客户服务质量分析岗、监管报送岗的智能副驾 Skill。核心原则：**知识外挂、工具托管、决策留人**——Skill 提供方法论和规范路径，所有涉及对外沟通、对外报送、生效制度修改的输出必须经人工审核确认后才能使用。

## 适用场景

| 场景 | 典型任务 |
|------|----------|
| 投诉受理与分类 | 工单打标、投诉/咨询区分、重复识别、优先级评估（遵循 JR/T 0169-2018） |
| 数据统计分析 | 投诉统计、投诉率、异常波动、对标分析、建模（描述性 → 诊断性 → 预测性 → 指导性四层价值链） |
| 投诉报告撰写 | 投诉月报、季报、专项报告 |
| 根因诊断 | 投诉量上升归因、根因归因漏斗法、多维交叉分析 |
| 谈判支持 | 重大投诉介入、谈判方案（上中下三策）、话术引导、责任判定 |
| 文书生成 | 和解协议、告知函、处理记录、案件复盘 |
| 制度管理与法规对标 | 制度起草、新规比对、版本管理、合规缺口分析 |
| 溯源整改 | 整改任务派发、整改效果评估 |

## 目录结构

```
├── SKILL.md                  # 技能主文件（场景路由与工作规范）
├── references/               # 各场景参考文件（分析方法、口径标准、谈判支持、文书生成等）
├── scripts/                  # complaint_stats.py 投诉统计脚本
├── templates/                # 分析报告、根因报告、和解协议、整改任务模板
└── assets/                   # 图标源文件与生成脚本
```

## 安装使用

将本目录复制到 WorkBuddy 用户级技能目录：

```
~/.workbuddy/skills/complaint-management/
```

重启会话后在对话中直接使用触发词即可，例如"帮我分析本月投诉数据""生成投诉季报""出一份谈判方案"。

## 关联技能（八大权益 · 金融消保系列）

- [消保审查](https://github.com/openfcp/consumer-protection-review)
- [消保检查](https://github.com/openfcp/consumer-protection-inspection)
- [消保评价](https://github.com/openfcp/consumer-protection-annual-evaluation)
- [合规销售](https://github.com/openfcp/compliance-sales)
- [金融消保专家](https://github.com/openfcp/consumer-protection-expert)

## 更新日志

- v1.0.1：新增话术模板库（六类话术+通用禁忌）；修复统计脚本 Python 3.9 兼容性问题；补充英文展示名与描述。
