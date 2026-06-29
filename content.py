# -*- coding: utf-8 -*-
"""
TAPIS DIGITECH — content registry
=================================
Data + light layout helpers for all GENERATED pages (services, industries,
solutions, trust, legal). The shared head/header/footer/CTA live in build.py.
Run `python3 tools/build.py` to (re)generate everything.

Every entry below is written to a real, unique purpose — no thin content. To
scale (300+ services etc.) you add dicts here, not hand-built HTML.
"""

DOMAIN = "https://www.tapisdigitech.com/"


# ---------------------------------------------------------------------------
# Reusable layout helpers (return HTML strings)
# ---------------------------------------------------------------------------
def page_hero(crumbs_html, h1, lead):
    return f"""<section class="page-hero">
  <div class="container">
    {crumbs_html}
    <h1>{h1}</h1>
    <p>{lead}</p>
  </div>
</section>
"""


def intro_split(icon, heading, paragraphs, checks):
    ps = "".join(f'<p class="muted" style="margin-bottom:18px">{t}</p>' for t in paragraphs)
    lis = "".join(f'<li><i class="fa-solid fa-circle-check"></i> {c}</li>' for c in checks)
    return f"""<section class="section">
  <div class="container grid-2">
    <div class="reveal">
      <div class="svc-ico" style="width:60px;height:60px;font-size:26px;margin-bottom:18px"><i class="{icon}"></i></div>
      <h2 style="font-size:clamp(1.6rem,3vw,2rem);margin-bottom:14px">{heading}</h2>
      {ps}
      <ul class="check-list">{lis}</ul>
    </div>
    <div class="reveal svc-visual">
      <div class="sv-grid"></div><div class="sv-glow"></div>
      <div class="sv-core"><i class="{icon}"></i></div>
      <span class="sv-chip sv-c1"><i class="fa-solid fa-bolt"></i></span>
      <span class="sv-chip sv-c2"><i class="fa-solid fa-circle-check"></i></span>
      <span class="sv-chip sv-c3"><i class="fa-solid fa-gears"></i></span>
      <span class="sv-chip sv-c4"><i class="fa-solid fa-chart-pie"></i></span>
    </div>
  </div>
</section>
"""


def feature_section(eyebrow, heading, sub, cards, alt=False):
    """cards = list of (icon, title, desc)."""
    c = "".join(
        f'<div class="feature-card reveal"><div class="svc-ico"><i class="{i}"></i></div>'
        f'<h3>{t}</h3><p>{d}</p></div>' for i, t, d in cards
    )
    klass = "section alt" if alt else "section"
    return f"""<section class="{klass}">
  <div class="container">
    <div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2>{heading}</h2><p>{sub}</p></div>
    <div class="grid-3">{c}</div>
  </div>
</section>
"""


def process_section(steps, alt=False):
    """steps = list of (title, desc)."""
    s = "".join(
        f'<div class="step reveal"><div class="step-num">{n}</div><h3>{t}</h3><p>{d}</p></div>'
        for n, (t, d) in enumerate(steps, 1)
    )
    klass = "section dark"
    return f"""<section class="{klass}">
  <div class="container">
    <div class="sec-head reveal"><span class="eyebrow" style="color:var(--blue-400)">How We Deliver</span><h2 style="color:#fff">A Proven Delivery Process</h2><p>From first conversation to compounding impact.</p></div>
    <div class="steps">{s}</div>
  </div>
</section>
"""


def related_engine(g, depth, groups):
    """
    The internal-linking engine. groups = list of dicts:
      {eyebrow, heading, cards: [(icon, label, desc, href)]}
    href values are root-relative and rewritten for depth.
    """
    blocks = []
    for gi, grp in enumerate(groups):
        cards = "".join(
            f'<a href="{g["rel"](href, depth)}" class="rel-card reveal">'
            f'<span class="rel-ico"><i class="{ic}"></i></span>'
            f'<span class="rel-txt"><b>{lb}</b><span>{ds}</span></span>'
            f'<i class="fa-solid fa-arrow-right rel-arrow" aria-hidden="true"></i></a>'
            for ic, lb, ds, href in grp["cards"]
        )
        alt = " alt" if gi % 2 else ""
        blocks.append(
            f'<section class="section{alt}"><div class="container">'
            f'<div class="sec-head reveal"><span class="eyebrow">{grp["eyebrow"]}</span><h2>{grp["heading"]}</h2></div>'
            f'<div class="rel-grid">{cards}</div></div></section>'
        )
    return "".join(blocks)


