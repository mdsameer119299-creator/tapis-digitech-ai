# -*- coding: utf-8 -*-
"""
TAPIS DIGITECH — Trust foundation pages.
Truthful descriptions of *approach*. Anything requiring verified facts
(certifications, audit reports, sub-processor lists) is a clearly-marked
placeholder — never invented.
"""


def _trust_nav(g, depth, current):
    items = [
        ("index", "Trust Center", "trust/index.html"),
        ("security", "Security", "trust/security.html"),
        ("responsible-ai", "Responsible AI", "trust/responsible-ai.html"),
        ("technology-stack", "Technology Stack", "trust/technology-stack.html"),
        ("development-process", "Development Process", "trust/development-process.html"),
        ("quality-assurance", "Quality Assurance", "trust/quality-assurance.html"),
    ]
    parts = []
    for key, label, href in items:
        on = key == current
        cls = "chip chip-on" if on else "chip"
        aria = ' aria-current="page"' if on else ""
        parts.append('<a href="%s" class="%s"%s>%s</a>' % (g["rel"](href, depth), cls, aria, label))
    links = "".join(parts)
    return ('<section class="section" style="padding:30px 0 0"><div class="container">'
            '<div class="subnav" aria-label="Trust Center sections">%s</div></div></section>' % links)


def build_trust(g, page_hero, content_sections, feature_section, related_engine, ph, DOMAIN):
    depth = 1

    def crumbs(name):
        return g["breadcrumb"](depth, [("Home", "index.html"), ("Trust Center", "trust/index.html"), (name, None)])

    def crumbs_home():
        return g["breadcrumb"](depth, [("Home", "index.html"), ("Trust Center", None)])

    # ---- Trust Center hub ----
    path = "trust/index.html"
    trail = [("Home", ""), ("Trust Center", path)]
    body = page_hero(crumbs_home(), "Trust Center",
                     "How TAPIS DIGITECH approaches security, privacy, responsible AI and quality — in one place. This is the home for the assurances enterprise buyers need.")
    body += _trust_nav(g, depth, "index")
    body += feature_section("What's Inside", "Everything you need to evaluate us",
                            "Each area below explains our approach today and what formal documentation is on the roadmap.", [
                                ("fa-solid fa-lock", "Security", "Our security model, data handling and the controls we build in by default."),
                                ("fa-solid fa-scale-balanced", "Responsible AI", "How we deploy AI safely, with human oversight and clear boundaries."),
                                ("fa-solid fa-layer-group", "Technology Stack", "The vetted, modern technologies we build on and why."),
                                ("fa-solid fa-diagram-project", "Development Process", "How we plan, build, review and release software."),
                                ("fa-solid fa-clipboard-check", "Quality Assurance", "How we keep quality high across testing, accessibility and performance."),
                                ("fa-solid fa-file-shield", "Privacy & Legal", "Our privacy policy and terms, written for clarity."),
                            ], alt=True)
    body += content_sections([
        ("Our commitment", "<p>We build technology that organisations depend on, so trust is not an afterthought — it is part of the engineering. The pages in this Trust Center describe, honestly, how we work today and where formal certification is planned.</p>"
         + ph("Formal certifications, audit reports (e.g. SOC 2), and a downloadable security package will be linked here once finalised. Nothing on these pages should be read as a current certification unless explicitly stated.")),
    ])
    body += related_engine(g, depth, [{
        "eyebrow": "Explore", "heading": "Continue in the Trust Center",
        "cards": [
            ("fa-solid fa-lock", "Security", "Data protection and controls", "trust/security.html"),
            ("fa-solid fa-scale-balanced", "Responsible AI", "Safe, accountable AI", "trust/responsible-ai.html"),
            ("fa-solid fa-layer-group", "Technology Stack", "What we build on", "trust/technology-stack.html"),
        ]}])
    g["page"](path, depth, None, "Trust Center", "Security, privacy, responsible AI and quality at TAPIS DIGITECH — the assurances enterprise buyers need, in one place.", trail, body)

    # ---- Security ----
    path = "trust/security.html"
    trail = [("Home", ""), ("Trust Center", "trust/index.html"), ("Security", path)]
    body = page_hero(crumbs("Security"),
                     "Security",
                     "Security is built into every layer of what we design and build — not bolted on at the end.")
    body += _trust_nav(g, depth, "security")
    body += content_sections([
        ("Our security approach", "<p>We practise secure-by-default engineering. Access is least-privilege, data is encrypted in transit and at rest, secrets are managed centrally, and we design systems to be observable so issues are caught early. Security review is part of our standard development process rather than a separate gate.</p>"),
        ("Data protection", "<p>We handle client and end-user data on a need-to-know basis, segregate environments, and prefer privacy-preserving designs (data minimisation, scoped retention). When we build on third-party platforms we choose vendors with strong security postures and clear data-processing terms.</p>"),
        ("AI &amp; data", "<p>For AI systems we are deliberate about what data is sent to which model provider, support deployments that keep sensitive data in your environment, and never use your private data to train shared models without explicit agreement.</p>"),
        ("Reporting a vulnerability", "<p>We welcome responsible disclosure. Security contact details are published in our <code>security.txt</code> file. We aim to acknowledge reports promptly and keep reporters informed.</p>"),
        ("Certifications &amp; formal assurance", ph("Verified certifications (e.g. ISO 27001, SOC 2 Type II), penetration-test summaries and a complete sub-processor list will be published here once available. Provide these documents and we will link them. Do not represent any certification as held until it is listed here with evidence.")),
    ])
    g["page"](path, depth, None, "Security", "How TAPIS DIGITECH protects data with secure-by-default engineering, encryption, least-privilege access and responsible AI data handling.", trail, body)

    # ---- Responsible AI ----
    path = "trust/responsible-ai.html"
    trail = [("Home", ""), ("Trust Center", "trust/index.html"), ("Responsible AI", path)]
    body = page_hero(crumbs("Responsible AI"),
                     "Responsible AI",
                     "We build AI that is useful, accountable and safe — with humans in control of the decisions that matter.")
    body += _trust_nav(g, depth, "responsible-ai")
    body += feature_section("Our Principles", "How we deploy AI responsibly",
                            "Principles we apply on every AI engagement.", [
                                ("fa-solid fa-user-check", "Human Oversight", "People stay in control of consequential decisions; AI assists, it does not unilaterally decide."),
                                ("fa-solid fa-bullseye", "Bounded Use Cases", "We deploy AI on well-scoped problems with clear success and failure criteria."),
                                ("fa-solid fa-magnifying-glass-chart", "Evaluation", "We measure quality with evaluation harnesses before and after launch."),
                                ("fa-solid fa-shield-halved", "Safety Guardrails", "Input/output checks, escalation paths and monitoring reduce harmful or wrong outputs."),
                                ("fa-solid fa-eye", "Transparency", "Users are told when they are interacting with AI and how to reach a human."),
                                ("fa-solid fa-scale-balanced", "Fairness & Privacy", "We watch for bias and design for data minimisation and consent."),
                            ], alt=True)
    body += content_sections([
        ("Why this matters", "<p>AI creates real value when it is reliable and trusted. Our approach favours measurable, well-bounded deployments with human oversight over flashy autonomy. This is how we keep AI accountable to your business and your customers.</p>"),
        ("Governance", ph("A formal AI ethics / governance policy and model-usage register can be published here. We will draft these to match your organisation's risk posture and regulatory environment.")),
    ])
    g["page"](path, depth, None, "Responsible AI", "TAPIS DIGITECH's responsible-AI principles: human oversight, bounded use cases, evaluation, safety guardrails, transparency and fairness.", trail, body)

    # ---- Technology Stack ----
    path = "trust/technology-stack.html"
    trail = [("Home", ""), ("Trust Center", "trust/index.html"), ("Technology Stack", path)]
    body = page_hero(crumbs("Technology Stack"),
                     "Technology Stack",
                     "A modern, vetted, AI-ready stack chosen for performance, security and scale.")
    body += _trust_nav(g, depth, "technology-stack")
    body += feature_section("What We Build With", "A deliberate, modern stack",
                            "We choose technologies for reliability and longevity, not novelty.", [
                                ("fa-solid fa-brain", "AI & Models", "OpenAI, Claude, Gemini and open models — selected per use case (model-agnostic)."),
                                ("fa-brands fa-react", "Frontend", "Next.js, React and TypeScript for fast, accessible, SEO-strong interfaces."),
                                ("fa-solid fa-database", "Data", "Supabase and managed databases with sensible backup and access controls."),
                                ("fa-brands fa-aws", "Cloud", "AWS and Vercel for reliable, scalable, observable infrastructure."),
                                ("fa-solid fa-diagram-project", "Automation", "n8n and custom pipelines for reliable workflow automation."),
                                ("fa-brands fa-docker", "DevOps", "Docker, GitHub and CI/CD for safe, frequent releases."),
                            ], alt=True)
    body += content_sections([
        ("How we choose technology", "<p>We pick tools that are widely supported, secure and a good fit for your constraints — not whatever is trending. Being model-agnostic and cloud-native means we can optimise for your latency, privacy and cost requirements, and avoid lock-in where it would hurt you.</p>"),
    ])
    g["page"](path, depth, None, "Technology Stack", "The modern, AI-ready technology stack TAPIS DIGITECH builds on: OpenAI/Claude/Gemini, Next.js, React, Supabase, AWS, Vercel, Docker and more.", trail, body)

    # ---- Development Process ----
    path = "trust/development-process.html"
    trail = [("Home", ""), ("Trust Center", "trust/index.html"), ("Development Process", path)]
    body = page_hero(crumbs("Development Process"),
                     "Development Process",
                     "How we plan, build, review and release — transparent sprints with quality built in.")
    body += _trust_nav(g, depth, "development-process")
    body += content_sections([
        ("Discovery &amp; scoping", "<p>Every engagement starts by aligning on goals, constraints and success metrics. We define the smallest valuable first slice so you see working software quickly.</p>"),
        ("Design &amp; architecture", "<p>We design the data model, architecture and interfaces up front, choosing patterns that scale and avoid rework. Security and accessibility are considered here, not later.</p>"),
        ("Build in transparent sprints", "<p>We ship in short iterations with regular demos. You always know what is done, what is next, and where the risks are. Code is reviewed before it merges.</p>"),
        ("Test &amp; review", "<p>Automated tests, code review and quality checks run continuously. Larger changes get extra review. We treat accessibility and performance as acceptance criteria.</p>"),
        ("Release &amp; operate", "<p>We release through CI/CD with the ability to roll back safely, then monitor in production. After launch we measure, learn and improve.</p>"),
    ])
    g["page"](path, depth, None, "Development Process", "TAPIS DIGITECH's development process: discovery, design, transparent sprints, continuous testing and review, and safe releases with monitoring.", trail, body)

    # ---- Quality Assurance ----
    path = "trust/quality-assurance.html"
    trail = [("Home", ""), ("Trust Center", "trust/index.html"), ("Quality Assurance", path)]
    body = page_hero(crumbs("Quality Assurance"),
                     "Quality Assurance",
                     "Quality is a standard, not a phase — across testing, accessibility, performance and security.")
    body += _trust_nav(g, depth, "quality-assurance")
    body += feature_section("How We Keep Quality High", "Quality engineered in",
                            "The practices that keep what we ship dependable.", [
                                ("fa-solid fa-vial", "Automated Testing", "Unit, integration and end-to-end tests guard against regressions."),
                                ("fa-solid fa-universal-access", "Accessibility", "We build to WCAG best practices and test with real assistive tech in mind."),
                                ("fa-solid fa-gauge-high", "Performance", "We budget for speed and measure Core Web Vitals."),
                                ("fa-solid fa-code-compare", "Code Review", "Every change is reviewed before it ships."),
                                ("fa-solid fa-shield-halved", "Security Checks", "Dependency and security scanning are part of the pipeline."),
                                ("fa-solid fa-chart-line", "Monitoring", "We watch production and act on issues quickly."),
                            ], alt=True)
    body += content_sections([
        ("Our quality targets", "<p>For websites and web apps we aim for excellent Lighthouse scores — strong performance, full accessibility, best practices and SEO — and we treat these as acceptance criteria rather than nice-to-haves.</p>"),
    ])
    g["page"](path, depth, None, "Quality Assurance", "TAPIS DIGITECH's QA approach: automated testing, accessibility, performance budgets, code review, security scanning and production monitoring.", trail, body)
