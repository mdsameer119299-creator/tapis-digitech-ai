# -*- coding: utf-8 -*-
import re
p="index.html"; s=open(p,encoding="utf-8").read()

# ---- 1) Hero copy: AI-first transformation positioning ----
s=s.replace('<span class="badge-pill"><span class="dot"></span> AI &amp; Digital Transformation Company</span>',
            '<span class="badge-pill"><span class="dot"></span> Enterprise AI Transformation Company</span>')
s=s.replace('<h1>Enterprise AI That Actually <span class="text-blue">Grows Businesses</span></h1>',
            '<h1>Transform Your Business with <span class="text-blue">Enterprise AI</span></h1>')
s=s.replace('<p class="lead">We build AI, automation and digital products that turn complex operations into measurable, compounding growth.</p>',
            '<p class="lead">We help businesses cut costs, increase sales and automate operations with AI — backed by enterprise-grade engineering. Software, cloud and data are how we deliver it.</p>')
s=s.replace('<a href="services.html" class="btn btn-ghost btn-lg">Explore Services <i class="fa-solid fa-arrow-right"></i></a>',
            '<a href="#platform" class="btn btn-ghost btn-lg">See the AI Platform <i class="fa-solid fa-arrow-right"></i></a>')
s=s.replace('<p>Trusted by <b>100+ businesses</b> worldwide</p>',
            '<p>An <b>AI-first</b> partner for ambitious businesses worldwide</p>')

# ---------- helpers ----------
def sec(inner, cls="section"):
    return f'<section class="{cls}">\n  <div class="container">\n{inner}\n  </div>\n</section>\n'
def head(eyebrow,h2,sub,dark=False):
    style=' style="color:#fff"' if dark else ''
    eb=' style="color:var(--blue-400)"' if dark else ''
    return (f'    <div class="sec-head reveal"><span class="eyebrow"{eb}>{eyebrow}</span>'
            f'<h2{style}>{h2}</h2><p>{sub}</p></div>\n')
def mod(icon,t,d):
    return (f'<div class="mod-card reveal"><div class="svc-ico"><i class="{icon}"></i></div>'
            f'<h3>{t}</h3><p>{d}</p></div>')
def feat(icon,t,d):
    return (f'<div class="feature-card reveal"><div class="svc-ico"><i class="{icon}"></i></div>'
            f'<h3>{t}</h3><p>{d}</p></div>')
def cap(icon,t,d,metric):
    return (f'<div class="cap-card reveal"><div class="cap-ico"><i class="{icon}"></i></div>'
            f'<h3>{t}</h3><p>{d}</p><span class="cap-metric"><i class="fa-solid fa-bolt"></i> {metric}</span></div>')
def fbox(text,icon=None,accent=False,small=False):
    cl="flow-box"+(" accent" if accent else "")+(" small" if small else "")
    ic=f'<i class="{icon}"></i>' if icon else ''
    return f'<div class="{cl}">{ic}{text}</div>'
ARROW='<div class="flow-arrow" aria-hidden="true"></div>'
def chip(text,icon):
    return f'<span class="flow-chip"><i class="{icon}"></i>{text}</span>'

NEW=[]

# ---- A) Business Challenge -> Vision ----
inner=head("The Business Challenge","Your competitors aren’t buying more software. They’re deploying AI.",
           "Rising costs, manual work and slow decisions are the real limits on growth — and they’re exactly what AI removes.")