def placeholder_note(text):
    return (f'<div class="ph-note" role="note"><i class="fa-solid fa-circle-info" aria-hidden="true"></i> '
            f'<span><b>Placeholder —</b> {text}</span></div>')


def content_sections(sections):
    """sections = list of (heading, html_body). Rendered as readable prose blocks."""
    out = []
    for i, (h, body) in enumerate(sections):
        alt = " alt" if i % 2 else ""
        out.append(
            f'<section class="section{alt}"><div class="container" style="max-width:860px">'
            f'<h2 style="font-size:clamp(1.5rem,2.6vw,2rem);margin-bottom:18px">{h}</h2>'
            f'{body}</div></section>'
        )
    return "".join(out)


# ---------------------------------------------------------------------------
# DATA — Services (5 pillar detail pages, referenced by the nav dropdown)
# ---------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "ai-solutions", "id": "services", "icon": "fa-solid fa-brain",
        "name": "AI Solutions",
        "title": "AI Solutions & AI Agent Development",
        "desc": "Custom AI agents, chatbots, voice AI and workflow automation — designed around measurable business outcomes, not hype.",
        "lead": "We design and build production-grade AI systems — autonomous agents, copilots, chatbots and predictive analytics — engineered around the metrics your business actually cares about.",
        "intro_h": "Applied AI that ships, scales and pays for itself",
        "intro_p": [
            "Most AI projects stall in a demo. Ours go to production. We start from a bounded, measurable use case, instrument everything, keep a human in the loop where it matters, and expand coverage as confidence grows.",
            "We are model-agnostic — OpenAI, Claude, Gemini and open models — so the architecture fits your data, latency, privacy and cost constraints rather than a vendor's roadmap.",
        ],
        "checks": ["AI Strategy & Consulting", "AI Agents Development", "AI Chatbots & Voice AI",
                   "Workflow Automation", "AI Data Analysis", "Custom AI Solutions"],
        "features": ("What's Included", "Capabilities inside AI Solutions",
                     "A complete path from strategy to a system in production.", [
                         ("fa-solid fa-compass", "AI Strategy & Roadmap", "We identify the highest-ROI use cases and sequence them into a roadmap with clear success metrics."),
                         ("fa-solid fa-robot", "Autonomous Agents", "Agents that reason over context, call your tools and complete multi-step tasks end to end."),
                         ("fa-solid fa-comments", "Chatbots & Voice AI", "Support and sales assistants that resolve — not just deflect — across chat, voice and WhatsApp."),
                         ("fa-solid fa-gears", "Workflow Automation", "LLM-powered pipelines that remove repetitive operational work and reduce error rates."),
                         ("fa-solid fa-chart-line", "Predictive Analytics", "Models that forecast demand, churn and risk so teams can act earlier."),
                         ("fa-solid fa-shield-halved", "Safe Deployment", "Guardrails, evaluation harnesses and human-in-the-loop review built in from day one."),
                     ]),
        "process": [("Discover", "We map goals, data and constraints, and pick a bounded first use case."),
                    ("Strategy", "We design the architecture, model approach and evaluation plan."),
                    ("Build", "We ship in transparent sprints with demos and continuous evaluation."),
                    ("Scale", "We deploy with monitoring, then widen coverage as confidence grows.")],
        "related_ind": ["healthcare", "retail-ecommerce", "finance"],
        "related_sol": ["reduce-support-costs", "automate-operations"],
        "related_blog": [("ai-agents-customer-support", "fa-solid fa-robot", "AI", "How AI Agents Are Reshaping Customer Support")],
    },
    {
        "slug": "software-development", "id": "services", "icon": "fa-solid fa-code",
        "name": "Software Development",
        "title": "Custom Software & Product Development",
        "desc": "Web apps, mobile apps, SaaS platforms and custom software built on a modern, scalable, AI-ready stack.",
        "lead": "Robust, scalable software crafted for your exact workflows — web, mobile, SaaS and enterprise platforms, engineered to grow without painful rewrites.",
        "intro_h": "Engineering that holds up under real-world load",
        "intro_p": [
            "We build cloud-native systems on a modern stack (Next.js, React, TypeScript, Supabase, AWS) chosen for performance, security and scale. Clean architecture means your product can evolve as fast as your business.",
            "Every build is AI-ready by default, so adding agents, search or automation later is an upgrade — not a rebuild.",
        ],
        "checks": ["Website Development", "Web Applications", "Mobile App Development",
                   "SaaS Development", "CRM & ERP Solutions", "Custom Software"],
        "features": ("What's Included", "Capabilities inside Software Development",
                     "Product engineering from first prototype to enterprise scale.", [
                         ("fa-solid fa-window-maximize", "Web Applications", "Fast, accessible, SEO-strong web apps built on modern frameworks."),
                         ("fa-solid fa-mobile-screen", "Mobile Apps", "Cross-platform apps that share logic and ship faster."),
                         ("fa-solid fa-layer-group", "SaaS Platforms", "Multi-tenant, billing-ready SaaS with the scaffolding to scale."),
                         ("fa-solid fa-diagram-project", "CRM & ERP", "Systems tailored to your processes instead of forcing you into theirs."),
                         ("fa-solid fa-plug", "Integrations & APIs", "Reliable connections to the tools your business already runs on."),
                         ("fa-solid fa-vial", "Quality Engineering", "Automated testing and CI/CD so releases stay safe and frequent."),
                     ]),
        "process": [("Discover", "We define users, scope and the architecture that fits."),
                    ("Design", "We craft interfaces and data models around real needs."),
                    ("Build", "Engineers ship in fast sprints with continuous feedback."),
                    ("Scale", "We launch, monitor and optimise for sustained growth.")],
        "related_ind": ["retail-ecommerce", "finance", "healthcare"],
        "related_sol": ["automate-operations", "increase-revenue"],
        "related_blog": [("cloud-migration-guide", "fa-solid fa-cloud", "Cloud", "A No-Drama Guide to Cloud Migration")],
    },
    {
        "slug": "digital-marketing", "id": "services", "icon": "fa-solid fa-bullhorn",
        "name": "Digital Marketing",
        "title": "AI-Driven Digital Marketing & Growth",
        "desc": "SEO, paid media, content and conversion optimisation — data-driven marketing that fills your pipeline and compounds.",
        "lead": "Data-driven marketing that grows your brand, fills your pipeline and turns visitors into customers — amplified by AI and measured against revenue.",
        "intro_h": "Growth you can attribute, not just admire",
        "intro_p": [
            "We treat marketing as an engineering problem: clear hypotheses, instrumented funnels and ruthless iteration. Every channel maps to pipeline, not vanity metrics.",
            "AI accelerates research, content production and campaign optimisation so your team moves faster with smaller budgets.",
        ],
        "checks": ["Search Engine Optimization", "PPC & Google Ads", "Social Media Marketing",
                   "Content Marketing", "Email Marketing", "Conversion Optimization"],
        "features": ("What's Included", "Capabilities inside Digital Marketing",
                     "A full-funnel growth engine, built and operated.", [
                         ("fa-solid fa-magnifying-glass", "SEO & Content", "Topical-authority content architecture that earns durable organic traffic."),
                         ("fa-solid fa-rectangle-ad", "Paid Media", "Tightly measured Google and social campaigns optimised to CAC and ROAS."),
                         ("fa-solid fa-envelope-open-text", "Lifecycle & Email", "Automated nurture flows that convert and retain."),
                         ("fa-solid fa-flask", "Conversion Optimisation", "Experimentation that lifts the numbers that matter."),
                         ("fa-solid fa-chart-pie", "Analytics & Attribution", "Clean measurement so you know what actually works."),
                         ("fa-solid fa-share-nodes", "Social & Brand", "Consistent presence that builds trust at every touchpoint."),
                     ]),
        "process": [("Audit", "We benchmark channels, funnels and competitors."),
                    ("Plan", "We prioritise the highest-leverage growth bets."),
                    ("Execute", "We launch, measure and iterate weekly."),
                    ("Compound", "We double down on what works and scale it.")],
        "related_ind": ["retail-ecommerce", "finance"],
        "related_sol": ["increase-revenue", "reduce-support-costs"],
        "related_blog": [("business-automation-before-hiring", "fa-solid fa-gears", "Automation", "Automate These 7 Tasks Before Your Next Hire")],
    },
    {
        "slug": "branding-design", "id": "services", "icon": "fa-solid fa-pen-nib",
        "name": "Branding & Design",
        "title": "Branding, UI/UX & Product Design",
        "desc": "Brand identity, UI/UX and design systems that make people stop, trust and engage.",
        "lead": "Distinctive brand identities and interfaces that make people stop, trust and engage — design that does a job, not just decoration.",
        "intro_h": "Design that earns trust in the first three seconds",
        "intro_p": [
            "Great design is a business advantage: it lowers acquisition cost, raises conversion and makes products easier to use. We build identity and interface systems that scale across every surface.",
            "Our design systems hand off cleanly to engineering, so what you approve is what ships.",
        ],
        "checks": ["Brand Identity Design", "Logo & Visual Identity", "UI/UX Design",
                   "Landing Page Design", "Presentation Design", "Marketing Collateral"],
        "features": ("What's Included", "Capabilities inside Branding & Design",
                     "From brand strategy to a production-ready design system.", [
                         ("fa-solid fa-fingerprint", "Brand Identity", "Logo, palette, type and voice that make you recognisable."),
                         ("fa-solid fa-object-group", "UI/UX Design", "Research-led interfaces that are a pleasure to use."),
                         ("fa-solid fa-swatchbook", "Design Systems", "Reusable components that keep quality high as you scale."),
                         ("fa-solid fa-wand-magic-sparkles", "Landing Pages", "High-converting pages aligned to each campaign."),
                         ("fa-solid fa-file-powerpoint", "Presentation Design", "Decks that win rooms and close deals."),
                         ("fa-solid fa-images", "Collateral", "Consistent assets across every channel.")],
                     ),
        "process": [("Discover", "We learn your audience, market and goals."),
                    ("Define", "We set the brand strategy and direction."),
                    ("Design", "We craft the identity and interface system."),
                    ("Deliver", "We hand off production-ready assets and guidelines.")],
        "related_ind": ["hospitality", "real-estate"] if False else ["retail-ecommerce", "healthcare"],
        "related_sol": ["increase-revenue"],
        "related_blog": [("ai-agents-customer-support", "fa-solid fa-robot", "AI", "How AI Agents Are Reshaping Customer Support")],
    },
    {
        "slug": "cloud-it", "id": "services", "icon": "fa-solid fa-cloud",
        "name": "Cloud & IT Services",
        "title": "Cloud, DevOps & Managed IT",
        "desc": "Secure, resilient cloud infrastructure, DevOps and managed IT that keep your business running and growing.",
        "lead": "Secure, resilient cloud infrastructure and IT services that keep your business running and ready to scale — with security built in at every layer.",
        "intro_h": "Infrastructure you never have to think about",
        "intro_p": [
            "We design cloud foundations that are secure, observable and cost-efficient — then automate the operations so your team can focus on the product, not the plumbing.",
            "From migration to day-2 operations, we apply the same secure-by-default engineering we use across every TAPIS DIGITECH build.",
        ],
        "checks": ["Cloud Deployment", "DevOps & Automation", "Server Management",
                   "Cybersecurity Solutions", "Backup & Recovery", "IT Consulting"],
        "features": ("What's Included", "Capabilities inside Cloud & IT",
                     "Modern infrastructure, automated and secured.", [
                         ("fa-solid fa-cloud-arrow-up", "Cloud Deployment", "Architected for reliability, scale and sensible cost."),
                         ("fa-solid fa-infinity", "DevOps & CI/CD", "Automated pipelines for safe, frequent releases."),
                         ("fa-solid fa-server", "Managed Operations", "Monitoring, patching and on-call so systems stay healthy."),
                         ("fa-solid fa-lock", "Security & Compliance", "Access controls, encryption and hardening by default."),
                         ("fa-solid fa-database", "Backup & Recovery", "Tested restore paths so data is never a single point of failure."),
                         ("fa-solid fa-headset", "IT Consulting", "Pragmatic guidance to modernise without disruption.")],
                     ),
        "process": [("Assess", "We review current infrastructure and risks."),
                    ("Plan", "We design the target architecture and migration path."),
                    ("Migrate", "We move workloads with zero-downtime rollouts."),
                    ("Operate", "We monitor, secure and optimise continuously.")],
        "related_ind": ["finance", "healthcare"],
        "related_sol": ["automate-operations"],
        "related_blog": [("cloud-migration-guide", "fa-solid fa-cloud", "Cloud", "A No-Drama Guide to Cloud Migration")],
    },
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}

