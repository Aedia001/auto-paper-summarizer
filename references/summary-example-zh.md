# From Local to Global: A Graph RAG Approach to Query-Focused Summarization（Arxiv 2024）

代码：
- https://github.com/neo4j/neo4j-graphrag-python
- https://github.com/gusye1234/nano-graphrag

作者提出 GraphRAG：先用 LLM 把大规模文本抽取成“实体-关系”图并做社区划分与分层摘要，再在回答“全局/主题型”问题时对社区摘要并行生成局部回答并汇总成全局答案，从而在约百万 token 级语料的 query-focused summarization 场景下，相比传统向量检索式 RAG 更“全面且多样”，并在合适粒度下显著降低推理 token 成本。

**研究动机**
- 传统向量检索式 RAG（semantic search + top-k chunk）适合“答案局部存在”的问题，但对“需要全局理解/主题归纳”的 sensemaking 问题天然不适配，本质更像 Query-Focused Summarization（QFS）。
- 现有 QFS 方法往往难以扩展到 RAG 常见的百万 token 级私有语料规模；而单纯扩大上下文窗口也会遭遇“lost in the middle”等长上下文退化。
- 需要一种既能扩展到大语料、又能支持全局主题综合的索引与生成范式。

**创新点**
- 把“知识图谱 + 社区发现（community detection）+ 分层摘要”作为 RAG 的索引结构：利用图的模块性把大语料切成语义社区，并预生成社区摘要，支持全局问答。
- Query-time 采用 map-reduce：对每个社区摘要并行生成“社区答案（partial answer）”，再在 reduce 阶段汇总为全局答案（global answer）。
- 提出面向“全局 sensemaking”问题的评测流程：先用一个 LLM 生成多样的全局问题，再用另一个 LLM 按预定义标准做相对比较，并在更新版本中补充 claim-based 指标。

**方法**
- 核心流程是 `Indexing -> Query`：先把文档切成 text chunks，再用 LLM 从 chunk 中抽取 entities、relationships、claims 等元素并生成摘要，形成图索引。
- 随后对图做社区发现（如 Leiden），得到多层级社区，并为每个社区离线生成社区摘要（community summaries）。
- 在线回答时，先对每个社区摘要做 QFS 生成社区答案（map），再把这些社区答案再做一次 QFS 汇总成全局答案（reduce）。
- 对照设置包括不同社区层级的 GraphRAG（C0-C3）、无图的全局 map-reduce 文本汇总（TS），以及向量检索式 RAG baseline（SS）。
- 一个关键工程观察是：更小的上下文窗口（例如 8k）在“全面性”上反而更优，因此作者最终固定用较小窗口进行评测。

**结果**
- 在两套真实语料（Podcast transcripts / News articles）上，作者构建了多层级图摘要体系；图规模大致达到 8,564 节点 / 20,691 边与 15,754 节点 / 19,520 边。
- 相比向量检索式 RAG（SS），所有“全局方法”（GraphRAG C0-C3 与 TS）在 Comprehensiveness 和 Diversity 上都显著更强。典型 win-rate 大致为：Podcast 上全面性约 72%–83%、多样性约 75%–82%；News 上全面性约 72%–80%、多样性约 62%–71%。
- GraphRAG 的社区摘要在多种设置下相对 TS 有小幅但一致的提升，同时保持更好的 token 效率。
- 在成本方面，低层社区摘要（C3）相比 TS 可减少约 26%–33% 的上下文 token；根层社区摘要（C0）可减少 97% 以上的上下文 token，虽然会牺牲部分性能，但仍整体优于向量检索式 RAG。
- 更新版本补充的 claim-based 评测中，作者用 Claimify 抽取并去重后得到约 47,075 条 unique claims，结论整体与 LLM-as-a-judge 的趋势一致：全局方法优于向量 RAG。

缺点
- 评测强依赖 LLM-as-a-judge 以及 LLM 生成问题，可能存在评判偏好和稳定性问题，缺少更充分的人工评测与真实用户任务验证。
- 语料和问题覆盖仍有限，主要集中在两类语料、约百万 token 规模以及特定的 sensemaking 问题；推广到更多领域、更大规模或更复杂任务仍需验证。
- 图索引构建本身成本较高、工程复杂度较强，抽取与总结依赖大量 LLM 调用，prompt 设计也会显著影响结果。
- “Empowerment”指标结果不稳定，说明图索引或摘要链路可能丢失引用、原话与细节，进而影响可用性与可溯源性。
