![Visitors](https://visitor-badge.laobi.icu/badge?page_id=skyline180.regex-generator)

# Architechture of final version

```
Input(s)
  ↓
Token analyzer
  ↓
Known pattern matcher (email/url/ip/uuid)
  ↓
Heuristic regex builder
  ↓
Multi-sample statistical inference
  ↓
LLM/AI refinement
  ↓
Regex optimizer
  ↓
Final regex
```