# ---------------------------------------------------------------------------
# DATA — Industries (exemplar detail pages establishing the template)
# ---------------------------------------------------------------------------
INDUSTRIES = [
    {
        "slug": "healthcare", "icon": "fa-solid fa-heart-pulse", "name": "Healthcare",
        "title": "AI & Software Solutions for Healthcare",
        "desc": "AI, automation and secure software for clinics, hospitals and health-tech — built around privacy and patient outcomes.",
        "lead": "We help healthcare organisations cut administrative load, improve patient experience and unlock data — with privacy and safety designed in from the start.",
        "intro_h": "Technology that gives clinicians time back",
        "intro_p": [
            "Healthcare runs on documentation, scheduling and coordination. AI and automation can absorb much of that load, letting clinical teams focus on patients.",
            "We build with privacy-first data handling and human-in-the-loop safeguards, because in healthcare, trust is the product.",
        ],
        "checks": ["Patient intake & triage automation", "Clinical documentation assistance",
                   "Appointment scheduling & reminders", "Secure patient portals",
                   "Analytics & population health", "Privacy-first data architecture"],
        "features": ("Use Cases", "Where we make the biggest difference",
                     "High-impact, well-bounded workflows that respect clinical safety.", [
                         ("fa-solid fa-clipboard-list", "Intake & Triage", "Conversational intake that routes patients faster and reduces no-shows."),
                         ("fa-solid fa-file-medical", "Documentation Support", "Assistants that draft notes for clinician review, never replacing judgement."),
                         ("fa-solid fa-calendar-check", "Scheduling", "Automated booking, reminders and follow-ups that fill calendars."),
                         ("fa-solid fa-shield-heart", "Privacy by Design", "Access controls and encryption aligned to healthcare expectations."),
                     ]),
        "process": [("Discover", "We map clinical and admin workflows and constraints."),
                    ("Design", "We scope a safe, measurable first use case."),
                    ("Build", "We ship with human-in-the-loop review and auditing."),
                    ("Scale", "We expand coverage as outcomes are proven.")],
        "related_svc": ["ai-solutions", "software-development", "cloud-it"],
        "related_sol": ["reduce-support-costs", "automate-operations"],
        "related_blog": [("ai-agents-customer-support", "fa-solid fa-robot", "AI", "How AI Agents Are Reshaping Customer Support")],
    },
    {
        "slug": "retail-ecommerce", "icon": "fa-solid fa-cart-shopping", "name": "Retail & E-commerce",
        "title": "AI & Software Solutions for Retail & E-commerce",
        "desc": "Personalisation, automation and AI support for retail and e-commerce brands that want to grow margins.",
        "lead": "We help retailers and online brands lift conversion, automate operations and deliver standout customer experience — measured against revenue.",
        "intro_h": "Sell more, serve better, spend less",
        "intro_p": [
            "Modern retail wins on experience and efficiency. AI personalises the journey while automation strips cost out of operations and support.",
            "We connect storefront, CRM and back-office so growth doesn't create chaos.",
        ],
        "checks": ["AI product recommendations", "Conversational shopping assistants",
                   "Support automation & returns", "Inventory & ops automation",
                   "Conversion optimisation", "Unified customer data"],
        "features": ("Use Cases", "Where we make the biggest difference",
                     "Revenue and efficiency levers across the funnel.", [
                         ("fa-solid fa-wand-sparkles", "Personalisation", "Recommendations that lift average order value."),
                         ("fa-solid fa-comments", "Shopping Assistants", "AI that answers, upsells and recovers carts."),
                         ("fa-solid fa-rotate-left", "Returns & Support", "Automated resolution for high-volume queries."),
                         ("fa-solid fa-boxes-stacked", "Ops Automation", "Inventory, fulfilment and reporting on autopilot."),
                     ]),
        "process": [("Discover", "We map the funnel and operations."),
                    ("Design", "We prioritise the biggest revenue levers."),
                    ("Build", "We ship and measure against conversion."),
                    ("Scale", "We compound wins across channels.")],
        "related_svc": ["ai-solutions", "digital-marketing", "software-development"],
        "related_sol": ["increase-revenue", "reduce-support-costs"],
        "related_blog": [("business-automation-before-hiring", "fa-solid fa-gears", "Automation", "Automate These 7 Tasks Before Your Next Hire")],
    },
    {
        "slug": "finance", "icon": "fa-solid fa-chart-line", "name": "Finance",
        "title": "AI & Software Solutions for Finance",
        "desc": "Secure automation, analytics and AI for financial services, fintech and finance teams.",
        "lead": "We help financial organisations automate operations, sharpen risk and analytics, and ship secure software — with controls and auditability built in.",
        "intro_h": "Speed and rigour, not a trade-off",
        "intro_p": [
            "Finance demands accuracy, security and auditability. We bring automation and AI to operations and analytics without compromising control.",
            "Secure-by-default engineering and clear audit trails are standard in everything we build for finance.",
        ],
        "checks": ["Process & reconciliation automation", "Risk & fraud analytics",
                   "Document processing", "Customer onboarding (KYC-ready)",
                   "Secure data platforms", "Compliance-minded architecture"],
        "features": ("Use Cases", "Where we make the biggest difference",
                     "Efficiency and insight, delivered securely.", [
                         ("fa-solid fa-file-invoice-dollar", "Process Automation", "Reconciliation and back-office workflows automated end to end."),
                         ("fa-solid fa-shield-halved", "Risk & Fraud", "Analytics that surface anomalies earlier."),
                         ("fa-solid fa-id-card", "Onboarding", "Faster, KYC-ready customer onboarding flows."),
                         ("fa-solid fa-lock", "Security & Audit", "Controls and trails aligned to financial expectations."),
                     ]),
        "process": [("Assess", "We review processes, data and risk."),
                    ("Design", "We scope a secure, measurable first use case."),
                    ("Build", "We ship with controls and auditability."),
                    ("Scale", "We extend with confidence.")],
        "related_svc": ["ai-solutions", "cloud-it", "software-development"],
        "related_sol": ["automate-operations", "increase-revenue"],
        "related_blog": [("cloud-migration-guide", "fa-solid fa-cloud", "Cloud", "A No-Drama Guide to Cloud Migration")],
    },
]
INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}

