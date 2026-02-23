# How to Use This Research Agent

A super simple guide. No tech experience needed.

---

## What Is This?

You ask a question → the agent searches the internet → it reads what it finds → it gives you a clean answer with links to where it got the info.

```
   YOU                        THE AGENT                    THE INTERNET

  "What causes               "Let me look             Searches Google
   rainbows?"  ──────────►    that up!"  ──────────►  Reads websites
                                                       Collects facts
                              "Here's what                   │
   You read a                  I found!"               ◄────┘
   neat answer  ◄──────────
```

---

## First-Time Setup (Do This Once)

### Step 1 — Install the brain

Open **Terminal** (search "Terminal" in the Start menu) and type:

```
npm install -g @anthropic-ai/claude-code
```

### Step 2 — Get your secret key

> This is like a password. It lets the agent talk to Claude.

1. Go to **https://console.anthropic.com/**
2. Sign up or log in
3. Click **"API Keys"**
4. Click **"Create Key"**
5. Copy it (looks like `sk-ant-abc123...`)

```
┌─────────────────────────────────────────┐
│                                         │
│  ⚠ Keep this key SECRET.               │
│    Never share it online.               │
│    Treat it like a password.            │
│                                         │
└─────────────────────────────────────────┘
```

### Step 3 — Save your key

Pick ONE of these:

**Option A** — Type this in Terminal:
```
set ANTHROPIC_API_KEY=sk-ant-paste-your-key-here
```

**Option B** — Use a file:
1. Find `.env.example` in the project folder
2. Copy it and rename the copy to `.env`
3. Open `.env` in Notepad
4. Replace `your_api_key_here` with your real key
5. Save

### Step 4 — Install the tools

```
cd path\to\claude-agent
pip install -r requirements.txt
```

**Done! You only do Steps 1-4 once.**

---

## Using the Agent (Every Time)

### Open Terminal and type:

```
cd path\to\claude-agent
python main.py "your question here"
```

### Example:

```
python main.py "What causes the Northern Lights?"
```

### What you will see:

```
Research question: What causes the Northern Lights?

  >> Searching: Northern Lights aurora borealis cause
  >> Reading:   https://www.nasa.gov/aurora...
  >> Searching: solar wind magnetosphere explanation
  >> Reading:   https://science.org/articles/...

The Northern Lights (Aurora Borealis) are caused by
charged particles from the Sun hitting Earth's
magnetic field...

Sources:
- https://www.nasa.gov/aurora
- https://science.org/articles/aurora-explained

[Completed in 28.3s | Cost: $0.0621 | Turns: 6]
[Session: abc-123-def]
  (use --resume to continue this conversation)
```

---

## 5 Ways to Run It

```
┌───────────────────────────────────────────────────────────┐
│                                                           │
│  NORMAL       python main.py "question"                   │
│               ► Good for most questions                   │
│                                                           │
│  DEEP         python main.py --deep "question"            │
│               ► Extra thorough — reads more sources       │
│                                                           │
│  SAVE         python main.py -o report.md "question"      │
│               ► Saves the answer to a file                │
│                                                           │
│  QUIET        python main.py -q "question"                │
│               ► Shows only the answer, nothing else       │
│                                                           │
│  FOLLOW-UP    python main.py --resume ID "question"       │
│               ► Continue a previous conversation          │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

**You can combine them:**

```
python main.py --deep -o report.md "How do black holes form?"
                 │          │
                 │          └── saves answer to report.md
                 └── uses deep research mode
```

---

## Cheat Sheet

```
┌──────────────────────────────────────────┐
│                                          │
│   Every time you want to use it:         │
│                                          │
│   1. Open Terminal                        │
│   2. cd path\to\claude-agent     │
│   3. python main.py "your question"      │
│                                          │
│   That's it. Three steps.                │
│                                          │
└──────────────────────────────────────────┘
```

---

## Something Not Working?

| What you see | What it means | What to do |
|---|---|---|
| "CLI not found" | The brain isn't installed | Run `npm install -g @anthropic-ai/claude-code` |
| "API key" error | Your key is missing | Set it with `set ANTHROPIC_API_KEY=your_key` |
| "No module named..." | Tools aren't installed | Run `pip install -r requirements.txt` |
| "Cannot launch inside Claude Code" | Wrong terminal | Open a regular Terminal, not Claude Code |
