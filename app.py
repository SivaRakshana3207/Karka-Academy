import os
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from dotenv import load_dotenv

try:
    from groq import Groq
except Exception:
    Groq = None

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
PUBLIC_STATIC_DIR = BASE_DIR / "public" / "static"
STATIC_DIR = PUBLIC_STATIC_DIR if os.getenv("VERCEL") and PUBLIC_STATIC_DIR.is_dir() else BASE_DIR / "static"
DB_PATH = Path(
    os.getenv("KARKA_DB_PATH")
    or (Path(tempfile.gettempdir()) / "karka.db" if os.getenv("VERCEL") else BASE_DIR / "karka.db")
)

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "karka-demo-secret-change-me")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

SITE = {
    "name": "KARKA",
    "tagline": "Build. Ship. Get Hired.",
    "location": "Nagercoil, Tamil Nadu",
    "phone": "+91 93455 80857",
    "email": "team.hr@karka.academy",
    "instagram": "@karka.ai",
}

TRACKS = [
    {
        "id": "fullstack",
        "category": "Coding & Development",
        "filter_group": "coding",
        "eyebrow": "🔥 MOST POPULAR · 94% PLACEMENT RATE",
        "title": "React + Python Fullstack",
        "desc": "Architect production web systems from responsive React interfaces to scalable Python microservices, PostgreSQL databases, and Docker pipelines.",
        "stack": ["React 19", "Python", "FastAPI", "PostgreSQL", "Docker", "REST"],
        "duration": "180 Days (Full-time)",
        "tone": "plum",
        "salary_range": "₹4.5L – ₹11.5L PA",
        "projects_count": "5 Production Apps",
        "key_outcome": "Fullstack Engineer / Backend Specialist",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Frontend Core: HTML5/CSS3 Mastery, ES6+ JS, React 19 Components & Hooks"},
            {"week": "Weeks 5–8", "topic": "Backend Mastery: Python, FastAPI/Flask, SQLAlchemy, Auth, RESTful API Design"},
            {"week": "Weeks 9–12", "topic": "Databases & Cloud: PostgreSQL, Migrations, Redis Caching, Dockerization"},
            {"week": "Weeks 13–24", "topic": "Live Client Capstone, CI/CD Pipelines, System Architecture & ATS Polish"}
        ]
    },
    {
        "id": "mern",
        "category": "Coding & Development",
        "filter_group": "coding",
        "eyebrow": "⚡ HIGH DEMAND · STARTUP FAVORITE",
        "title": "MERN Fullstack Architecture",
        "desc": "Master the world's most ubiquitous modern stack. Ship single-page web apps, event-driven Node.js APIs, and real-time MongoDB applications.",
        "stack": ["MongoDB", "Express", "React", "Node.js", "WebSockets", "Cloud"],
        "duration": "180 Days (Full-time)",
        "tone": "orange",
        "salary_range": "₹4.2L – ₹10.8L PA",
        "projects_count": "4 Full-Stack Deployments",
        "key_outcome": "MERN Developer / Frontend Specialist",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Modern JavaScript, State Machines, React SPA Architecture & Tailwind CSS"},
            {"week": "Weeks 5–8", "topic": "Node.js Asynchronous Runtime, Express Middleware, JWT Security, REST"},
            {"week": "Weeks 9–12", "topic": "MongoDB Aggregation Pipelines, Mongoose Modeling, WebSockets Real-time"},
            {"week": "Weeks 13–24", "topic": "Production Deployment, Monorepo Setup, Performance Profiling & Mock Interviews"}
        ]
    },
    {
        "id": "genai",
        "category": "Data / AI",
        "filter_group": "ai",
        "eyebrow": "🚀 THE FUTURE · 3.5X SALARY HIKE",
        "title": "Generative AI & LLM Engineering",
        "desc": "Turn cutting-edge foundation models into autonomous business agents, custom RAG pipelines, fine-tuned LLMs, and intelligent automation systems.",
        "stack": ["LLMs", "LangChain", "LlamaIndex", "Vector DBs", "RAG", "Python"],
        "duration": "180 Days (Immersive)",
        "tone": "violet",
        "salary_range": "₹6.0L – ₹14.5L PA",
        "projects_count": "4 Autonomous AI Systems",
        "key_outcome": "Gen AI Engineer / AI Solutions Architect",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Python for AI, Vector Math, Prompt Engineering & API Orchestration (OpenAI/Anthropic/Groq)"},
            {"week": "Weeks 5–8", "topic": "RAG Pipelines: Embeddings, Chunking Strategies, Chroma/Pinecone Vector Search"},
            {"week": "Weeks 9–12", "topic": "Autonomous AI Agents: LangGraph, Tools Calling, Memory, Self-Healing Code"},
            {"week": "Weeks 13–24", "topic": "Local LLMs (Ollama/vLLM), Model Evaluation, Enterprise AI Deployment"}
        ]
    },
    {
        "id": "datascience",
        "category": "Data / AI",
        "filter_group": "ai",
        "eyebrow": "📊 HIGH GROWTH · BUSINESS CRITICAL",
        "title": "AI, Machine Learning & Data Science",
        "desc": "Transform messy raw datasets into high-impact predictive models, automated computer vision/NLP engines, and dynamic executive dashboards.",
        "stack": ["Python", "SQL", "Pandas", "Scikit-Learn", "PyTorch", "Tableau"],
        "duration": "180 Days (Full-time)",
        "tone": "yellow",
        "salary_range": "₹4.8L – ₹12.0L PA",
        "projects_count": "5 Data & ML Products",
        "key_outcome": "Data Scientist / Machine Learning Engineer",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Statistical Foundations, Advanced SQL, Pandas Data Wrangling & Exploratory Analysis"},
            {"week": "Weeks 5–8", "topic": "Supervised & Unsupervised Machine Learning with Scikit-Learn & Feature Engineering"},
            {"week": "Weeks 9–12", "topic": "Deep Learning with PyTorch, Computer Vision / NLP Basics & Model Optimization"},
            {"week": "Weeks 13–24", "topic": "Production ML Pipelines, Model Drift Monitoring, Tableau Storytelling & Client Demos"}
        ]
    },
    {
        "id": "uiux",
        "category": "Business / Management",
        "filter_group": "design",
        "eyebrow": "🎨 PRODUCT OBSESSED · HIGH IMPACT",
        "title": "UI/UX & Product Experience Design",
        "desc": "Design world-class digital products from scratch. Master user research, design systems, high-fidelity micro-interactions, and engineering handoffs.",
        "stack": ["Figma", "Design Systems", "Prototyping", "User Research", "Wireframing"],
        "duration": "120–180 Days",
        "tone": "pink",
        "salary_range": "₹4.0L – ₹9.5L PA",
        "projects_count": "3 Agency-Ready Case Studies",
        "key_outcome": "Product Designer / UI/UX Specialist",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Design Principles, Psychology of UX, Information Architecture & User Journey Mapping"},
            {"week": "Weeks 5–8", "topic": "Advanced Figma: Component Libraries, Auto-Layout 5.0, Variables & Design Tokens"},
            {"week": "Weeks 9–12", "topic": "Interactive Micro-Prototyping, Usability Testing & Accessibility (WCAG 2.1)"},
            {"week": "Weeks 13–24", "topic": "Full App Redesign Case Study, Developer Handoff & Portfolio Review with Industry Leaders"}
        ]
    },
    {
        "id": "internship",
        "category": "Internship",
        "filter_group": "internship",
        "eyebrow": "💼 REAL CODE · CORPORATE IMMERSION",
        "title": "Full Stack Developer Internship",
        "desc": "Step onto real client deliverables from week one. Work with senior engineers, participate in daily standups, submit code reviews, and ship live software.",
        "stack": ["Agile Sprints", "Git Flow", "Code Reviews", "DevOps", "Client Delivery"],
        "duration": "180 Days (Industry Immersion)",
        "tone": "cyan",
        "salary_range": "Stipend + Pre-Placement Offer (PPO)",
        "projects_count": "Live Client Deployments",
        "key_outcome": "Production-Ready Software Engineer",
        "syllabus": [
            {"week": "Weeks 1–4", "topic": "Onboarding, Production Codebase Walkthrough, Git Flow, Standard Linters & CI"},
            {"week": "Weeks 5–8", "topic": "Sprint 1: Feature Development, Unit Testing, Pair Programming & Code Reviews"},
            {"week": "Weeks 9–16", "topic": "Sprint 2 & 3: Production Client Deliverables, Performance Optimization & Bug Fixes"},
            {"week": "Weeks 17–24", "topic": "Capstone Demo to Stakeholders, PPO Evaluation, ATS Resume & Placement Launch"}
        ]
    },
]