inner+='''    <div class="grid-2">
      <div class="reveal">
        <h3 style="font-size:24px;margin-bottom:14px">From digitised to genuinely intelligent</h3>
        <p class="muted" style="margin-bottom:18px">For two decades businesses competed on who had the best software. The next decade belongs to companies whose operations can think, decide and act with AI. TAPIS DIGITECH makes that transition practical, safe and measurable — starting from your highest-cost, highest-friction processes.</p>
        <ul class="check-list">
          <li><i class="fa-solid fa-circle-check"></i> Replace manual work with autonomous AI workflows</li>
          <li><i class="fa-solid fa-circle-check"></i> Turn scattered data into real-time decisions</li>
          <li><i class="fa-solid fa-circle-check"></i> Scale output without scaling headcount</li>
          <li><i class="fa-solid fa-circle-check"></i> Keep humans in control of what matters</li>
        </ul>
      </div>
      <div class="reveal svc-visual">
        <div class="sv-grid"></div><div class="sv-glow"></div>
        <div class="sv-core"><i class="fa-solid fa-brain"></i></div>
        <span class="sv-chip sv-c1"><i class="fa-solid fa-coins"></i></span>
        <span class="sv-chip sv-c2"><i class="fa-solid fa-arrow-trend-up"></i></span>
        <span class="sv-chip sv-c3"><i class="fa-solid fa-gears"></i></span>
        <span class="sv-chip sv-c4"><i class="fa-solid fa-face-smile"></i></span>
      </div>
    </div>
'''
NEW.append(sec(inner))

# ---- B) Enterprise AI Platform (modules) ----
mods=[("fa-solid fa-robot","AI Agents","Autonomous agents that complete real tasks across your tools."),
("fa-solid fa-gears","AI Automation","Remove repetitive work and cut operational cost."),
("fa-solid fa-chart-line","AI Analytics","Turn scattered data into decisions you can act on."),
("fa-solid fa-book-open","Knowledge AI","Instant answers from your documents and policies."),
("fa-solid fa-microphone-lines","Voice AI","Handle calls and voice queries without adding staff."),
("fa-solid fa-file-lines","Document Intelligence","Extract, classify and process documents automatically."),
("fa-solid fa-headset","Customer Support AI","Resolve routine queries 24/7 and lift satisfaction."),
("fa-solid fa-arrow-trend-up","Sales AI","Qualify leads and follow up faster to win more deals."),
("fa-solid fa-diagram-project","Operations AI","Streamline back-office workflows end to end."),
("fa-solid fa-chart-pie","Business Intelligence","Live dashboards that surface what actually matters."),
("fa-solid fa-sitemap","Workflow Automation","Connect systems into reliable, monitored flows."),
("fa-solid fa-plug","Enterprise Integrations","Plug AI into CRM, ERP, email, WhatsApp and more.")]
inner=head("The TAPIS AI Platform","One integrated AI platform — not a pile of tools",
           "Modular capabilities that snap together around your business. Start with one module, expand as value compounds.")
inner+='    <div class="mod-grid">'+"".join(mod(*m) for m in mods)+'</div>\n'
NEW.append('<section class="section alt" id="platform">\n  <div class="container">\n'+inner+'  </div>\n</section>\n')

# ---- C) Business Outcomes ----
outs=[("fa-solid fa-coins","Reduce Operational Costs","Automation removes repetitive work and costly errors.","AI Automation"),
("fa-solid fa-arrow-trend-up","Increase Sales","Faster lead response and AI-assisted selling.","Sales AI"),
("fa-solid fa-gears","Automate Repetitive Work","Free your team from manual, low-value tasks.","Workflow Automation"),
("fa-solid fa-face-smile","Improve Customer Experience","Instant, accurate, around-the-clock service.","Customer Support AI"),
("fa-solid fa-bolt","Accelerate Decisions","Real-time analytics replace slow guesswork.","AI Analytics"),
("fa-solid fa-arrows-rotate","Modernize Legacy Processes","Bring old workflows into an AI-native era.","Operations AI"),
("fa-solid fa-people-group","Scale Without More Headcount","Grow output without growing payroll.","AI Agents"),
("fa-solid fa-shield-halved","Reduce Risk & Errors","Consistent, auditable, monitored execution.","Document Intelligence")]
inner=head("Business Outcomes","We sell results, not technology",
           "Every engagement maps to a measurable business outcome. The technology is how we get there.")
inner+='    <div class="cap-grid">'+"".join(cap(*o) for o in outs)+'</div>\n'
NEW.append(sec(inner))

