"""Authored site copy. Markdown strings are rendered at build time.
Everything here summarises the research doc; detail pages carry the sources."""

SITE_NAME = "Enterprise AI Handbook"
TAGLINE = "60 departments. 57 tools. One verified learning path."
DOC_URL = "https://claude.ai/artifact/PzB4eRd3Trt1TU4GsT6hrH"
REPO_URL = "https://github.com/kirannarayanak/ai-handbook-research"
AS_OF = "October 2026"

HOME = {
    "kicker": "Corporate AI Tools & Training, revised October 2026",
    "title": "Learn the AI your department actually uses.",
    "lead": "A department-by-department guide to enterprise AI: which tools fit which roles, what the data rules are, and how to train for it. Every claim is traced to a page a researcher opened.",
    "stats": [
        ("60", "departments mapped"),
        ("57", "tools profiled"),
        ("131", "more tools and functions found"),
        ("626", "sources opened and checked"),
    ],
    "paths": [
        {"title": "I'm new to AI at work", "desc": "Start with the foundations: one approved assistant, verification habits and the data rules that apply to everyone.", "href": "learn/foundations/", "icon": "spark"},
        {"title": "I lead a department", "desc": "Find your department, see the tools the handbook recommends, the real use cases and the capstone your team should build.", "href": "departments/", "icon": "org"},
        {"title": "I choose and govern tools", "desc": "Compare assistants side by side, read the data-handling notes, and use the matrix to rationalise overlapping licences.", "href": "compare/", "icon": "scale"},
        {"title": "I design the curriculum", "desc": "Use the tier bands, hour estimates, cross-cutting modules and the gap list to build a programme that holds up to audit.", "href": "learn/", "icon": "book"},
    ],
    "principles": [
        ("Foundation first", "Everyone learns one employer-approved general assistant, prompting, verification, privacy and human review before anything role-specific."),
        ("Role-based depth", "Each role picks two to four tools for practical exercises: a general assistant plus the specialist platform the role already runs."),
        ("Three tiers", "Core 6-10 hours, Advanced 12-20 hours, Specialist 20-40+ hours. Assessment is on real deliverables, safe data use and accuracy."),
        ("Validate before adopting", "Licensing, residency, integrations and even product names change monthly. Nothing here is a purchase mandate."),
    ],
}

LEARN_INTRO = {
    "title": "The learning path",
    "lead": "Six short chapters that take you from first principles to a department-specific plan. Read them in order, or jump to the one you need. Your progress is saved in this browser.",
}