PILLARS = [
    (
        "01",
        "Business Communication & Fluency",
        "Executive Speaking · Tech Storytelling · Client Demos · Writing",
        "Master the confidence to pitch ideas, conduct standups, and speak like a tech leader."
    ),
    (
        "02",
        "Modern App Architecture",
        "React · Python · Node · APIs · Cloud DevOps · Scalable DBs",
        "No outdated college theory. You write production code that users actually touch."
    ),
    (
        "03",
        "AI Multiplier Skills",
        "Prompt Engineering · Autonomous Agents · RAG · Copilots · LLMs",
        "Harness AI as a 10x multiplier to build faster, test smarter, and solve complex logic."
    ),
    (
        "04",
        "Interview & Placement Mastery",
        "ATS Resume · 1-on-1 Mock Interviews · System Design · Behavioral Coaching",
        "Walk into interviews with undeniable project proof, polished charisma, and salary leverage."
    ),
]

PERSONAS = [
    {
        "id": "developer",
        "label": "Software Developer",
        "summary": "You want to build real products, ship clean code, and command high engineering salaries.",
        "path": "Full Stack Development (React + Python / MERN)",
        "stage": "Build 4 client-grade production web apps and master modern Git & DevOps workflows.",
        "icon": "💻"
    },
    {
        "id": "ai",
        "label": "AI / Data Professional",
        "summary": "You want to ride the Generative AI wave, build autonomous agents, and unlock predictive insights.",
        "path": "Gen AI & LLM Engineering / Data Science",
        "stage": "Learn vector embeddings, RAG pipelines, and deploy AI copilots from scratch.",
        "icon": "🤖"
    },
    {
        "id": "design",
        "label": "UI/UX Designer",
        "summary": "You want to craft jaw-dropping user experiences, design systems, and mobile apps that feel magical.",
        "path": "UI/UX Product Design & Systems",
        "stage": "Create 3 comprehensive Figma case studies with live prototypes and developer handoffs.",
        "icon": "🎨"
    },
    {
        "id": "switcher",
        "label": "Career Switcher",
        "summary": "You have a degree in Mechanical, Civil, Commerce, or Arts and want a lucrative, secure career in tech.",
        "path": "Zero-to-Hero Tech Acceleration",
        "stage": "Begin with absolute fundamentals, 1-on-1 mentorship, and step-by-step project sprints.",
        "icon": "🔄"
    },
    {
        "id": "student",
        "label": "College / Fresher",
        "summary": "Tired of cramming textbooks and struggling with campus placements? You need real proof.",
        "path": "Full Stack Developer Internship",
        "stage": "Skip the certificate hoarders. Build real client software with senior engineer guidance.",
        "icon": "🎓"
    },
]