# ---------------------------------------------------------------------------
# DATA — Solutions (exemplar outcome-driven detail pages)
# ---------------------------------------------------------------------------
SOLUTIONS = [
    {
        "slug": "reduce-support-costs", "icon": "fa-solid fa-headset", "name": "Reduce Support Costs",
        "title": "Reduce Customer Support Costs with AI",
        "desc": "Resolve routine queries automatically and cut support cost per ticket — without hurting customer experience.",
        "lead": "Cut cost per ticket and response times by letting AI resolve routine, high-volume queries end to end — while your team focuses on the conversations that need a human.",
        "intro_h": "Lower cost and better experience — at the same time",
        "intro_p": [
            "Most support volume is repetitive and well-bounded: order status, resets, scheduling, tier-1 troubleshooting. AI agents can resolve these autonomously, around the clock.",
            "Done well, deflection becomes resolution: customers get outcomes faster, and your team is freed for complex, high-empathy work.",
        ],
        "checks": ["Autonomous resolution of tier-1 queries", "24/7 multilingual coverage",
                   "Smart escalation with full context", "Lower cost per ticket",
                   "Higher CSAT on routine issues", "Analytics on deflection & quality"],
        "features": ("How It Works", "The building blocks of this outcome",
                     "A pragmatic, measurable path to lower support cost.", [
                         ("fa-solid fa-robot", "Resolution Agents", "Agents that complete tasks, not just answer questions."),
                         ("fa-solid fa-route", "Smart Routing", "Confident hand-offs to humans with full context."),
                         ("fa-solid fa-globe", "Always-On Coverage", "Round-the-clock, multilingual support."),
                         ("fa-solid fa-gauge-high", "Quality Guardrails", "Evaluation and human review keep answers safe."),
                     ]),
        "process": [("Scope", "We pick the highest-volume, lowest-risk queries first."),
                    ("Build", "We deploy agents with guardrails and routing."),
                    ("Measure", "We track deflection, CSAT and cost per ticket."),
                    ("Expand", "We widen coverage as quality is proven.")],
        "related_svc": ["ai-solutions", "software-development"],
        "related_ind": ["retail-ecommerce", "healthcare", "finance"],
        "related_blog": [("ai-agents-customer-support", "fa-solid fa-robot", "AI", "How AI Agents Are Reshaping Customer Support")],
    },
    {
        "slug": "automate-operations", "icon": "fa-solid fa-gears", "name": "Automate Operations",
        "title": "Automate Repetitive Operations",
        "desc": "Replace manual, repetitive operational work with reliable automation and AI workflows.",
        "lead": "Reclaim hours every week by letting software handle repetitive operational work — fewer errors, faster cycle times and a team focused on higher-value work.",
        "intro_h": "Automate the work nobody should be doing by hand",
        "intro_p": [
            "Data entry, reporting, reconciliation, handoffs between tools — this work is slow, error-prone and demoralising. Automation removes it.",
            "We map your processes, automate the repetitive steps, and keep humans in control of the decisions that matter.",
        ],
        "checks": ["Process mapping & prioritisation", "Cross-tool workflow automation",
                   "Document & data processing", "Automated reporting",
                   "Fewer errors & faster cycles", "Clear audit trails"],
        "features": ("How It Works", "The building blocks of this outcome",
                     "Reliable automation that earns trust quickly.", [
                         ("fa-solid fa-diagram-project", "Workflow Automation", "Connect the tools you already use into reliable pipelines."),
                         ("fa-solid fa-file-lines", "Document Processing", "Extract and route data without manual rekeying."),
                         ("fa-solid fa-chart-column", "Automated Reporting", "Always-current reports without the spreadsheet grind."),
                         ("fa-solid fa-user-check", "Human-in-the-Loop", "People approve the decisions that matter."),
                     ]),
        "process": [("Map", "We document the process and the cost of doing it by hand."),
                    ("Automate", "We build and test the workflow."),
                    ("Verify", "We confirm accuracy and add audit trails."),
                    ("Scale", "We roll out across teams.")],
        "related_svc": ["ai-solutions", "cloud-it", "software-development"],
        "related_ind": ["finance", "healthcare", "retail-ecommerce"],
        "related_blog": [("business-automation-before-hiring", "fa-solid fa-gears", "Automation", "Automate These 7 Tasks Before Your Next Hire")],
    },
    {
        "slug": "increase-revenue", "icon": "fa-solid fa-arrow-trend-up", "name": "Increase Revenue",
        "title": "Increase Revenue with AI & Growth Engineering",
        "desc": "Grow pipeline and conversion with AI-driven marketing, personalisation and product improvements.",
        "lead": "Grow pipeline and lift conversion with AI-driven marketing, personalisation and product experiences — every initiative measured against revenue.",
        "intro_h": "Compounding growth, not one-off spikes",
        "intro_p": [
            "Revenue growth comes from many small, measured improvements across acquisition, conversion and retention. We engineer that system and run it.",
            "AI accelerates research, content and personalisation so each cycle does more with less.",
        ],
        "checks": ["Topical-authority SEO & content", "Conversion-rate optimisation",
                   "AI personalisation", "Lifecycle & retention", "Attribution & analytics",
                   "Experimentation engine"],
        "features": ("How It Works", "The building blocks of this outcome",
                     "A growth system you can attribute to revenue.", [
                         ("fa-solid fa-magnifying-glass", "Organic Growth", "Content architecture that earns durable traffic."),
                         ("fa-solid fa-flask", "Conversion Optimisation", "Experiments that lift the numbers that matter."),
                         ("fa-solid fa-wand-sparkles", "Personalisation", "Relevant experiences that convert and retain."),
                         ("fa-solid fa-chart-pie", "Attribution", "Clean measurement so you invest in what works."),
                     ]),
        "process": [("Audit", "We benchmark funnels and opportunities."),
                    ("Plan", "We prioritise the highest-leverage bets."),
                    ("Execute", "We launch and measure weekly."),
                    ("Compound", "We scale what works.")],
        "related_svc": ["digital-marketing", "ai-solutions", "branding-design"],
        "related_ind": ["retail-ecommerce", "finance"],
        "related_blog": [("business-automation-before-hiring", "fa-solid fa-gears", "Automation", "Automate These 7 Tasks Before Your Next Hire")],
    },
]
SOLUTION_BY_SLUG = {s["slug"]: s for s in SOLUTIONS}