CHAPTERS = [
    {
        "slug": "foundations",
        "title": "Foundations everyone needs",
        "minutes": 8,
        "summary": "One approved assistant, a verification habit, and the data rules that never change.",
        "body": """
## Start with one tool, not ten

The handbook's first rule is simple: every employee learns **one employer-approved general assistant** well before touching anything role-specific. In most organisations that is Microsoft Copilot, Gemini, Claude or ChatGPT Enterprise, whichever the company licenses. The research found that the six general assistants overlap heavily, and that most large firms end up running two of them. Learn the one you have.

## Treat every output as a draft

AI assistants are measured to be wrong often enough that checking is part of the job, not an optional extra:

- Paid legal-research tools were wrong over 17% of the time, and general chatbots 58-82% of the time, in Stanford's benchmark.
- Eight AI search engines gave incorrect answers to over 60% of news-citation queries in Columbia's test, and premium tiers were worse because they answered confidently instead of declining.

The habit that follows: **open the source before you repeat a citation**, and check any high-stakes number against the system of record.

## Know what may go in

Three tiers of tool, three different rules:

| Tier | Typical example | What may go in |
|---|---|---|
| Consumer or free | Personal ChatGPT, free Gemini API | Nothing confidential. Free tiers may use prompts to improve products. |
| Business | Claude Team, ChatGPT Business | Internal work, under the company policy. Check retention and audit limits. |
| Enterprise | Microsoft Copilot, Claude Enterprise, ChatGPT Enterprise | Approved for company data within the agreed residency and retention terms. |

Never paste secrets, personal data, material non-public information or regulated records into anything below the enterprise tier.

## Agents change the rules

Many handbook tools now act on systems rather than just answer: coding agents, SOC agents, Genie Code's auto-approve mode, MCP connectors. The UK National Cyber Security Centre's advice is blunt: language models cannot reliably separate instructions from data, so prompt injection may never be fully mitigated. Give agents least privilege, keep a human approval gate on sends, writes and payments, and log what they do.

## The five-line rule set

1. Use only approved, company-account AI tools.
2. Treat citations and quotes as unverified until you open the source.
3. Check high-stakes output against primary sources.
4. Do not let agents act on email, web or document content you do not trust.
5. Classify before you paste.
""",
        "next_links": [("Governance and regulation", "learn/governance/"), ("Browse the 57 tools", "tools/")],
    },
    {
        "slug": "tools",
        "title": "The tool landscape",
        "minutes": 10,
        "summary": "Ten families of tools, what each is for, and where the handbook's list is already out of date.",
        "body": """
## Ten families

The 57 handbook tools fall into ten groups. The first two are horizontal and appear in nearly every department; the rest are specialist platforms you only train on if your company runs them.

1. **General assistants and research tools**: Gemini, Claude, ChatGPT Enterprise, NotebookLM (now Gemini Notebook), Perplexity, Perplexity Enterprise.
2. **Microsoft Copilots and Power Platform**: one licence, several surfaces (Word, Excel, Teams, Power BI), plus Power Automate.
3. **Presentation, design and documents**: Gamma, Canva, Adobe Firefly and Acrobat, Figma and FigJam.
4. **Coding assistants**: Claude Code, GitHub Copilot, Cursor, Gemini Code Assist, Amazon Q Developer, Playwright.
5. **Enterprise business platforms**: ServiceNow, Salesforce, SAP Joule, Workday, Jira/Rovo, UiPath.
6. **Sales and marketing**: Gong, HubSpot, LinkedIn, Google Ads, Meta Advantage+.
7. **Customer service and experience**: Zendesk, Intercom Fin, Gainsight, Qualtrics.
8. **Legal, audit and GRC**: CoCounsel, Datasite, AuditBoard (now Optro).
9. **Security, cloud operations and observability**: Security Copilot, Charlotte AI, Gemini in Security, Purview, Azure Copilot, Datadog, Dynatrace.
10. **Data, analytics and AI platforms**: Databricks, Snowflake, Tableau Pulse, Google AI Studio, Microsoft Foundry, Amazon Bedrock, MLflow.

## Teach the platform you own

For groups 4 to 10 the pattern is identical: enterprises standardise on the AI of the platform they already run. A Falcon shop trains on Charlotte AI, a Datadog shop on Bits AI, an Azure shop on Azure Copilot. Collapsing the list this way cuts 57 training objects to roughly 35 without dropping a single department.

## Names move fast

At least fourteen handbook names were out of date by the time this research ran: NotebookLM became Gemini Notebook, Microsoft 365 Copilot became Microsoft Copilot, Azure AI Foundry became Microsoft Foundry, Databricks Assistant became Genie Code, AuditBoard became Optro, Intercom became Fin (and was bought by Salesforce), Dynatrace Davis AI became Dynatrace Intelligence. Two tools are on a sunset path: Gemini Code Assist (end of sale, replaced by Antigravity) and Amazon Q Developer (replaced by Kiro). The gaps chapter carries the full table.

## Pricing is now mostly metered

Seat prices still exist (Copilot and Gemini Enterprise at USD 30 per user per month; Claude Enterprise from about USD 60), but the specialist tools bill in credits, compute units or usage: Security Copilot SCUs, Datadog and Dynatrace credits, Snowflake AI Credits, Copilot Studio credits, Rovo usage billing from December 2026. Budget owners need the cost model in the training, not just the features.

## Confidence

Of the 57 profiles, 10 are high confidence, 39 medium and 8 low. The low ones are mostly vendors whose websites blocked the researchers (OpenAI, Canva, Adobe, Gainsight, Meta). Treat those cells as needing your own verification before launch.
""",
        "next_links": [("Open the tool catalogue", "tools/"), ("Compare tools side by side", "compare/")],
    },
    {
        "slug": "departments",
        "title": "Departments and their work",
        "minutes": 10,
        "summary": "Eight clusters, sixty departments, and the shape of a good capstone.",
        "body": """
## Eight clusters

The 60 departments group into eight clusters that share data, risks and tools: leadership and governance; HR and workplace; finance and investor relations; sales and marketing; customer and product; engineering and IT; security, data and AI; operations and transformation. Departments in the same cluster can share most of a training module and split only on the specialist tool.

## The same four moves everywhere

Across all 60 departments the AI use cases reduce to four moves: **summarise** (meetings, tickets, filings, incidents), **draft** (briefs, code, messages, policies), **classify or triage** (alerts, invoices, applications, deviations), and **analyse** (variance, forecasts, exceptions). What differs is the system of record the output must be checked against, and the regulation that applies to the data.

## What a capstone looks like

Every department page carries a capstone sized for its tier. They all follow the handbook's assignment template: one real deliverable, built with an approved assistant, with the prompts documented, a validation log showing every figure traced to its source, a list of the AI's mistakes caught in review, and a measured before-and-after time comparison. Assess the validation log, not the prompt.

## Where the evidence is strong and weak

Fifteen departments are high confidence, 44 medium and one low (Enterprise Applications & ERP, whose outcomes are all vendor-sourced). Most quantified benefits anywhere in the research are vendor claims or vendor-published case studies. Use them as hypotheses to test with your own KPIs, which each department page lists.

## Beyond the 60

Two research passes found 41 further functions large organisations commonly staff that the handbook omits: from corporate communications, pricing and government affairs to revenue cycle management, AML operations, localisation, FinOps and global mobility. If your organisation has them, the additional-departments page gives a starting tool list and the evidence for each.
""",
        "next_links": [("Open the department directory", "departments/"), ("See the matrix", "matrix/")],
    },
    {
        "slug": "governance",
        "title": "Governance, regulation and data",
        "minutes": 9,
        "summary": "What the law now requires of employers, and how residency and retention differ between assistants.",
        "body": """
## The EU rules that govern this programme

The EU AI Act's Article 4 AI-literacy duty has applied since 2 February 2025. The July 2026 Digital Omnibus softened its wording (providers and deployers must now "take measures supporting" staff literacy) but did not remove it. In practice: keep the attendance records, dates and content of this training. High-risk obligations for recruitment and employment systems moved to 2 December 2027, so HR teams using Workday AI or LinkedIn Recruiter AI need human-oversight training before then. Transparency duties (telling users they are talking to an AI) apply from 2 August 2026.

## US state law is arriving department by department

Illinois requires notice when AI is used in employment decisions (since 1 January 2026). Colorado's replacement act takes effect 1 January 2027 with pre-use notice and adverse-decision explanations. California's automated decision-making rules apply from 1 January 2027. Connecticut follows in October 2027. South Korea's AI Basic Act (January 2026) treats hiring as high-impact. Each maps to the HR cluster first and to customer-facing tools second.

## A single framework anchor

The NIST AI Risk Management Framework and its Generative AI Profile already appear in the security and AI department pages. Build one governance module on NIST, attach the EU and US obligations as an annex, and every department takes it once.

## Residency and retention are not the same across assistants

- **ChatGPT Enterprise**: data at rest in the UK, EU and eight other regions, but in-region inference only for the US or Europe; residency is fixed when the workspace is created.
- **Claude**: the first-party product has a US-only workspace geography; no EU or UK region.
- **Gemini Notebook**: outside the Workspace data-region settings.
- **Microsoft**: Security Copilot fixes its geography at onboarding; Foundry global deployments may route outside the home region.

All business and enterprise tiers opened in the research state that prompts are not used for training by default. Consumer and free tiers differ. Note that the ChatGPT figures are second-hand because OpenAI's own pages could not be opened.

## Shadow AI is the governance problem that matters

IBM found high shadow-AI use added USD 670,000 to the average breach cost, and 63% of organisations had no AI governance policy. Netskope found 47% of generative-AI users still used personal apps. The controls are unglamorous: an approved-tool list, managed accounts, DLP on sensitive data flows (Purview DSPM for AI covers Microsoft Copilots, ChatGPT Enterprise and Claude Enterprise), and approval gates on agents.
""",
        "next_links": [("Full cross-cutting themes", "themes/"), ("Security, data and AI departments", "departments/#security-data-and-ai")],
    },
    {
        "slug": "adoption",
        "title": "Adoption, measurement and accessibility",
        "minutes": 7,
        "summary": "What makes AI training stick, how to prove it, and who it helps most.",
        "body": """
## The one rigorous trial

The UK Department for Business and Trade ran a three-month Microsoft 365 Copilot trial of 1,000 licences, evaluated by diary studies, interviews, observed tasks and usage telemetry. Findings: 72% of diary respondents were satisfied; time was saved on drafting, summaries, transcription, search and brainstorming, and none on image generation, scheduling or slide creation. Benefit was role-specific (HR and commercial gained more than policy and legal), and uncertainty about acceptable use made people cautious.

## What the evidence supports

- Role-specific use cases beat generic prompting courses.
- Publish the acceptable-use policy before the rollout, not after.
- Champions and manager modelling matter (Prosci's finding, vendor-sourced).
- Measure at the task level, with a baseline.

## How to measure

Copy the DBT design: pair self-reported diaries (use case, minutes saved, accuracy, satisfaction) with usage telemetry from the vendor dashboards. Every department page lists five KPIs; together with the capstone's before-and-after comparison, they give you Kirkpatrick Level 3 and Level 4 evidence without a separate study.

## Accessibility is an outcome, not only a duty

The same DBT trial found Copilot helped neurodiverse staff, people with hearing or vision impairments and non-native English speakers, mostly through summarisation and meeting recap. Build training content to WCAG 2.2 AA regardless of whether the European Accessibility Act or ADA rules reach your internal platforms, and put an assistive-use unit in the Core tier.

## Hours by tier

Core 6-10 hours per tool, Advanced 12-20, Specialist 20-40. Because the foundation and governance modules cover classification, verification and agent safety once, per-tool hours should shrink to the tool-specific remainder. A department's total is the shared module (4-6 hours Core, 6-8 Advanced and Specialist) plus its three to five tool modules, less overlaps within one licence.
""",
        "next_links": [("Gaps and recommendations", "learn/gaps/"), ("Matrix and hours", "matrix/")],
    },
    {
        "slug": "gaps",
        "title": "Gaps, caveats and what to do next",
        "minutes": 6,
        "summary": "Where the research is thin, which names have changed, and the eight decisions that shape the matrix.",
        "body": """
## Where to be careful

- **Eight low-confidence tools**: ChatGPT Enterprise, Canva Magic Studio, Adobe Firefly, Adobe Acrobat AI Assistant, ServiceNow Now Assist, Meta Advantage+, Gainsight AI, Google AI Studio. Their vendor pages blocked the researchers; verify through help subdomains, trust-portal PDFs or DPAs before teaching them.
- **Vendor-reported outcomes everywhere**: 550% faster triage, 98% accuracy, 50% faster delivery. Hypotheses, not facts.
- **Dates**: the research ran on 24-25 October 2026 and found four renames in its final sixteen weeks. Re-check quarterly.

## Decisions for the matrix

1. Collapse the four Microsoft surfaces into one tool with four modules.
2. Train the platform the company owns in each specialist category rather than every entrant.
3. Use current names with the handbook name in brackets.
4. Merge the two Perplexity rows unless both are licensed.
5. Carry a confidence column into every cell.
6. Carry a data-tier and residency column for each horizontal tool.
7. Show hours as a range with the shared module subtracted.
8. Re-verify the low-confidence cells before launch.

## Decisions for the curriculum

Build one shared foundation module; assess the validation log, not the prompt; give agentic tools their own safety unit; keep EU Article 4 records; cover the embedded assistants the handbook omits where you run them (Veeva, Prosci Kaiya, Kinaxis, LeanIX, Copilot Studio and Agent 365); build to WCAG 2.2 AA; evaluate with telemetry plus diaries.

The full renames table, caveats and the 131 additional tools and functions are on the reference pages.
""",
        "next_links": [("Gaps and renames reference", "gaps/"), ("More tools the handbook omits", "tools/more/")],
    },
]