DISCOVERY_STEPS = [
    {"id": "learn", "label": "01 Learn", "detail": "Master industry-standard stacks with live mentor sessions."},
    {"id": "build", "label": "02 Build", "detail": "Ship 4-5 real-world production applications from scratch."},
    {"id": "intern", "label": "03 Intern", "detail": "Work on live client deliverables under senior engineer code reviews."},
    {"id": "communicate", "label": "04 Polish", "detail": "Sharpen executive communication, client demos & tech storytelling."},
    {"id": "interview", "label": "05 Prep", "detail": "Tackle 30+ mock technical interviews, algorithmic tests & ATS resumes."},
    {"id": "launch", "label": "06 Get Hired", "detail": "Step into high-growth tech roles with Pay After Placement peace of mind."},
]

PROJECTS = [
    {
        "id": "omniagent",
        "name": "OmniAgent AI",
        "tagline": "Autonomous Multi-Modal Enterprise Agent",
        "category": "Gen AI / Python",
        "stack": ["Python", "LangChain", "FastAPI", "ChromaDB", "React"],
        "problem": "Enterprise customer teams drowning in 20,000+ support queries with slow manual lookups.",
        "outcome": "Engineered an autonomous AI copilot with dynamic RAG vector retrieval, tool-calling for DB mutations, and automated human escalation.",
        "metrics": "⚡ Sub-350ms response · 94.2% intent precision · 24/7 uptime",
        "badge": "Client Project"
    },
    {
        "id": "pulsepay",
        "name": "PulsePay High-Throughput Ledger",
        "tagline": "Real-time FinTech Reconciliation Engine",
        "category": "Fullstack / Backend",
        "stack": ["Node.js", "Express", "PostgreSQL", "Redis", "Docker"],
        "problem": "Payment gateway dropouts causing mismatch between merchant settlements and banking ledgers.",
        "outcome": "Architected an idempotent transaction processing queue with Redis caching, PostgreSQL ACID guarantees, and automated webhook retries.",
        "metrics": "🔥 6,500+ simulated tps · Zero transaction drop · Automated failover",
        "badge": "FinTech Architecture"
    },
    {
        "id": "campusos",
        "name": "Karka Campus OS",
        "tagline": "Smart Academy ERP & Code Evaluation Sandbox",
        "category": "React + Python",
        "stack": ["React 19", "Python Flask", "PostgreSQL", "GitHub API", "Tailwind"],
        "problem": "Disjointed systems for tracking student git commits, PR evaluations, and mock interview readiness.",
        "outcome": "Built a unified operating system used daily across Karka academy for automated PR grading, live attendance, and career radar metrics.",
        "metrics": "🚀 250+ active daily users · 1,800+ PRs graded · Real-time stats",
        "badge": "Production Software"
    },
    {
        "id": "designsync",
        "name": "DesignSync Collaborative Studio",
        "tagline": "Real-time Multi-User Prototyping Canvas",
        "category": "UI/UX & Frontend",
        "stack": ["React", "TypeScript", "WebSockets", "Canvas API", "Figma API"],
        "problem": "Remote design sprint teams lacked seamless, low-latency live wireframe collaboration.",
        "outcome": "Engineered a browser-based vector canvas with multi-cursor multiplayer synchronization and instant CSS token export.",
        "metrics": "✨ 60 FPS smooth canvas · <20ms WebSocket latency · 1-click export",
        "badge": "Product Engineering"
    },
]

