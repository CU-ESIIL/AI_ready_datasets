# Reference assessment

Checked 20 November 2026 against primary sources. These papers motivate controls;
none establishes the proposed Fire VASE agent-versus-representation result.

| Reference | Verified scope | Use in this study / limit |
| --- | --- | --- |
| [Chen et al., 2026, arXiv:2605.28787v1](https://arxiv.org/html/2605.28787v1) | Agentic dataset retrieval through open-web versus structured dataset-search ecosystems | Measure actionable access as well as relevance. Different corpora/rankers mean this is not an isolated causal metadata-only experiment; hold our cohort and retrieval backend fixed |
| [Hu et al., SAGE, arXiv:2602.05975v1](https://arxiv.org/html/2602.05975v1) | Literature-search agents with sparse and learned retrievers | Include lexical/index/cache baselines. BM25 advantage is strongest on short-form questions; open-ended comparisons are closer and one dense retriever can slightly exceed BM25. Not a universal rejection of learned retrieval |
| [Liu, Ma & Zhong, 2025](https://doi.org/10.1038/s41467-025-60434-9) | LOO-map analysis of discontinuities and artifacts in neighbor embeddings such as t-SNE/UMAP | Check local reliability separately from broad organization. Does not establish that every learned representation or PCA is unreliable |
| [Ma et al., November 2026](https://www.microsoft.com/en-us/research/publication/earth-embeddings-in-environmental-remote-sensing-a-practitioners-perspective/) / [paper](https://arxiv.org/pdf/2611.13612) | Earth embedding review and four environmental remote-sensing case studies | Retain original-input and conventional-feature baselines; results vary by task. No direct evidence about fire-history agents or replacing scientific semantics |
| [Marsocci et al., PANGAEA, arXiv:2412.04204v2](https://arxiv.org/html/2412.04204v2) | Diverse geospatial foundation-model evaluation against supervised alternatives | Use label-budget, modality and geographic/time controls; does not test metadata × agent capability directly |

The SAGE author names on the paper are Tiansheng Hu, Yilun Zhao, Canyu Zhang,
Arman Cohan and Chen Zhao. Use those rather than the supplied ambiguous initials.
The verified PANGAEA preprint title is *PANGAEA: A Global and Inclusive Benchmark
for Geospatial Foundation Models*. The supplied journal DOI
`10.1109/MGRS.2025.3628194` could not be resolved by the browsing tool in this
inspection; retain it as user-supplied pending publisher-metadata verification,
rather than declaring it wrong or silently substituting another publication.

The original proposal is retained unchanged. Its substantive hypothesis remains
plausible and falsifiable, but claims about metadata causing improvements,
general-purpose embeddings or scientific transfer must remain scoped to evidence.