THEMES_MD = r"""
## Governance and AI regulation obligations for employers (as of October 2026)

The EU Digital Omnibus on AI was published in the Official Journal on 24 July 2026 and entered into force on 27 July 2026. It changed timelines and softened the literacy wording, but did not remove the duty that governs this training programme ([Lewis Silkin](https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo), [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/)).

| Obligation | Status and date | What it means for the matrix |
|---|---|---|
| EU AI Act Art. 4 AI literacy | Applied since 2 Feb 2025. After the Omnibus, providers and deployers must "take measures supporting" staff AI literacy rather than guarantee a "sufficient level". | Keep attendance records, dates and content of this programme. It applies to all 60 departments. Regulators' documentation expectations rest on law-firm commentary (the Commission AI literacy Q&A page returned 403). |
| EU Art. 26 and Annex III (employment) | High-risk duties for recruitment and employment moved from 2 Aug 2026 to 2 Dec 2027; Annex I products to 2 Aug 2028. Art. 26(2) keeps competence and training duties for high-risk deployers. | HR, Talent Acquisition and People Analytics (departments 11-17) and users of Workday AI or LinkedIn Recruiter AI need human-oversight training before Dec 2027. |
| EU Art. 50 transparency | Disclosure that a user is interacting with AI applies from 2 Aug 2026; machine-readable marking of AI output for older systems from 2 Dec 2026. | Marketing, Communications and Customer Support chatbots: disclosure and content marking. |
| Colorado SB 26-189 | Repealed and replaced the 2024 Act (signed 14 May 2026), effective 1 Jan 2027. Pre-use notice, adverse-decision explanation within 30 days, three-year records ([Covington](https://www.insideglobaltech.com/2026/08/18/admt-law-round-up-what-employers-need-to-know-about-recent-admt-laws/)). | HR screening and ADMT tools: notice and human-review procedures. |
| Illinois HB 3773 | In force 1 Jan 2026: notice when AI is used in employment decisions; ZIP-code proxies banned. | Hiring managers and recruiters. |
| California CPPA ADMT rules | Apply from 1 Jan 2027: pre-use notice, opt-out and risk assessment. | HR, performance management and workforce-reduction tools. |
| Connecticut SB 5 | Employment-AI provisions apply to tools deployed from 1 Oct 2027. | HR. |
| South Korea AI Basic Act | In force 22 Jan 2026; hiring is a high-impact use with explainability and advance-notice duties ([Cooley](https://www.cooley.com/news/insight/2026/2026-01-27-south-koreas-ai-basic-act-overview-and-key-takeaways)). | Korean HR and recruiting. |

Not verified in this research: NYC Local Law 144, the California Civil Rights Council FEHA rules, US federal preemption developments, and UK ICO and DSIT guidance.

**Framework anchor.** Departments 48 and 51 already cite the NIST AI Risk Management Framework and its Generative AI Profile (NIST AI 600-1, July 2024) ([NIST](https://www.nist.gov/itl/ai-risk-management-framework)). A single AI governance module built on NIST, with the EU and US obligations above as an annex, can serve every department.

## Data privacy, residency and the horizontal assistants

- **Training defaults.** All business tiers opened in this research state that customer prompts are not used to train models by default: ChatGPT Enterprise and Business ([SpotDev residency](https://www.spotdev.co.uk/blog/ai-data-residency-uk-chatgpt-claude-gemini-grok-muse), [SpotDev governance gap](https://www.spotdev.co.uk/blog/chatgpt-business-vs-enterprise-governance-gap), both second-hand because openai.com returned 403), Claude Team and Enterprise, Gemini for Workspace, and Microsoft Copilot. Consumer and free tiers differ: Google states the Gemini API free tier may use prompts to improve products ([Google Cloud migration guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/migrate/migrate-google-ai)).
- **Residency.** ChatGPT Enterprise offers data at rest in the UK, EU and eight other regions, but in-region inference only for the US or Europe; residency is set at workspace creation and cannot be added later. Claude's first-party product has a "us" workspace geo only. Gemini Notebook is excluded from Workspace data-region settings. Gemini in Google SecOps and Microsoft Foundry global deployments may route requests outside the home geography. Security Copilot fixes the Workspace geo at onboarding.
- **Retention and audit.** ChatGPT Enterprise retention is configurable only for "qualifying organisations"; Enterprise has SCIM, RBAC and a Compliance API, and Business lacks SCIM, audit logs, ISO coverage and residency (second-hand). Claude Enterprise has admin-set retention, SSO, SCIM and audit logs. Microsoft Copilot is auditable through Purview. Perplexity Enterprise and Gemini Notebook Enterprise retention and SSO were not covered by an opened source.
- **Certifications.** Claude lists ISO 42001 and a BAA; the OpenAI ISO 27001/27017/27018/27701 certificate covers Enterprise and Edu but not Business (second-hand). CrowdStrike, Salesforce and Workday also state ISO 42001.

**Implication for training.** The matrix should carry a per-tool "what may go in" line that distinguishes consumer, business and enterprise tiers.

## Licensing cost models, overlap and rationalisation

Published list prices in the opened sources ([IT Daily](https://en.it-daily.net/it-management-en/ai-en/ai-assistants-compared-2026), [EPC Group](https://www.epcgroup.net/microsoft-copilot-vs-gemini-vs-claude-enterprise-decision-framework-2026)): Microsoft Copilot USD 30 per user per month on top of E3/E5; Gemini Enterprise USD 30 per user per month on top of Workspace; Claude Enterprise custom, starting around USD 60 per user per month at minimum-seat commitments. ChatGPT Enterprise, Perplexity Enterprise and Gemini Notebook Enterprise list prices were not verified. The specialist tools add metered models: Security Copilot SCUs, Datadog and Dynatrace credits, Snowflake AI Credits at USD 2.00 or 2.20, Copilot Studio credits at USD 200 per 25,000, Agent 365 at USD 15 per user per month ([Rencore](https://rencore.com/en/blog/understanding-microsoft-agent-365-pricing)), Rovo usage billing from 3 Dec 2026, and Genie Code pay-as-you-go from 8 July 2026.

| Scenario (1,000 seats, list price, excluding base licences and metered usage) | Annual licence |
|---|---|
| A: one assistant, Microsoft Copilot for all | USD 360,000 |
| B: Copilot for all, plus 200 Claude Enterprise seats at about USD 60 and 50 Gemini Enterprise seats at USD 30 | USD 522,000 |

**Overlap.** The handbook lists six general assistants, four Microsoft surfaces of one licence, four coding IDEs plus Amazon Q Developer, two observability agents, three SOC agents, and two Perplexity entries. Gartner's May 2026 advice, as reported, is to match assistants to use case and worker type by capability, cost and trust; Forrester sees 2026 as a consolidation year with 25% of planned AI spend deferred to 2027.

**Lock-in and exit.** No opened source covered conversation export, custom GPT or Project portability, MCP connector portability, contract terms or price-protection clauses. Two forced migrations illustrate the risk: Gemini Code Assist's end of sale on 9 Oct 2026 (users sent to Antigravity) and Amazon Q Developer's retirement in favour of Kiro by 30 Apr 2027.

**Recommendation.** Treat the four Microsoft surfaces as one tool with four modules, teach one general assistant per learner (two at most), teach the coding tool the team actually licenses, and teach the SOC and observability agent bound to the platform the company owns. That cuts the 57-tool matrix to roughly 35 distinct training objects.

## Hallucination, verification, prompt injection and shadow AI

**Hallucination is measured, not hypothetical.** Stanford RegLab/HAI found paid legal-research tools wrong over 17% of the time (Lexis+ AI, Ask Practical Law AI) and over 34% (Westlaw AI-Assisted Research), with general chatbots at 58-82% on legal queries ([Stanford HAI](https://hai.stanford.edu/news/ai-trial-legal-models-hallucinate-1-out-6-or-more-benchmarking-queries)). The Columbia Tow Center found eight AI search tools wrong on over 60% of news-citation queries (Perplexity 37%, Grok 3 94%), with premium tiers worse because they answered confidently instead of declining ([CJR](https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php)).

**Prompt injection is structural.** OWASP LLM01:2025 states injected instructions can be imperceptible to humans and that RAG and fine-tuning do not fully mitigate them ([OWASP](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)). EchoLeak (CVE-2025-32711) showed one crafted email causing zero-click data exfiltration from Microsoft 365 Copilot ([arXiv](https://arxiv.org/html/2509.10540v1)). The UK NCSC says LLMs do not separate instructions from data, so injection may never be fully mitigated; it advises deterministic limits on actions, dropping tool privileges when processing untrusted content, and logging inputs, outputs and tool calls ([NCSC](https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection)).

**Shadow AI is widespread and costly.** IBM's 2025 Cost of a Data Breach report found high shadow AI added USD 670,000 to average breach cost, 63% of 600 organisations had no AI governance policy, and 97% of those with AI incidents lacked AI access controls ([IBM](https://www.ibm.com/think/x-force/2025-cost-of-a-data-breach-navigating-ai)). Netskope's 2026 report found 47% of generative AI users still used personal AI apps, while sensitive-data policy incidents doubled to an average of 223 per month per organisation ([Netskope](https://www.netskope.com/resources/cloud-and-threat-reports/cloud-and-threat-report-2026)).

**Employee rule set.** 1. Use only approved, company-account AI tools. 2. Treat citations and quotes as unverified until you open the source. 3. Check high-stakes output against primary sources. 4. Do not let agents act on email, web or document content you do not trust. 5. Classify before you paste.

**Manager and IT checklist.** Publish an AI policy and approved-tool list and provision managed accounts; give agents least privilege with deterministic approval gates for sends, writes and payments; log prompts, outputs and tool calls; monitor for sensitive data going to personal AI apps; review auto-approve defaults in agentic tools; run an evaluation set before any agent reaches production.

## Adoption, change management and training ROI

The one rigorous evaluation opened is the UK Department for Business and Trade's three-month Microsoft 365 Copilot trial of 1,000 licences, evaluated by diary study, interviews, observed tasks and a usage dashboard ([DBT report](https://digitaltrade.blog.gov.uk/2025/09/25/discover-dbts-m365-copilot-evaluation-report/)). 72% of diary respondents were satisfied; time was saved on drafting, research summaries, meeting transcription, search and brainstorming, and none on image generation, scheduling or PowerPoint creation. Benefit was role-specific, and uncertainty about security and acceptable use made users cautious. Vendor-run studies with the same shape: Zoominfo's 400-developer Copilot rollout and the GitHub/Accenture randomised trial (department 41), the Thumbtack and Nulab case studies (departments 55 and 44), and Gartner's finding that only 32% of leaders say their last change achieved healthy adoption (department 57).

**ROI method:** pair self-reported diaries with usage telemetry, as DBT did. Every department entry carries five adoption KPIs and a capstone with a measured before-and-after comparison; these are the raw material for a Level 3 and Level 4 evaluation.

## Accessibility and AI as assistive technology

The European Accessibility Act has applied since 28 June 2025; internal training platforms are not obviously in scope, so legal review is needed ([Covington](https://www.insideglobaltech.com/2025/06/10/european-accessibility-act-june-2025-deadline-has-arrived/)). The US ADA Title II web rule requires WCAG 2.1 AA by 24 April 2026 for public bodies serving 50,000 or more and 26 April 2027 for smaller bodies ([LCW](https://www.lcwlegal.com/news/new-ada-title-ii-web-content-and-mobile-accessibility-deadlines/)). DBT found Copilot benefits for neurodiverse staff, people with hearing or vision impairments and non-native English speakers ([DBT neurodiversity post](https://digitaltrade.blog.gov.uk/2025/05/19/flying-with-co-pilot-how-ai-is-helping-neurodiverse-staff-thrive-in-dbt/)). **Recommendation:** build training content to WCAG 2.2 AA regardless of legal scope, and include an assistive-use module in the Core tier.

## Tiering and hours

The handbook's three tiers map onto the 60 departments as 16 Core, 28 Advanced and 16 Specialist. The tool deep dives converge on consistent hour bands: Core 6-10 hours per tool, Advanced 12-20 hours, Specialist 20-40 hours, with the highest estimates for platform-governance roles and the lowest for single-purpose tools. A department's total is the shared module (4-6 hours Core, 6-8 Advanced and Specialist) plus the sum of its three to five tool modules, less overlaps where the tools are surfaces of the same licence.
"""