PLACEMENT_STORIES = [
    {
        "name": "Gabriel Samraj",
        "role": "Frontend Developer",
        "company": "Tech Innovators Lab",
        "hike": "+180% First Tech Role",
        "before": "Non-coding background, zero practical portfolio",
        "journey": "Karka UI/UX & Frontend Track → 4 Production Projects → Direct Placement",
        "proof": "Shipped 3 production React web apps with custom design systems",
        "quote": "Karka was an absolute game-changer. The instructors are passionate, the code reviews are intense, and the curriculum is 100% updated with real design trends.",
        "avatar": "GS",
        "tone": "plum"
    },
    {
        "name": "Ananya Krishnan",
        "role": "Gen AI & LLM Engineer",
        "company": "CloudMatrix AI",
        "hike": "+260% Salary Hike (8.2 LPA)",
        "before": "B.Sc Physics graduate with zero prior programming experience",
        "journey": "Python Foundations → Prompt Engineering → LangChain → Vector RAG → Hired",
        "proof": "Built an autonomous enterprise document assistant handling 10,000+ docs",
        "quote": "I walked into Karka having never written a single line of code. Within 5 months, I deployed an autonomous document QA agent and secured an 8.2 LPA offer!",
        "avatar": "AK",
        "tone": "violet"
    },
    {
        "name": "Karthik V.",
        "role": "Fullstack Developer",
        "company": "FinFlow Technologies",
        "hike": "+220% Career Jump (7.5 LPA)",
        "before": "Mechanical engineering graduate working odd non-tech jobs",
        "journey": "Web Fundamentals → FastAPI APIs → React SPA → Pay After Placement",
        "proof": "Architected a real-time financial ledger & webhook retry queue",
        "quote": "Pay After Placement gave me the courage to bet on myself without placing any financial burden on my parents. The mentorship here is unmatched in South India.",
        "avatar": "KV",
        "tone": "orange"
    },
    {
        "name": "Praveen Kumar",
        "role": "MERN Stack Developer",
        "company": "Nexus Systems",
        "hike": "+195% First Job (6.5 LPA)",
        "before": "College fresher rejected by 40+ campus placement drives",
        "journey": "Modern JavaScript → Node.js → Express → MongoDB → 30 Mock Interviews",
        "proof": "Engineered a collaborative task manager with WebSockets",
        "quote": "The 4-pillar interview prep transformed how I speak in tech interviews. Instead of reciting definitions, I walked interviewers through my GitHub code!",
        "avatar": "PK",
        "tone": "yellow"
    },
    {
        "name": "Sneha Raj",
        "role": "Product UI/UX Designer",
        "company": "Studio Crafted",
        "hike": "+240% Hike (7.8 LPA)",
        "before": "Freelance graphic designer stuck in low-paying print design",
        "journey": "Design Thinking → Figma Design Systems → Usability Testing → Portfolio Launch",
        "proof": "Published full SaaS redesign case study with interactive prototypes",
        "quote": "At Karka, you don't just design pretty mockups. You learn how engineers implement designs, which made my portfolio stand out from hundreds of applicants.",
        "avatar": "SR",
        "tone": "pink"
    },
    {
        "name": "Dinesh R.",
        "role": "Fullstack Intern → Associate Engineer",
        "company": "CodeSprint Global",
        "hike": "PPO Secured (6.0 LPA)",
        "before": "Final-year college student looking for real corporate internship",
        "journey": "Live Client Sprint → Git PR Reviews → Dockerization → Full-time PPO",
        "proof": "Authored and merged 16 production pull requests to client codebase",
        "quote": "The internship felt like working at a real high-growth startup from day one. Daily standups, code reviews, and shipping live features got me a PPO before graduation!",
        "avatar": "DR",
        "tone": "cyan"
    },
]