# ---------------------------------------------------------------------------
# BUILD
# ---------------------------------------------------------------------------
def build(g):
    rel = g["rel"]
    g["rel"] = rel  # ensure available to helpers via g
    _build_services(g)
    _build_industries(g)
    _build_solutions(g)
    _build_trust(g)
    _build_legal(g)


def _svc_related_groups(g, depth, svc):
    groups = [{
        "eyebrow": "Industries", "heading": "Industries we serve with this",
        "cards": [(INDUSTRY_BY_SLUG[s]["icon"], INDUSTRY_BY_SLUG[s]["name"],
                   INDUSTRY_BY_SLUG[s]["desc"], "industries/%s.html" % s) for s in svc["related_ind"]]
    }, {
        "eyebrow": "Solutions", "heading": "Outcomes this service powers",
        "cards": [(SOLUTION_BY_SLUG[s]["icon"], SOLUTION_BY_SLUG[s]["name"],
                   SOLUTION_BY_SLUG[s]["desc"], "solutions/%s.html" % s) for s in svc["related_sol"]]
    }, {
        "eyebrow": "Insights", "heading": "Related reading",
        "cards": [(ic, lb, "Read the article", "blog/%s.html" % sl) for sl, ic, tg, lb in svc["related_blog"]]
    }]
    return groups


