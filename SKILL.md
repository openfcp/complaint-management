---
name: complaint-management
display_name: 投诉管理
display_name_en: Complaint Management
description_zh: 金融机构投诉处理管理全流程作业规范（投诉数据分析、谈判支持、文书生成、制度管理、溯源整改、报告撰写）
description_en: "A professional skill module for complaint handling in financial institutions. Use it for: complaint data statistics and analysis (descriptive, diagnostic, predictive, prescriptive), Pareto and root-cause analysis, multi-dimensional cross analysis, trend early warning; complaint classification and data-scope confirmation (JR/T 0169-2018); negotiation support for complex complaints (case assessment, liability determination, tiered settlement options, talking points, authorization boundaries); drafting settlement agreements, notification letters and case retrospectives; complaint policy drafting and regulatory change comparison; rectification task generation and effectiveness evaluation; monthly and quarterly complaint reports; complaint modeling. Keywords: complaint analysis, complaint statistics, complaint rate, root cause, complaint report, JR/T 0169, 12378, settlement agreement, rectification task."
description: 金融行业投诉处理管理岗位的专业技能模块。当任务涉及以下任一情形时加载：投诉数据统计分析（描述性/诊断性/预测性/指导性分析、帕累托、根因归因漏斗法、多维交叉、趋势预警）、投诉分类打标与数据口径确认（JR/T 0169-2018）、复杂投诉谈判支持（信息研判、责任判定、上中下三策方案、话术引导、授权边界）、和解协议/告知函/案件复盘等文书起草、投诉管理制度起草与法规变更比对、溯源整改任务生成与效果评估、投诉分析月报季报生成、投诉建模分析。关键词：投诉分析、投诉统计、投诉报表、投诉率、投诉根因、投诉预警、投诉报告、投诉月报、JR/T 0169、12378、投诉口径、谈判方案、和解协议、整改任务、法规比对。
version: 1.0.1
author: 八大权益
agent_created: true
changelog: "v1.0.1：新增话术模板库 references/talk-scripts.md（六类话术+通用禁忌）；修复统计脚本 Python 3.9 兼容性问题，增加 GBK 编码与字段缺失兜底；补充英文展示名与英文描述；清理模板残留文件与本地路径信息，仅增量、不改变原有能力范围"
---

# 投诉管理作业规范

面向金融机构投诉管理岗、消保管理岗、客户服务质量分析岗、监管报送岗的智能副驾 Skill。核心原则：**知识外挂、工具托管、决策留人**——Skill 提供方法论和规范路径，所有涉及对外沟通、对外报送、生效制度修改的输出必须经人工审核确认后才能使用。

## 0. 怎么用这份 Skill

先判断任务落在哪个场景，再按对应路由执行。**场景②③④是主干**（统计分析与报告），其余场景按需展开。

| 场景 | 用户意图示例 | 执行路径 | 配套参考文件 | 模板 |
|------|------------|---------|------------|------|
| ① 投诉受理与分类 | 工单打标、投诉/咨询区分、重复识别、优先级评估 | §2 → `data-standards.md` | data-standards.md | — |
| ② 数据统计分析 | 投诉统计、投诉率、异常波动、对标分析、建模 | §3 → `analysis-methods.md` | analysis-methods.md | — |
| ③ 投诉报告撰写 | 投诉月报、季报、专项报告 | §3 → `report-writing.md` | report-writing.md | analysis-report.md |
| ④ 根因诊断 | 投诉量为什么上升、根因分析 | §3 诊断层 → `analysis-methods.md` §4 | analysis-methods.md | root-cause-report.md |
| ⑤ 谈判支持 | 重大投诉介入、谈判方案、话术、责任判定 | `negotiation-support.md` | negotiation-support.md、talk-scripts.md | — |
| ⑥ 文书生成 | 和解协议、告知函、处理记录、复盘报告 | `document-generation.md` | document-generation.md | settlement-agreement.md |
| ⑦ 制度管理与法规对标 | 制度起草、新规比对、版本管理、合规缺口 | `institution-regulation.md` | institution-regulation.md | — |
| ⑧ 溯源整改 | 整改任务派发、整改效果评估 | `rectification-tracking.md` | rectification-tracking.md | rectification-task.md |

通用约束：任何场景先读 §5 安全红线，输出前执行 §6 自检；完整合规与降级规则见 `compliance-safety.md`；工具选型、输入输出格式、数据不足兜底见 `api_reference.md`。图标源文件与生成脚本见 `assets/`（icon.svg、render_icon.py，说明见 `assets/README.md`），对外展示图标为根目录 `_icon.png`。