HIRING_PARTNERS = [
    {"name": "Zoho", "tier": "Enterprise SaaS", "badge": "Product Leader"},
    {"name": "Freshworks", "tier": "Global CRM", "badge": "Cloud Giant"},
    {"name": "Swiggy", "tier": "Consumer Tech", "badge": "Scale Platform"},
    {"name": "Cognizant", "tier": "Digital Transformation", "badge": "Global IT"},
    {"name": "Kaar Tech", "tier": "Enterprise Cloud", "badge": "Tech Partner"},
    {"name": "TCS", "tier": "Consulting & Services", "badge": "Global Scale"},
    {"name": "FinFlow", "tier": "FinTech Startup", "badge": "Fast Growth"},
    {"name": "NextLab AI", "tier": "GenAI Venture", "badge": "AI First"},
]

INSTA_REELS = [
    {
        "id": "reel1",
        "title": "Appraisal meeting: skills beat luck",
        "views": "1.1M",
        "likes": "43K",
        "category": "Career mindset",
        "hook": "A playful take on appraisal season, with a reminder that skills shape your next move.",
        "tag": "Career mindset",
        "thumbnail": "img/reels/appraisal.jpg",
        "instagram_url": "https://www.instagram.com/karka.ai/reel/DSKfwHJDIUT/"
    },
    {
        "id": "reel2",
        "title": "When you think your team lead isn't watching",
        "views": "17.8K",
        "likes": "163",
        "category": "Office humor",
        "hook": "A familiar workplace moment from Karka's Reel about trying to slack off unnoticed.",
        "tag": "Office life",
        "thumbnail": "img/reels/office-humor.jpg",
        "instagram_url": "https://www.instagram.com/karka.ai/reel/DdwAyPno6t7/"
    },
    {
        "id": "reel3",
        "title": "Data Analytics meets AI",
        "views": "1,029",
        "likes": "11",
        "category": "Data + AI",
        "hook": "A course overview covering Excel, Power BI, Python, AI tools, and hands-on datasets.",
        "tag": "Course spotlight",
        "thumbnail": "img/reels/data-ai.jpg",
        "instagram_url": "https://www.instagram.com/karka.ai/reel/DdoQxfqjXg_/"
    },
    {
        "id": "reel4",
        "title": "Will AI replace developers?",
        "views": "1,208",
        "likes": "20",
        "category": "AI + careers",
        "hook": "Karka's take: understanding users, architecture, and problem-solving still matters.",
        "tag": "Tech perspective",
        "thumbnail": "img/reels/ai-developers.jpg",
        "instagram_url": "https://www.instagram.com/karka.ai/reel/DdWSkLsiORk/"
    },
]

PAP_DATA = {
    "upfront": "₹0",
    "threshold_salary": "₹3,50,000",
    "threshold_label": "₹3.5 LPA",
    "payment_rule": "Pay only after you secure a qualifying tech job",
    "zero_risk_rule": "If you don't get placed above the threshold, you pay ₹0 tuition fee.",
    "perks": [
        "₹0 upfront tuition — zero financial risk to get started",
        "We succeed only when you succeed — our incentives are 100% aligned",
        "1-on-1 career coaching, ATS resume crafting & unlimited mock interviews",
        "Work on live client deliverables that blow away traditional fresher resumes",
        "Transparent program agreement with clear, learner-friendly terms"
    ]
}

