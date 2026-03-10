# ⚡ QUICK START GUIDE
**Get your tariff tracker running in 60 minutes**

## 🎯 Your Checklist (tick these off as you go!)

### Part 1: Setup (20 minutes)
- [ ] Install Python
- [ ] Create GitHub account
- [ ] Download GitHub Desktop
- [ ] Clone your repository
- [ ] Get Claude API key

### Part 2: Configure (10 minutes)
- [ ] Copy all starter kit files to your repo folder
- [ ] Create `.env` file with your API key
- [ ] Install Python libraries: `pip install -r requirements.txt`

### Part 3: Test Locally (15 minutes)
- [ ] Run: `python fetch_feeds.py`
- [ ] Run: `python analyze_tariffs.py`
- [ ] Run: `python generate_site.py`
- [ ] Open `index.html` in browser - does it look good?

### Part 4: Deploy (15 minutes)
- [ ] Push code to GitHub using GitHub Desktop
- [ ] Connect Cloudflare Pages to GitHub
- [ ] Add API key as environment variable in Cloudflare
- [ ] Point theTariffEffect.com to Cloudflare Pages
- [ ] Visit your live site!

---

## 🆘 If Something Breaks

**"Module not found":**
```bash
pip install -r requirements.txt
```

**"API key not found":**
- Check that `.env` file exists in your project folder
- Open it and make sure it has: `ANTHROPIC_API_KEY=sk-ant-...`
- No spaces, no quotes

**"No articles found":**
- This is normal if there's no tariff news today
- Try running again tomorrow
- Or manually add test data to `data/raw_articles.json`

**Site not deploying:**
- Check GitHub - did your code upload?
- Check Cloudflare Pages - any errors in build log?
- Make sure you added the API key to Cloudflare environment variables

---

## 📞 Next Steps After Launch

**Day 1-7:**
- Monitor the automation (check GitHub Actions tab)
- Tweak the AI prompts if needed
- Share on social media

**Week 2:**
- Add email signup
- Create first email newsletter
- Start building subscriber list

**Week 3:**
- Add Google Analytics
- Set up Google AdSense
- Track which articles get most views

**Month 2:**
- Reach out to affiliate partners
- Create premium content
- Consider adding a budget calculator tool

---

## 💡 Pro Tips

1. **The site updates at 6am daily** - Check it each morning for the first week to make sure it's working

2. **Not every day has news** - Some days will have 0 relevant articles. That's normal!

3. **Start promoting early** - Don't wait for "perfect." Share on Twitter/LinkedIn now.

4. **Engage with your audience** - Reply to comments, answer questions, build community

5. **Track your costs** - Monitor Claude API usage in console.anthropic.com

---

## ✅ You're Ready!

Open the full README.md for detailed step-by-step instructions.

Let's build this! 🚀