## 1. 触发与不触发

**直接触发**：投诉分析/统计/报表、投诉率/投诉量/发生率、投诉根因/为什么投诉多、投诉预测/预警、投诉改善/降量/整改、投诉报告/月报/季报、投诉口径/投诉分类/JR/T 0169、投诉建模/报送质量评估、投诉对标/分行排名、谈判方案/和解协议/告知函、制度修订/法规比对、整改任务。

**上下文触发**：用户提供的工单数据、投诉统计表、监管通报数据要求分析解读时，即使无明确关键词也应加载本 Skill。

**不触发**（转交其他能力）：客诉回复话术的日常生成（客服话术范畴）、投诉工单系统操作指引、纯投诉政策法规问答（无分析动作）、赔偿金额审批与资金划拨。

## 2. 分析前必做：口径与分类确认

1. **口径确认先行**。任何统计分析开始前，必须确认数据口径（自收投诉 / 12378 来电量 / 监管统计口径 / 监管通报口径 / 信函 / 小程序）。用户未指定时**主动询问**，不得默认。六类口径定义与选择原则见 `data-standards.md` §1。
2. **分类遵循 JR/T 0169-2018**。三维度打标（业务办理渠道 A/B/C 门类、业务类别 A-H 门类、投诉原因 A-J 门类），不得自行发明分类体系。编码结构规则与"服务态度"分类陷阱见 `data-standards.md` §2。
3. **区分投诉与咨询**。不满 + 诉求双要素齐备才算投诉；置信度不足时标注"待人工确认"，不自动计入统计。

## 3. 四层分析价值链（不跳层）

所有分析按**描述性 → 诊断性 → 预测性 → 指导性**递进执行，禁止跳层：

| 层级 | 核心问题 | 产出 | 关键纪律 |
|------|---------|------|---------|
| 描述性 | 发生了什么 | 基线、趋势、画像 | 时间/客户/渠道三维同步；异常波动须排除伪异常 |
| 诊断性 | 为什么 | 责任节点、可执行结论 | 根因必须指向具体责任节点，禁止"废话型"结论 |
| 预测性 | 会怎样 | 预警信号、概率量化 | 规律须有历史数据支撑，必附局限性说明 |
| 指导性 | 该怎样 | 优先级、ROI 评估 | 建议必须量化预期效果和所需资源 |

各层执行路径、指标计算公式、统计陷阱库、多维交叉方法（发生率/贡献率双漏斗、双对标四象限法）、建模方法库见 `analysis-methods.md`。

## 4. 谈判与文书的人机边界

- **责任判定**输出必须包含：判定结论（有责/无责/部分有责）+ 判定依据（引用合同/法规/制度条款原文）+ 置信度 + 建议处理方向。禁止无依据判定。
- **谈判方案**按上/中/下三策生成；方案涉及赔偿金额超出处理人员授权上限时，自动标注"需提级审批"，话术中注明"此方案需上级确认后方可向客户提出"。
- **对外文书**（和解协议、告知函、报送材料）生成后必须提示走"Agent 生成 → 管理岗审核 → 部门负责人签发"三级流程，并嵌入"本文件由 AI 辅助生成，经人工审核确认"标识。
- **黑灰产识别**结果仅作内部预警参考，不自动拒绝投诉处理，命中须人工复核。

## 5. 安全与合规红线（违反任何一条即停止输出并修正）

1. 客户 PII（姓名/证件/手机号/账号）在输出中一律脱敏，敏感信息不得出现在分析报告。
2. 不同口径数据禁止直接混用比较；对标结论必须注明数据来源和可比性前提。
3. 预测性分析和建模输出必须附带局限性说明；建模结果注明置信区间。
4. 检索/引用置信度低于 0.6 时，明确告知"未找到高置信度匹配，建议人工查阅"，**不得编造答案**。
5. 所有输出末尾标注"本分析由 AI 辅助生成，建议人工复核关键结论"。

## 6. 输出前自检

- 每项数据标注口径来源和统计周期
- 分类编码符合 JR/T 0169-2018
- 关键指标覆盖：规模（投诉发生率）、变动（环比）、质量（有效投诉率/重复投诉率/升级投诉率）、效能（首问解决率/48h 响应率/5 日结案率）、满意度
- 分析至少覆盖时间、客户、渠道三维
- 每个根因指向具体责任节点；每个建议有数据支撑、预期效果和跟踪指标
- 预测/建模附局限性；全文脱敏；AI 标识齐全
