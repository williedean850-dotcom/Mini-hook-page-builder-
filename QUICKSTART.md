# 🎣 Hook Page Builder - Simple Setup

## What It Does (In Plain English)

1. **You enter:**
   - Your affiliate link
   - An image URL
   - A short description

2. **AI does the work:**
   - Writes a catchy headline for you

3. **You get:**
   - A beautiful landing page
   - People enter their email
   - They get redirected to your affiliate link
   - You keep their emails for later

---

## Quick Setup (5 Minutes)

### Step 1: Get OpenAI API Key (Free)
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key

### Step 2: Add Key to Backend
1. Open `backend/.env`
2. Replace `your_api_key_here` with your actual key
3. Save

### Step 3: Start Backend
```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```

You'll see: `🚀 Hook Page Builder Backend Running on http://localhost:5000`

### Step 4: Start Frontend (New Terminal)
```bash
cd frontend
npm install
npm start
```

It will open in your browser automatically.

---

## How to Use

### Create a Hook Page:

1. Click **Create New** button
2. Fill in:
   - **Affiliate Link:** Your referral URL
   - **Image URL:** Link to an image (jpg/png)
   - **Description:** What are you promoting?
3. Click **Generate Hook** (AI writes the title)
4. Click **Create Page**
5. Copy the link and share on social media!

### What Happens:

**Visitor sees:**
- Your image
- AI-generated headline
- Description
- Email field + "Get Access" button

**When they enter email:**
- Email saved to your dashboard
- Redirected to your affiliate link
- If they buy within 60 days = you get paid!

---

## Where Your Emails Are

- Dashboard shows all captured emails
- View how many per page
- Download later to send follow-ups

---

## Troubleshooting

**"Backend not running"**
- Make sure you ran `python app.py` in backend folder

**"Page won't load"**
- Both backend and frontend must be running
- Backend: http://localhost:5000
- Frontend: http://localhost:3000

**"AI not generating titles"**
- Check your OpenAI API key is correct in `.env`

---

## Questions?

Just ask! This is meant to be simple and work for you. 🚀