# ---- D) Enterprise AI Architecture (dark flow) ----
sources=["CRM","ERP","WhatsApp","Email","Documents","Databases","Cloud"]
src_icons=["fa-solid fa-database","fa-solid fa-cubes","fa-brands fa-whatsapp","fa-solid fa-envelope","fa-solid fa-file-lines","fa-solid fa-server","fa-solid fa-cloud"]
flow=('    <div class="flow reveal">\n'
      '      <div class="flow-row">'+"".join(chip(t,i) for t,i in zip(sources,src_icons))+'</div>\n'
      f'      {ARROW}\n      {fbox("TAPIS AI Platform","fa-solid fa-brain",accent=True)}\n'
      f'      {ARROW}\n      {fbox("AI Agents","fa-solid fa-robot")}\n'
      f'      {ARROW}\n      {fbox("Automation","fa-solid fa-gears")}\n'
      f'      {ARROW}\n      {fbox("Analytics","fa-solid fa-chart-line")}\n'
      f'      {ARROW}\n      {fbox("Better Business Decisions","fa-solid fa-bullseye",accent=True)}\n'
      '    </div>\n')
inner=head("Enterprise AI Architecture","AI that connects the systems you already run","dark"==None and "" or "We integrate with your stack — your data stays yours. AI sits on top, orchestrating work across every tool.",dark=True)
NEW.append('<section class="section dark">\n  <div class="container">\n'+inner+flow+'  </div>\n</section>\n')

# ---- E) Real AI Workflows ----
def workflow(title, steps):
    out=f'      <div class="reveal"><div class="flow-title">{title}</div>\n      <div class="flow">\n'
    for i,(t,ic,acc) in enumerate(steps):
        out+=f'        {fbox(t,ic,accent=acc,small=True)}\n'
        if i<len(steps)-1: out+=f'        {ARROW}\n'
    out+='      </div></div>\n'
    return out
w1=workflow("Enquiry → Proposal",[
 ("Customer enquiry","fa-solid fa-inbox",False),("AI agent reads CRM + documents","fa-solid fa-robot",True),
 ("Generates tailored proposal","fa-solid fa-file-invoice",False),("Emails the customer","fa-solid fa-paper-plane",False),
 ("Updates ERP & dashboard","fa-solid fa-chart-pie",True)])
w2=workflow("Invoice → Posted Entry",[
 ("Invoice received","fa-solid fa-file-lines",False),("Document AI extracts data","fa-solid fa-magnifying-glass",True),
 ("Validated against ERP","fa-solid fa-circle-check",False),("Exceptions flagged for review","fa-solid fa-user-check",False),
 ("Posted & team notified","fa-solid fa-bell",True)])
inner=head("Real AI Workflows","This is what AI actually does in your business",
           "Not abstract intelligence — concrete, auditable workflows that run across your systems, with humans in the loop where it counts.")
inner+='    <div class="flow-2">\n'+w1+w2+'    </div>\n'
NEW.append(sec(inner,"section alt"))

# ---- F) Supporting capabilities (reframed services) ----
inner=head("Capabilities","Everything we do exists to deploy AI in your business",
           "AI is the core. Software, cloud, data and design are the engineering muscle that makes AI work in the real world.")
caps=[("fa-solid fa-brain","AI Solutions","The core engine — agents, automation, analytics and custom AI.","services/ai-solutions.html"),
("fa-solid fa-code","Software Development","The applications and platforms your AI runs inside.","services/software-development.html"),
("fa-solid fa-cloud","Cloud & IT","The secure, scalable infrastructure AI is deployed on.","services/cloud-it.html"),
("fa-solid fa-bullhorn","Digital Marketing","AI-amplified growth that turns capability into pipeline.","services/digital-marketing.html"),
("fa-solid fa-pen-nib","Branding & Design","The interfaces that make AI usable and trusted.","services/branding-design.html")]
cards="".join(f'<a href="{h}" class="svc-card reveal"><div class="svc-ico"><i class="{i}"></i></div><h3>{t}</h3><p style="font-size:14.5px;color:var(--muted);margin-bottom:16px">{d}</p><span class="svc-more">Explore <i class="fa-solid fa-arrow-right"></i></span></a>' for i,t,d,h in caps)
inner+='    <div class="services-grid">'+cards+'</div>\n'
NEW.append(sec(inner))