RENAMES = [
    ("NotebookLM", "Gemini Notebook; NotebookLM Enterprise is Gemini Notebook Enterprise", "16 Jul 2026", "Verified (Google)"),
    ("Microsoft 365 Copilot", "Microsoft Copilot (licences may still carry the old name)", "Aug 2026", "Verified (Microsoft)"),
    ("Excel Copilot", "Copilot in Excel; the preview =COPILOT() function has been retired", "Retirement date not verified", "Verified (Microsoft Support)"),
    ("Azure AI Foundry", "Microsoft Foundry", "Announced Ignite, Nov 2025", "Verified (Microsoft Learn)"),
    ("Vertex AI (referenced by Google AI Studio and Claude Code)", "Gemini Enterprise Agent Platform (Google Cloud docs); the Claude Code profile uses the name Google Cloud Agent Platform", "2026", "Verified on Google Cloud docs"),
    ("Databricks Assistant", "Genie Code", "Mar 2026", "Verified (Databricks docs and community post)"),
    ("AuditBoard AI", "Optro and Optro AI", "9 Mar 2026", "Verified (press release, Accounting Today)"),
    ("Intercom Fin", "Fin (company renamed 12 May 2026), acquired by Salesforce 10 Sep 2026", "2026", "Verified (vendor and Salesforce releases)"),
    ("Dynatrace Davis AI", "Dynatrace Intelligence; Davis CoPilot evolving into Dynatrace Assist", "Jan 2026 (Perform)", "Verified (Dynatrace)"),
    ("Gemini Code Assist", "End of sale for Standard and Enterprise; agentic coding sold as Google Antigravity inside Gemini Enterprise", "9 Oct 2026", "Verified (Google Cloud docs)"),
    ("Amazon Q Developer", "Being retired in favour of Kiro; plugins, subscriptions and transformation end 30 Apr 2027", "2026-2027", "Verified (AWS blog)"),
    ("Jira Atlassian Intelligence", "Rovo (Atlassian Intelligence persists as the legacy name); usage-based billing begins 3 Dec 2026", "2025-2026", "Verified (Atlassian)"),
    ("Salesforce Einstein", "Einstein Copilot became Agentforce; Einstein now names the predictive features and Trust Layer inside the Agentforce 360 Platform", "Oct 2025 onward", "Verified (Salesforce)"),
    ("Tableau Pulse (Enhanced Q&A)", "Tableau Agent in Pulse", "2026", "Verified (Tableau help)"),
    ("Azure Copilot", "Renamed from Microsoft Copilot in Azure", "Dated notice not opened", "Verified name on Learn"),
    ("Workday AI (Workday Illuminate)", "Agents orchestrated by Sana; Sana is the new Workday home (13 Oct 2026 release)", "2026", "Rename of Illuminate to Sana rests on a secondary source"),
    ("Canva Magic Studio", "Canva AI", "Reported 16 Apr 2026", "Not verified (canva.com 403)"),
    ("Snowflake Cortex AI", "Cortex Code reportedly renamed CoCo and Snowflake Intelligence renamed CoWork", "Reported Jun 2026", "Not verified"),
    ("Cursor", "Anysphere is a SpaceX subsidiary since 14 Aug 2026, sold under The X Subscription", "2026", "Verified acquisition"),
    ("Perplexity and Perplexity Enterprise", "Two entries for one vendor; redundancy not verified", "n/a", "Open question"),
]