def _build_services(g):
    depth = 1
    for svc in SERVICES:
        path = "services/%s.html" % svc["slug"]
        trail = [("Home", ""), ("Services", "services.html"), (svc["name"], path)]
        crumbs = g["breadcrumb"](depth, [("Home", "index.html"), ("Services", "services.html"), (svc["name"], None)])
        body = page_hero(crumbs, svc["title"], svc["lead"])
        body += intro_split(svc["icon"], svc["intro_h"], svc["intro_p"], svc["checks"])
        body += feature_section(*svc["features"], alt=True)
        body += process_section(svc["process"])
        body += related_engine(g, depth, _svc_related_groups(g, depth, svc))
        schema = [{
            "@type": "Service", "name": svc["title"], "serviceType": svc["name"],
            "provider": {"@id": DOMAIN + "#organization"}, "areaServed": "Worldwide",
            "url": DOMAIN + path, "description": svc["desc"],
        }]
        g["page"](path, depth, "services", svc["title"], svc["desc"], trail, body, schema)


def _ind_related_groups(g, depth, ind):
    return [{
        "eyebrow": "Services", "heading": "Services for this industry",
        "cards": [(SERVICE_BY_SLUG[s]["icon"], SERVICE_BY_SLUG[s]["name"],
                   SERVICE_BY_SLUG[s]["desc"], "services/%s.html" % s) for s in ind["related_svc"]]
    }, {
        "eyebrow": "Solutions", "heading": "Outcomes for this industry",
        "cards": [(SOLUTION_BY_SLUG[s]["icon"], SOLUTION_BY_SLUG[s]["name"],
                   SOLUTION_BY_SLUG[s]["desc"], "solutions/%s.html" % s) for s in ind["related_sol"]]
    }, {
        "eyebrow": "Insights", "heading": "Related reading",
        "cards": [(ic, lb, "Read the article", "blog/%s.html" % sl) for sl, ic, tg, lb in ind["related_blog"]]
    }]