# ---- G) Industry AI use cases (teaser) ----
def uc(icon,name,items,href):
    lis="".join(f'<li>{x}</li>' for x in items)
    return (f'<a href="{href}" class="uc-card reveal"><div class="uc-head"><div class="svc-ico"><i class="{icon}"></i></div>'
            f'<h3>{name}</h3></div><ul class="svc-list">{lis}</ul>'
            f'<span class="svc-more" style="margin-top:14px">See {name} AI <i class="fa-solid fa-arrow-right"></i></span></a>')
ucs=[uc("fa-solid fa-industry","Manufacturing",["Predictive maintenance","Quality inspection AI","Production planning","Inventory forecasting"],"industries.html#manufacturing"),
uc("fa-solid fa-heart-pulse","Healthcare",["AI appointment assistant","Patient support AI","Medical documentation","Workflow automation"],"industries/healthcare.html"),
uc("fa-solid fa-cart-shopping","Retail & E-commerce",["Demand forecasting","Recommendation engine","AI customer support","Inventory optimisation"],"industries/retail-ecommerce.html")]
inner=head("Industry AI Use Cases","We know how AI applies to your industry",
           "From the factory floor to the trading desk — practical AI use cases mapped to each sector.")
inner+='    <div class="uc-grid">'+"".join(ucs)+'</div>\n'
inner+='    <div class="center reveal" style="margin-top:40px"><a href="industries.html" class="btn btn-light">Explore all industries <i class="fa-solid fa-arrow-right"></i></a></div>\n'
NEW.append(sec(inner,"section alt"))

# ---- H) AI Products ----
def product(icon,t,status,stcls,d):
    return (f'<div class="feature-card product-card reveal"><span class="status-badge {stcls}">{status}</span>'
            f'<div class="svc-ico"><i class="{icon}"></i></div><h3>{t}</h3><p>{d}</p></div>')
prods=[("fa-solid fa-arrow-trend-up","AI Sales Assistant","Private Beta","st-beta","Qualifies leads, drafts follow-ups and updates your CRM automatically."),
("fa-solid fa-headset","AI Customer Support","Coming Soon","st-soon","Resolves routine tickets across chat, email and WhatsApp, 24/7."),
("fa-solid fa-book-open","AI Knowledge Platform","In Development","st-dev","A private assistant trained on your documents, policies and data."),
("fa-solid fa-file-invoice","AI Proposal Generator","In Development","st-dev","Generates tailored proposals from a short brief and your CRM."),
("fa-solid fa-user-tie","AI Recruitment Assistant","Coming Soon","st-soon","Screens resumes and schedules interviews to speed up hiring."),
("fa-solid fa-sitemap","AI Workflow Studio","In Development","st-dev","Build and monitor multi-step AI workflows without heavy code.")]
inner=head("AI Products","We don’t just deliver projects — we build products",
           "A growing suite of AI products, in active development. Nothing here is generally available yet.")
inner+='    <div class="grid-3">'+"".join(product(*p) for p in prods)+'</div>\n'
inner+='    <div class="ph-note reveal" style="margin-top:28px;max-width:760px;margin-left:auto;margin-right:auto"><i class="fa-solid fa-circle-info" aria-hidden="true"></i><span><b>Placeholder —</b> product names, statuses and availability are indicative and in development. None are generally available. <a href="contact.html" style="color:inherit;text-decoration:underline">Contact us</a> to join an early-access waitlist.</span></div>\n'
NEW.append(sec(inner))

# ---- I) Technology stack (grouped) ----
def techcat(name, chips_):
    cs="".join(chip(t,i) for t,i in chips_)
    return (f'<div class="feature-card reveal"><h3 style="font-size:16px;margin-bottom:14px">{name}</h3>'
            f'<div class="flow-row" style="justify-content:flex-start">{cs}</div></div>')
cats=[("Large Language Models",[("OpenAI","fa-solid fa-brain"),("Claude","fa-solid fa-robot"),("Gemini","fa-solid fa-gem")]),
("AI & Automation",[("n8n","fa-solid fa-diagram-project"),("Workflow Pipelines","fa-solid fa-sitemap")]),
("Frontend",[("Next.js","fa-solid fa-code"),("React","fa-brands fa-react"),("TypeScript","fa-solid fa-file-code")]),
("Backend & Data",[("Supabase","fa-solid fa-database"),("Vector Search","fa-solid fa-magnifying-glass")]),
("Cloud",[("AWS","fa-brands fa-aws"),("Vercel","fa-solid fa-bolt")]),
("Deployment & DevOps",[("Docker","fa-brands fa-docker"),("GitHub","fa-brands fa-github")])]
inner=head("Technology Stack","A modern, AI-ready stack — chosen per project",
           "We are model-agnostic and cloud-native. We pick the right tools for your data, latency, privacy and cost.")