GAPS_MD = r"""
## Overall assessment

An independent critic pass over the first research run judged the tool research mostly solid, with pricing and product status well sourced for Claude, Figma, the coding assistants, Workday and UiPath. It found a structural hole on the department side (departments 52 and 53 missing, the Operations cluster resting on general practice, seven departments low confidence). A second research pass sourced all of them, so every one of the 60 departments now has at least one opened source and 59 are medium or high confidence. The critic also found the cross-cutting topics a CHRO, CIO or L&D director expects close to absent in the first run; the themes page was written to close those gaps and records which remain only partly sourced.

## Confidence at a glance

| Set | High | Medium | Low |
|---|---|---|---|
| 57 handbook tools | 10 | 39 | 8 |
| 60 handbook departments | 15 | 44 | 1 |

**Low-confidence tools and why.** ChatGPT Enterprise (openai.com returned 403; second-hand sources only). Canva Magic Studio (canva.com 403; rename to Canva AI unconfirmed). Adobe Firefly and Adobe Acrobat AI Assistant (pricing and legal FAQ not openable). ServiceNow Now Assist (docs pages did not render). Meta Advantage+ (business pages 403). Gainsight AI (gainsight.com 403). Google AI Studio (one opened page). **Low-confidence department.** 46 Enterprise Applications & ERP: all customer outcomes are vendor-sourced through a promotional trade-press article.

## Caveats that apply to the whole site

- **Vendor-reported outcomes.** Most quantified benefits are vendor claims or vendor-published case studies. Treat them as hypotheses to test with the department's own KPIs.
- **Second-hand ChatGPT data.** Every ChatGPT Enterprise and Business data-handling statement comes through third parties. Confirm against the OpenAI DPA and trust portal before putting it in a policy.
- **Pages that could not be opened.** openai.com, canva.com, adobe.com pricing and legal FAQ, gainsight.com, meta.com business pages, gartner.com, the European Commission AI literacy Q&A, the EBU/BBC study, docs.servicenow.com, Tableau and Google AI Studio pricing pages. Every claim that depended on them is marked not verified.
- **Regulatory hooks.** GDPR, SOX, HIPAA, PCI DSS and GxP references in department entries are general knowledge unless a source is cited next to them.
- **Dates.** Research ran on 24-25 October 2026. Names, prices and agent GA labels change monthly.
- **Hours.** All hour estimates are editorial, derived from the tool's capability surface and the handbook's tier bands.

## Recommendations for the curriculum

1. **Build one shared foundation module** covering governance (NIST AI RMF, EU AI Act Article 4 record-keeping), data classification by tool tier, verification, prompt-injection and agent-approval rules, and shadow-AI policy. Suggested 4-6 hours Core and 6-8 hours Advanced and Specialist.
2. **Teach a verification habit, not a prompting trick.** Assess the validation log and the before-and-after comparison in every capstone.
3. **Give agentic tools their own safety unit.** Require learners to demonstrate approval-gate configuration and least-privilege scoping before Specialist certification.
4. **Make the horizontal assistant modules tier-aware.** Separate what may be pasted into consumer, business and enterprise tiers, and name the residency limits.
5. **Cover the embedded assistants the handbook omits** where the organisation runs them: Veeva Vault QMS, Prosci Kaiya, Riskonnect, AlertMedia and Everbridge, Kinaxis Maestro and o9, Jira Service Management AI, LeanIX and Ardoq, Gemini Cloud Assist, Copilot Studio and Agent 365.
6. **Record attendance and content** against EU AI Act Article 4; add the EU Annex III and US state-law oversight unit for HR departments before December 2027.
7. **Build content to WCAG 2.2 AA** and include an assistive-use unit in the Core tier.
8. **Evaluate with telemetry plus diaries**, following the UK DBT design, and report Kirkpatrick Level 3 and 4 results per department.

## Recommendations for the matrix

1. **Collapse the Microsoft surfaces** into one tool with four modules; count Power BI Copilot and Power Automate separately.
2. **Replace "one tool per cell" with "the platform the company owns"** for SOC agents, observability, coding, cloud, data and AI platforms.
3. **Use current names with the handbook name in brackets** and schedule a quarterly name and status check. Plan replacement modules for Gemini Code Assist (Antigravity) and Amazon Q Developer (Kiro) now.
4. **Merge the two Perplexity rows** unless the organisation licenses both.
5. **Add a confidence column** to every matrix cell.
6. **Add a data-tier column** (consumer, business, enterprise) and a residency note for each horizontal tool.
7. **Carry hours as a range with the shared module subtracted.**
8. **Prioritise re-verification** of the eight low-confidence tools and department 46 before those cells are taught.
"""

