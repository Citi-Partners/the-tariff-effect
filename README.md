# The Tariff Effect - Complete Beginner Starter Kit 🚀

**Welcome!** This starter kit will help you build your automated tariff tracking website - NO prior coding experience needed.

## 📋 What You'll Build

A website that:
- ✅ Automatically fetches tariff news every day
- ✅ Uses AI to translate policy → family budget impact
- ✅ Updates your site automatically (no manual work!)
- ✅ Looks clean and professional
- ✅ Costs ~$30-50/month to run

## 🛠️ What You Need

Before starting, make sure you have:

- [x] Domain purchased (✓ You have theTariffEffect.com!)
- [x] Cloudflare account (✓ You're set up!)
- [ ] GitHub account (free) - [Sign up here](https://github.com/signup)
- [ ] Claude API key (free $5 credits) - [Get it here](https://console.anthropic.com)
- [ ] Python installed on your computer

---

## 🎯 Step-by-Step Setup Guide

### PART 1: Install Python (15 minutes)

**On Mac:**
1. Open Terminal (press Cmd+Space, type "terminal", press Enter)
2. Install Homebrew (copy this entire line and press Enter):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Python:
   ```bash
   brew install python
   ```
4. Verify it worked:
   ```bash
   python3 --version
   ```
   Should show: `Python 3.12.x` or similar

**On Windows:**
1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
2. Run the installer
3. ⚠️ **IMPORTANT:** Check the box that says "Add Python to PATH"
4. Click "Install Now"
5. Open Command Prompt and verify:
   ```bash
   python --version
   ```

---

### PART 2: Set Up Your Project (10 minutes)

**1. Create a GitHub account**
- Go to [github.com/signup](https://github.com/signup)
- Choose username, email, password
- Verify your email

**2. Create your repository**
- Click the "+" button in top right
- Click "New repository"
- Name it: `the-tariff-effect`
- ✅ Check "Add a README file"
- ✅ Choose "Public"
- Click "Create repository"

**3. Download GitHub Desktop (makes things easier)**
- Go to [desktop.github.com](https://desktop.github.com)
- Download and install
- Sign in with your GitHub account
- Click "Clone a repository"
- Select `the-tariff-effect`
- Choose where to save it on your computer (remember this location!)

---

### PART 3: Get Your Claude API Key (5 minutes)

**1. Sign up for Claude API**
- Go to [console.anthropic.com](https://console.anthropic.com)
- Click "Sign Up"
- Verify your email

**2. Get your API key**
- Click on your name (top right)
- Click "API Keys"
- Click "Create Key"
- **Copy the key and save it somewhere safe!**
  - It looks like: `sk-ant-api03-xxx...`
  - You'll only see it once!

---

### PART 4: Add the Starter Code (10 minutes)

**1. Download all the files from this starter kit**

You should have these files:
```
the-tariff-effect/
├── README.md (this file)
├── fetch_feeds.py
├── analyze_tariffs.py
├── generate_site.py
├── requirements.txt
├── index.html
├── styles.css
└── .github/
    └── workflows/
        └── daily-update.yml
```

**2. Copy them to your repository folder**
- Find where you cloned the repository (from Part 2, step 3)
- Copy all the files into that folder
- They should replace/merge with what's there

**3. Create a `.env` file for your API key**
- In your repository folder, create a new file called `.env`
- Add this line (replace with YOUR actual key):
  ```
  ANTHROPIC_API_KEY=sk-ant-api03-YOUR-KEY-HERE
  ```
- Save the file

⚠️ **IMPORTANT:** Never commit your `.env` file to GitHub! 
- Create another file called `.gitignore`
- Add this line: `.env`
- This keeps your API key private

---

### PART 5: Install Required Libraries (5 minutes)

**Open Terminal (Mac) or Command Prompt (Windows):**

1. Navigate to your project folder:
   ```bash
   cd path/to/the-tariff-effect
   ```
   (Replace `path/to/` with where you saved it)

2. Install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs:
   - `anthropic` (for Claude API)
   - `feedparser` (for reading RSS feeds)
   - `python-dotenv` (for loading your API key)
   - `requests` (for fetching web content)

---

### PART 6: Test It Locally (10 minutes)

**Let's make sure everything works before automating!**

**1. Fetch some tariff news:**
```bash
python fetch_feeds.py
```

You should see:
```
Fetching RSS feeds...
✓ Found 15 articles from USTR
✓ Found 22 articles from Reuters
...
Saved 87 articles to data/raw_articles.json
```

**2. Analyze with AI:**
```bash
python analyze_tariffs.py
```

You should see:
```
Analyzing articles with Claude AI...
Processing article 1/87...
✓ Consumer relevant: Steel tariffs → appliances +$50-80
Processing article 2/87...
✗ Not consumer relevant (technical trade policy)
...
Saved 23 relevant articles to data/analyzed_articles.json
```

**3. Generate the website:**
```bash
python generate_site.py
```

You should see:
```
Generating website...
✓ Created index.html
✓ Created category pages
✓ Updated styles.css
Site ready! Open index.html in your browser.
```

**4. View your site locally:**
- Find `index.html` in your project folder
- Double-click to open in your browser
- You should see your tariff tracker site!

---

### PART 7: Connect to Cloudflare Pages (15 minutes)

**1. Push your code to GitHub:**

In GitHub Desktop:
- You should see all your new files listed
- In the bottom left, type: "Initial commit - starter kit"
- Click "Commit to main"
- Click "Push origin" (top right)

**2. Set up Cloudflare Pages:**
- Log into Cloudflare dashboard
- Click "Workers & Pages" in left sidebar
- Click "Create application"
- Click "Pages" tab
- Click "Connect to Git"
- Choose "GitHub"
- Authorize Cloudflare to access GitHub
- Select your `the-tariff-effect` repository
- Click "Begin setup"

**3. Configure build settings:**
- Build command: `python generate_site.py`
- Build output directory: `/` (root)
- Click "Save and Deploy"

**4. Add your environment variable:**
- In Cloudflare Pages settings
- Go to "Settings" → "Environment variables"
- Click "Add variable"
- Name: `ANTHROPIC_API_KEY`
- Value: `sk-ant-api03-YOUR-KEY-HERE`
- Click "Save"

**5. Connect your domain:**
- In your Cloudflare Pages project
- Click "Custom domains"
- Click "Set up a custom domain"
- Enter: `thetariffeffect.com`
- Click "Activate domain"
- It should auto-configure (since you bought domain through Cloudflare!)

---

### PART 8: Set Up Daily Automation (10 minutes)

**Your site should now update automatically every day at 6am!**

How it works:
- GitHub Actions runs the workflow file (`.github/workflows/daily-update.yml`)
- It fetches new RSS feeds
- Analyzes them with Claude AI
- Generates updated HTML
- Pushes to GitHub
- Cloudflare auto-deploys the new version

**To verify automation is working:**
1. Go to your GitHub repository
2. Click the "Actions" tab
3. You should see scheduled workflows
4. First run happens tomorrow at 6am EST

**To test it now (don't wait until tomorrow):**
1. In your repository, click "Actions"
2. Click "Daily Tariff Update" workflow
3. Click "Run workflow" dropdown
4. Click the green "Run workflow" button
5. Watch it run in real-time!

---

## ✅ You're Done! 

Your site is now:
- ✅ Live at theTariffEffect.com
- ✅ Updating automatically every morning
- ✅ Processing tariff news with AI
- ✅ Translating policy → family impact

---

## 📊 What Happens Every Day (Automatically)

```
6:00 AM EST - GitHub Actions triggers
  ↓
6:01 AM - Fetch RSS feeds (15-20 sources)
  ↓
6:02 AM - Claude AI analyzes ~50-100 articles
  ↓
6:05 AM - Filters for consumer-relevant news (usually 5-15 articles)
  ↓
6:06 AM - Generates HTML pages
  ↓
6:07 AM - Pushes to GitHub
  ↓
6:08 AM - Cloudflare deploys new version
  ↓
6:09 AM - Your site is updated with today's tariff news!
```

---

## 💰 Monthly Costs

- Domain: $1.25/month (already paid annually)
- Cloudflare Pages: $0 (free tier)
- Claude API: $30-50/month (depending on article volume)
- GitHub: $0 (free tier)

**Total: $30-50/month**

---

## 🆘 Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"API key invalid" error:**
- Check your `.env` file
- Make sure the key starts with `sk-ant-api03-`
- Make sure there are no spaces or quotes around it

**"No articles found" error:**
- RSS feeds might be temporarily down
- Check your internet connection
- Try running again in 10 minutes

**Site not updating:**
- Check GitHub Actions tab for errors
- Make sure environment variable is set in Cloudflare
- Check that daily workflow is enabled

**Need help?**
- Check the error message carefully
- Google the exact error message
- Most Python errors have clear solutions online!

---

## 🚀 Next Steps (After You're Running)

**Week 1: Monitor and tweak**
- Check the site daily
- See which articles are being caught
- Adjust the AI prompts if needed (in `analyze_tariffs.py`)

**Week 2: Add features**
- Family budget calculator
- Email newsletter signup
- Social media share buttons

**Week 3: Start promoting**
- Share on Twitter, LinkedIn
- Post in relevant Reddit communities
- Reach out to personal finance bloggers

**Week 4: Monetization setup**
- Add Google Analytics
- Set up Google AdSense
- Create first affiliate partnerships

---

## 📝 File Descriptions

**What each file does:**

- `fetch_feeds.py` - Downloads tariff news from RSS feeds
- `analyze_tariffs.py` - Uses Claude AI to analyze articles
- `generate_site.py` - Creates the HTML pages
- `requirements.txt` - List of Python libraries needed
- `index.html` - Your homepage template
- `styles.css` - Makes your site look good
- `.github/workflows/daily-update.yml` - Automation schedule
- `README.md` - This guide!

---

## 🎓 Learning Resources (Optional)

Want to understand the code better?

**Python basics:**
- [Python for Beginners](https://www.python.org/about/gettingstarted/) (free)
- [Codecademy Python Course](https://www.codecademy.com/learn/learn-python-3) (free)

**RSS feeds:**
- [What is RSS?](https://en.wikipedia.org/wiki/RSS) (2 min read)

**APIs:**
- [What is an API?](https://www.freecodecamp.org/news/what-is-an-api-in-english-please-b880a3214a82/) (5 min read)

**GitHub:**
- [GitHub Hello World](https://guides.github.com/activities/hello-world/) (10 min tutorial)

---

## ✨ You Got This!

Remember: 
- The code is already written for you
- Everything is copy-paste-and-run
- Errors are normal (and Google-able!)
- Your site will be live in ~1 hour of work

**Let's build this!** 🚀