FAQS = [
    ("What is Pay After Placement (PAP) and how does it work?", "Pay After Placement is Karka's signature model designed to eliminate financial barriers. You pay ₹0 upfront tuition when you enroll. You only begin paying your course fees in affordable installments after you secure a qualifying tech role with a package at or above the program threshold (typically ₹3.5+ LPA). If you don't land a qualifying job, you owe ₹0 tuition."),
    ("Do I need a Computer Science degree or previous coding background?", "No! Over 60% of our most successful graduates transitioned from Non-CSE backgrounds including Mechanical, Civil, Commerce, Arts, and Science. Our curriculum starts from absolute fundamentals and systematically builds you into a confident, production-grade builder."),
    ("Is a job placement guaranteed?", "While no ethical institution can legally promise an unconditional guarantee, Karka's entire business model is built on your employment success. Because we only earn tuition when you get hired, our dedicated placement cell, corporate hiring network, and 4-pillar interview coaching work tirelessly until you land your offer."),
    ("How long are the programs and what is the daily time commitment?", "Programs range from 3 to 6 months (180 days). We offer both full-time immersive tracks (6–8 hours daily with onsite mentor guidance at our Nagercoil academy) and flexible hybrid options designed for working professionals and final-year college students."),
    ("Will I work on real client projects or just toy tutorial clones?", "At Karka, you will never build generic to-do apps or tutorial clones. You will contribute to live client deliverables, open-source repositories, and production systems under senior engineer supervision with genuine Git pull requests and CI/CD pipelines."),
    ("Where is Karka Academy located and how do I visit?", "Our physical academy campus is located in Nagercoil, Tamil Nadu, equipped with high-speed development workstations, collaborative sprint pods, and mentor lounges. You can also connect with us via call, WhatsApp (+91 93455 80857), or Instagram @karka.ai.")
]