inner+='    <div class="grid-3">'+"".join(techcat(*c) for c in cats)+'</div>\n'
NEW.append(sec(inner,"section alt"))

# ---- J) Why choose us (differentiators) ----
whys=[("fa-solid fa-brain","AI-First Architecture","Every solution is designed around AI from the start, not bolted on."),
("fa-solid fa-shield-halved","Enterprise-Grade Engineering","Secure, observable, production systems built to be depended on."),
("fa-solid fa-bullseye","Business-Focused AI","We optimise for your metrics, not for novelty."),
("fa-solid fa-lock","Secure Deployments","Least-privilege access, encryption and privacy by design."),
("fa-solid fa-plug","Scalable Integrations","AI that plugs into the systems you already run."),
("fa-solid fa-screwdriver-wrench","Custom AI Development","Built for your workflows — no rigid templates."),
("fa-solid fa-handshake","Long-Term Partnership","We stay after launch to optimise and evolve."),
("fa-solid fa-user-check","Human-in-the-Loop Design","People stay in control of consequential decisions."),
("fa-solid fa-arrow-trend-up","Continuous Improvement","We measure, learn and improve every cycle.")]
inner=head("Why TAPIS DIGITECH","Why businesses choose us for AI",
           "Not vanity claims — the engineering and partnership principles that make AI work.")
inner+='    <div class="why-grid">'+"".join(f'<div class="why-card reveal"><div class="svc-ico"><i class="{i}"></i></div><h3>{t}</h3><p>{d}</p></div>' for i,t,d in whys)+'</div>\n'
NEW.append(sec(inner))

# ---- K) Process (AI delivery) ----
steps=[("fa-solid fa-magnifying-glass","STEP 1","Discover","We find the highest-ROI AI use cases and define success metrics."),
("fa-solid fa-lightbulb","STEP 2","Strategy","We design the architecture and AI approach for real business value."),
("fa-solid fa-code","STEP 3","Build","We ship in fast, transparent sprints with continuous evaluation."),
("fa-solid fa-rocket","STEP 4","Deploy","We launch securely with monitoring and human-in-the-loop controls."),
("fa-solid fa-arrow-trend-up","STEP 5","Optimize","We measure, learn and expand — compounding the impact.")]
inner=head("How We Work","From business problem to AI in production","A clear, proven path — de-risked at every step.",dark=True)
inner+='    <div class="proc">'+"".join(f'<div class="proc-step reveal"><div class="proc-dot"><i class="{i}"></i></div><div class="proc-num">{n}</div><h3>{t}</h3><p>{d}</p></div>' for i,n,t,d in steps)+'</div>\n'
NEW.append('<section class="section dark">\n  <div class="container">\n'+inner+'  </div>\n</section>\n')

# ---- L) Case studies (illustrative) ----
inner=head("Illustrative Outcomes","The kind of impact we build toward",
           "Representative scenarios that show how AI transformation plays out. Verified, attributable case studies will replace these.")