METHOD_MD = r"""
## How the research was done

Research ran on 24-25 October 2026. Research and fact-check agents worked in parallel, one per tool group or department cluster, each instructed to cite only pages it had actually opened. A separate fact-check agent re-opened every cited page for each group, compared each claim against the page text, and removed or relabelled anything unsupported; the count of corrections appears on each group page. An independent critic then reviewed the whole result for missing departments, weak clusters, unsourced claims and absent cross-cutting topics; its six gap-fill tasks were researched by further agents, and the weakest clusters and departments were re-researched in a second pass. A second expansion pass then looked for tools and functions the handbook omits under ten further lenses. Editorial inferences are labelled as such.

## Verification labels

- **Verified** or an inline link: the claim was read on the linked page.
- **Not verified**: the claim came from a search snippet, a page that failed to open, or an earlier run whose page was not re-opened. It is kept only where useful and always labelled.
- **Vendor claim**, **vendor-reported**, **second-hand**: the page was opened but the figure is the vendor's own, or a third party quoting the vendor.
- **Confidence (high, medium, low)**: high means two or more independent opened sources agree on the core facts; medium means core facts are verified but secondary claims are not, or sources are vendor-only; low means a key page could not be opened or only one source exists.

## Known failures

HTTP 403 or empty renders from openai.com, help.openai.com, canva.com, adobe.com (pricing and legal FAQ), gainsight.com, business.meta.com, gartner.com, the European Commission AI literacy Q&A, the EBU/BBC news-integrity study, docs.servicenow.com, Tableau and Google AI Studio pricing pages, Business Wire, PDA and the Playwright v1.64 GitHub release page.
"""

ABOUT_MD = r"""
## About this site

This site is the web edition of the deep-research companion to the *Corporate AI Tools & Training Handbook* (60 departments, 57 tools, October 2026 revised edition), prepared for iMinds Academy curriculum planning. The long-form document with every section in one place is available as a Claude Doc; this site reorganises the same verified material into a learning path, a tool catalogue, a department directory, an interactive matrix and a comparison tool.

Every profile page links the pages a researcher opened. Where a claim could not be verified, it says so. Nothing on this site is a purchase recommendation, legal advice, or a substitute for reading the vendor's current contract terms.

## How to use it

- **Learners** start with the learning path and then open their own department.
- **Managers** open a department page for the capstone, KPIs and data rules.
- **Tool owners and IT** use the compare and matrix pages, then the gaps page for naming drift and re-verification needs.
- **Curriculum designers** use the themes page for the shared modules and the matrix for hours and overlap.

## Keeping it current

The underlying research is dated 24-25 October 2026. Tool names, prices and agent availability change monthly; the gaps page lists what had already moved. Plan a quarterly refresh.
"""