CAREER_SIMULATOR = [
    {
        "day": "DAY 01",
        "title": "Orientation & Mentor Mapping",
        "skills": ["Development environment setup", "Git & GitHub mastery", "Goal setting & milestone roadmap", "Peer study squad formation"],
        "milestone": "First GitHub PR merged"
    },
    {
        "day": "WEEK 04",
        "title": "Core Engineering Foundations",
        "skills": ["Clean code principles", "Data structures in practice", "Algorithmic thinking", "Interactive UI component architecture"],
        "milestone": "First interactive web application shipped"
    },
    {
        "day": "WEEK 08",
        "title": "Fullstack Architecture & APIs",
        "skills": ["RESTful API design", "PostgreSQL database modeling", "State management & Auth flows", "Containerization with Docker"],
        "milestone": "Fullstack CRUD system deployed live to cloud"
    },
    {
        "day": "WEEK 12",
        "title": "AI Multiplier & Vector Systems",
        "skills": ["Prompt engineering patterns", "LangChain & RAG pipelines", "Vector DB embeddings", "AI Copilot development"],
        "milestone": "Autonomous AI agent solving domain problem"
    },
    {
        "day": "WEEK 16",
        "title": "Live Client Internship Sprint",
        "skills": ["Real client deliverable execution", "Daily agile standups & sprint reviews", "System performance tuning", "Production error monitoring"],
        "milestone": "Production code deployed to live users"
    },
    {
        "day": "WEEK 20",
        "title": "Portfolio & ATS Resume Polish",
        "skills": ["High-impact project storytelling", "ATS-optimized resume crafting", "LinkedIn & GitHub personal brand", "Technical case study publication"],
        "milestone": "Interview-ready portfolio evaluated by tech leads"
    },
    {
        "day": "WEEK 24",
        "title": "Hiring Pipeline & Mock Interviews",
        "skills": ["50+ live mock technical interviews", "Salary negotiation coaching", "Direct referrals to hiring partners", "Offer evaluation & onboarding"],
        "milestone": "First offer letter signed & celebrated!"
    },
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_table_columns(table_name, columns):
    with get_db() as conn:
        existing = [row[1] for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()]
        for column_name, column_type in columns:
            if column_name not in existing:
                conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
        conn.commit()


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                track TEXT,
                goal TEXT,
                current_education TEXT,
                area_of_interest TEXT,
                preferred_program TEXT,
                message TEXT,
                created_at TEXT NOT NULL
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS discovery (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                selected_path TEXT,
                current_level TEXT,
                goal TEXT,
                journey TEXT,
                created_at TEXT NOT NULL
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS enquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT,
                area_of_interest TEXT,
                preferred_program TEXT,
                message TEXT,
                created_at TEXT NOT NULL
            )
        """
        )
        conn.commit()

    ensure_table_columns("leads", [("current_education", "TEXT"), ("area_of_interest", "TEXT"), ("preferred_program", "TEXT"), ("message", "TEXT")])
    ensure_table_columns("enquiries", [("current_education", "TEXT"), ("area_of_interest", "TEXT"), ("preferred_program", "TEXT"), ("message", "TEXT")])


init_db()


def local_ai_reply(message: str) -> str:
    question = message.casefold()
    if any(term in question for term in ("pay", "fee", "tuition", "pap", "cost", "afford")):
        return (
            "Karka operates on a zero-upfront Pay After Placement (PAP) model! You invest ₹0 during your 180 days of "
            "training. You only start paying tuition in comfortable installments after securing a tech role above the "
            "threshold (₹3.5+ LPA). If you don't land a qualifying job, you owe ₹0 tuition."
        )
    if any(term in question for term in ("intern", "project", "portfolio", "client", "omniagent", "pulsepay")):
        return (
            "At Karka, you build real client deliverables instead of toy tutorials! Flagship projects include OmniAgent AI "
            "(multi-modal autonomous RAG agent), PulsePay (high-throughput FinTech reconciliation engine), and DesignSync. "
            "Our Full Stack Developer Internship features daily agile standups, PR code reviews, and live production deployments."
        )
    if any(term in question for term in ("track", "course", "program", "stack", "learn", "react", "python", "genai", "ai", "uiux")):
        return (
            "We offer 6 industry-demanded career tracks: 1) React + Python Fullstack, 2) MERN Fullstack, 3) Gen AI & LLM Engineering, "
            "4) AI & Data Science, 5) UI/UX Product Design, and 6) Full Stack Developer Internship. Each track runs for 180 days with "
            "1-on-1 mentorship, live projects, and placement assistance."
        )
    if any(term in question for term in ("beginner", "background", "cse", "mechanical", "arts", "experience", "fresher")):
        return (
            "Over 60% of our placed learners come from Non-CSE backgrounds (Mechanical, Civil, B.Com, Arts, etc.). Our curriculum "
            "starts with absolute fundamentals and builds systematically into production-ready software engineering. No previous "
            "coding experience is required!"
        )
    if any(term in question for term in ("placement", "hike", "salary", "jobs", "hiring", "company", "companies")):
        return (
            "Our learners land roles as Fullstack Engineers, Gen AI Developers, and UI/UX Designers with salaries ranging from "
            "₹4.2L to ₹14.5L PA (average 3.2x salary jump). Hiring partners include Zoho, Freshworks, Swiggy, Cognizant, TCS, and "
            "fast-scaling GenAI & FinTech startups."
        )
    if any(term in question for term in ("contact", "phone", "call", "address", "where", "nagercoil", "location")):
        return f"Karka AI & Tech Academy is located in Nagercoil, Tamil Nadu. Reach us directly at {SITE['phone']}, email {SITE['email']}, or DM us on Instagram {SITE['instagram']}!"
    return (
        "Hey builder! I'm Karka's AI Career Concierge. Ask me anything about our 6 career tracks, zero-upfront Pay After Placement, "
        "real client internship projects, or campus life in Nagercoil. How can I accelerate your tech career today?"
    )


def ai_reply(message: str) -> tuple[str, str]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or Groq is None:
        return local_ai_reply(message), "guide"

    client = Groq(api_key=api_key)
    system = """You are Karka Academy's high-energy, motivational, Gen-Z friendly AI Career Concierge. """
    system += """Karka AI & Tech Academy is located in Nagercoil, Tamil Nadu (Instagram: @karka.ai). """
    system += """Tone: Confident, encouraging, motivational, clear, punchy, Gen-Z tech-builder vibe. """
    system += """Key verified facts: """
    system += """1. Pay After Placement (PAP): ₹0 upfront tuition. Learners only pay after landing a tech job >= ₹3.5 LPA. If not placed, ₹0 tuition. """
    system += """2. Career Tracks: React + Python Fullstack, MERN Fullstack, Gen AI & LLM Developer, AI & Data Science, UI/UX Design, and Full Stack Developer Internship (180 days). """
    system += """3. Real Projects: OmniAgent AI (autonomous enterprise RAG), PulsePay (FinTech ledger), Karka Campus OS, DesignSync Studio. Real client PRs, not toy clones. """
    system += """4. 4-Pillar Engine: Business Communication, Modern App Building, AI Multiplier Skills, and Interview Mastery (ATS profile, 50+ mock interviews). """
    system += """5. Open to beginners & non-CSE backgrounds (Mechanical, Civil, B.Com, Freshers). """
    system += """Keep answers concise (under 3 sentences), highly actionable, and always encourage taking the 60s quiz or applying.\n\n"""
    system += "User asks: " + message
    try:
        result = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role": "system", "content": system}],
            temperature=0.4,
            max_completion_tokens=220,
        )
        return result.choices[0].message.content.strip(), "ai"
    except Exception as exc:
        app.logger.warning("Groq request failed; using the Karka guide (%s)", type(exc).__name__)
        return local_ai_reply(message), "guide"