def _build_industries(g):
    depth = 1
    for ind in INDUSTRIES:
        path = "industries/%s.html" % ind["slug"]
        trail = [("Home", ""), ("Industries", "industries.html"), (ind["name"], path)]
        crumbs = g["breadcrumb"](depth, [("Home", "index.html"), ("Industries", "industries.html"), (ind["name"], None)])
        body = page_hero(crumbs, ind["title"], ind["lead"])
        body += intro_split(ind["icon"], ind["intro_h"], ind["intro_p"], ind["checks"])
        body += feature_section(*ind["features"], alt=True)
        body += process_section(ind["process"])
        body += related_engine(g, depth, _ind_related_groups(g, depth, ind))
        g["page"](path, depth, "industries", ind["title"], ind["desc"], trail, body)


def _sol_related_groups(g, depth, sol):
    return [{
        "eyebrow": "Services", "heading": "Services that deliver this outcome",
        "cards": [(SERVICE_BY_SLUG[s]["icon"], SERVICE_BY_SLUG[s]["name"],
                   SERVICE_BY_SLUG[s]["desc"], "services/%s.html" % s) for s in sol["related_svc"]]
    }, {
        "eyebrow": "Industries", "heading": "Where this applies",
        "cards": [(INDUSTRY_BY_SLUG[s]["icon"], INDUSTRY_BY_SLUG[s]["name"],
                   INDUSTRY_BY_SLUG[s]["desc"], "industries/%s.html" % s) for s in sol["related_ind"]]
    }, {
        "eyebrow": "Insights", "heading": "Related reading",
        "cards": [(ic, lb, "Read the article", "blog/%s.html" % sl) for sl, ic, tg, lb in sol["related_blog"]]
    }]


def _build_solutions(g):
    depth = 1
    for sol in SOLUTIONS:
        path = "solutions/%s.html" % sol["slug"]
        trail = [("Home", ""), ("Solutions", "solutions.html"), (sol["name"], path)]
        crumbs = g["breadcrumb"](depth, [("Home", "index.html"), ("Solutions", "solutions.html"), (sol["name"], None)])
        body = page_hero(crumbs, sol["title"], sol["lead"])
        body += intro_split(sol["icon"], sol["intro_h"], sol["intro_p"], sol["checks"])
        body += feature_section(*sol["features"], alt=True)
        body += process_section(sol["process"])
        body += related_engine(g, depth, _sol_related_groups(g, depth, sol))
        g["page"](path, depth, "solutions", sol["title"], sol["desc"], trail, body)


# ---- Trust foundation -------------------------------------------------------
def _build_trust(g):
    from trust_content import build_trust
    build_trust(g, page_hero, content_sections, feature_section, related_engine,
                placeholder_note, DOMAIN)


# ---- Legal ------------------------------------------------------------------
def _build_legal(g):
    from legal_content import build_legal
    build_legal(g, page_hero, content_sections, placeholder_note)