inner+='''    <div class="ph-note reveal" style="max-width:820px;margin:0 auto 32px"><i class="fa-solid fa-circle-info" aria-hidden="true"></i><span><b>Placeholder —</b> the figures below are illustrative examples, not verified client results. Real, attributable case studies will be published here.</span></div>
    <div class="grid-3"><div class="case-card reveal">
      <div class="case-top" style="background:linear-gradient(135deg,#2090ea,#0a1124)"><i class="fa-solid fa-headset" style="position:static;font-size:54px;opacity:.95"></i></div>
      <div class="case-body"><span class="tag">Illustrative · Support</span><h3>Support Automation</h3><p>An AI support agent resolves routine, high-volume queries end to end, freeing the team for complex cases.</p>
      <div class="case-metrics"><div><b>24/7</b><span>Coverage</span></div><div><b>Tier-1</b><span>Auto-resolved</span></div></div></div>
    </div><div class="case-card reveal">
      <div class="case-top" style="background:linear-gradient(135deg,#1574c4,#0a1124)"><i class="fa-solid fa-gears" style="position:static;font-size:54px;opacity:.95"></i></div>
      <div class="case-body"><span class="tag">Illustrative · Operations</span><h3>Operations Automation</h3><p>Document and workflow automation removes manual rekeying across finance and back-office processes.</p>
      <div class="case-metrics"><div><b>Fewer</b><span>Errors</span></div><div><b>Faster</b><span>Cycles</span></div></div></div>
    </div><div class="case-card reveal">
      <div class="case-top" style="background:linear-gradient(135deg,#0e4f8f,#0a1124)"><i class="fa-solid fa-robot" style="position:static;font-size:54px;opacity:.95"></i></div>
      <div class="case-body"><span class="tag">Illustrative · AI Suite</span><h3>Enterprise AI Suite</h3><p>An AI assistant suite unifying CRM, support and analytics in one workspace.</p>
      <div class="case-metrics"><div><b>Soon</b><span>In development</span></div><div><b>AI</b><span>Native</span></div></div></div>
    </div></div>
    <div class="center reveal" style="margin-top:40px"><a href="case-studies.html" class="btn btn-light">View case studies <i class="fa-solid fa-arrow-right"></i></a></div>
'''
NEW.append(sec(inner,"section alt"))

# ---- M) Blog ----
inner=head("Insights","Practical thinking on applied AI","How we deploy AI, automation and modern software for real businesses.")
inner+='''    <div class="blog-grid"><a href="blog/ai-agents-customer-support.html" class="blog-card reveal">
      <div class="blog-cover" style="background:linear-gradient(135deg,#2090ea,#0a1124)"><i class="fa-solid fa-robot"></i></div>
      <div class="blog-body"><div class="blog-meta"><span class="tag">AI</span><span>6 min read</span></div>
      <h3>How AI Agents Are Reshaping Customer Support in 2026</h3><p>Where autonomous agents add real value — and where human judgement still wins.</p><span class="svc-more">Read article <i class="fa-solid fa-arrow-right"></i></span></div></a>
      <a href="blog/business-automation-before-hiring.html" class="blog-card reveal">
      <div class="blog-cover" style="background:linear-gradient(135deg,#1574c4,#0a1124)"><i class="fa-solid fa-gears"></i></div>
      <div class="blog-body"><div class="blog-meta"><span class="tag">Automation</span><span>5 min read</span></div>
      <h3>Automate These 7 Tasks Before Your Next Hire</h3><p>Reclaim hours every week by letting AI handle the repetitive work.</p><span class="svc-more">Read article <i class="fa-solid fa-arrow-right"></i></span></div></a>
      <a href="blog/cloud-migration-guide.html" class="blog-card reveal">
      <div class="blog-cover" style="background:linear-gradient(135deg,#0e4f8f,#0a1124)"><i class="fa-solid fa-cloud"></i></div>
      <div class="blog-body"><div class="blog-meta"><span class="tag">Cloud</span><span>7 min read</span></div>
      <h3>A No-Drama Guide to Cloud Migration</h3><p>The checklist we use to move businesses to the cloud with zero downtime.</p><span class="svc-more">Read article <i class="fa-solid fa-arrow-right"></i></span></div></a></div>
'''
NEW.append(sec(inner))

NEW_HTML="\n".join(NEW)

# ---- Inject: keep hero + trusted, replace middle up to FAQ; keep existing FAQ + CTA ----
# We insert NEW between trusted section close and the existing "Our Core Services" section,
# then remove old sections from there up to the FAQ section (keep FAQ + CTA).
trusted_close = s.index('</section>', s.index('<section class="trusted">')) + len('</section>')
faq_start = s.index('<section class="section">\n  <div class="container" style="max-width:840px">')
s = s[:trusted_close] + "\n\n" + NEW_HTML + "\n" + s[faq_start:]
open(p,"w",encoding="utf-8").write(s)
print("homepage rebuilt; new length", len(s))