@app.context_processor
def inject_globals():
    return {
        "site": SITE,
        "tracks": TRACKS,
        "pillars": PILLARS,
        "personas": PERSONAS,
        "simulator": CAREER_SIMULATOR,
        "projects": PROJECTS,
        "stories": PLACEMENT_STORIES,
        "hiring_partners": HIRING_PARTNERS,
        "insta_reels": INSTA_REELS,
        "pap_data": PAP_DATA,
        "year": datetime.now().year,
    }


@app.route("/")
def home():
    return render_template(
        "index.html",
        stories=PLACEMENT_STORIES,
        faqs=FAQS,
        timeline=DISCOVERY_STEPS,
    )


@app.route("/apply", methods=["GET", "POST"])
def apply():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        current_education = request.form.get("current_education", "").strip()
        area_of_interest = request.form.get("area_of_interest", "").strip()
        preferred_program = request.form.get("preferred_program", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not phone:
            flash("Name and phone are required.", "error")
            return render_template("apply.html", selected_track=preferred_program)

        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO leads 
                (name, phone, email, current_education, area_of_interest, preferred_program, message, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    phone,
                    email,
                    current_education,
                    area_of_interest,
                    preferred_program,
                    message,
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )
            conn.commit()
        return redirect(url_for("success"))

    return render_template("apply.html", selected_track=request.args.get("track", ""))


@app.route("/success")
def success():
    return render_template("success.html")


@app.post("/api/assistant")
def assistant():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"answer": "Tell me what you're exploring — tracks, internships, projects or admissions."}), 400
    if len(message) > 800:
        return jsonify({"answer": "Please keep your question under 800 characters."}), 400
    answer, mode = ai_reply(message)
    return jsonify({"answer": answer, "mode": mode})


@app.post("/api/lead")
def lead_api():
    payload = request.get_json(silent=True) or {}
    name = str(payload.get("name", "")).strip()
    phone = str(payload.get("phone", "")).strip()
    email = str(payload.get("email", "")).strip()
    current_education = str(payload.get("current_education", "")).strip()
    area_of_interest = str(payload.get("area_of_interest", "")).strip()
    preferred_program = str(payload.get("preferred_program", "")).strip()
    message = str(payload.get("message", "")).strip()

    if not name or not phone:
        return jsonify({"ok": False, "message": "Name and phone are required."}), 400

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO enquiries (name, phone, email, current_education, area_of_interest, preferred_program, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                name,
                phone,
                email,
                current_education,
                area_of_interest,
                preferred_program,
                message,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()

    return jsonify({"ok": True, "message": "Application captured. The Karka team can follow up with you."})


@app.post("/api/discovery")
def career_discovery():
    payload = request.get_json(silent=True) or {}
    selected_path = str(payload.get("selected_path", "")).strip()
    current_level = str(payload.get("current_level", "")).strip()
    goal = str(payload.get("goal", "")).strip()
    journey = str(payload.get("journey", "")).strip()

    if not selected_path:
        return jsonify({"ok": False, "message": "Please select a path."}), 400

    with get_db() as conn:
        conn.execute(
            "INSERT INTO discovery (selected_path, current_level, goal, journey, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                selected_path,
                current_level,
                goal,
                journey,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        conn.commit()

    return jsonify({"ok": True, "message": "Your Karka path was saved."})


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
