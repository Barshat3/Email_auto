# Railway Deployment Guide

## Why Railway?
- ✅ **SMTP connections allowed** on free tier
- ✅ **$5 credit monthly** (enough for small apps)
- ✅ **Easy deployment** from GitHub
- ✅ **No code changes needed**
- ✅ **Better than Render** for your use case

## Step 1: Prepare Your Code

Your app is already ready! The files you need:
- ✅ `app.py` - Main Flask application
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Railway how to run the app
- ✅ `gunicorn.conf.py` - Gunicorn configuration
- ✅ `templates/` - HTML templates

## Step 2: Deploy to Railway

1. **Go to Railway**:
   - Visit [railway.app](https://railway.app)
   - Click **"Start a New Project"**

2. **Connect GitHub**:
   - Click **"Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub
   - Select your **Email_auto** repository

3. **Configure Deployment**:
   - Railway will auto-detect it's a Python app
   - It will use your `requirements.txt` and `Procfile`
   - No additional configuration needed!

4. **Add Environment Variables**:
   - Go to your project dashboard
   - Click **"Variables"** tab
   - Add: `FLASK_SECRET_KEY` = `your-random-secret-key-here`
   - Add: `FLASK_ENV` = `production`

5. **Deploy**:
   - Railway will automatically build and deploy
   - Wait 2-3 minutes for deployment
   - You'll get a URL like: `https://your-app.railway.app`

## Step 3: Test Your App

1. **Visit your Railway URL**
2. **Login** with your Gmail address
3. **Enter your Gmail App Password** (16 characters)
4. **Upload a small CSV** (3-5 recipients)
5. **Send emails** - should work perfectly!

## Step 4: Share with Your Team

1. **Share the Railway URL** with your 3-4 users
2. **Each user needs**:
   - Their own Gmail address
   - Their own Gmail App Password
   - No account setup required!

## Gmail App Password Setup

Each user needs to create a Gmail App Password:

1. **Go to Google Account** → **Security**
2. **Enable 2-Step Verification** (if not already)
3. **Go to App Passwords**
4. **Generate** a new password for "Mail"
5. **Use this 16-character password** (not your regular Gmail password)

## Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| SMTP Support | ✅ Yes | ❌ No (free tier) |
| Free Tier | $5 credit/month | 750 hours/month |
| Deployment | Easy | Easy |
| Your App | ✅ Works | ❌ Blocked |

## Monitoring Usage

1. **Check Railway Dashboard**:
   - View logs in real-time
   - Monitor resource usage
   - See deployment status

2. **Usage Limits**:
   - $5 credit monthly
   - Your app will use ~$2-3/month
   - Plenty of headroom for growth

## Troubleshooting

### "Network is unreachable" Error:
- This shouldn't happen on Railway
- Check your Gmail App Password
- Verify 2-Step Verification is enabled

### "Authentication failed" Error:
- Use Gmail App Password, not regular password
- Check the password is 16 characters
- Ensure 2-Step Verification is enabled

### App won't start:
- Check Railway logs in dashboard
- Verify environment variables are set
- Ensure all files are pushed to GitHub

## Cost Summary

- **Railway**: $0-3/month (within $5 credit)
- **Gmail**: Free (with App Password)
- **Total**: **Essentially FREE** for your use case!

## Next Steps

1. **Deploy to Railway** (follow steps above)
2. **Test with small CSV** (3-5 recipients)
3. **Share URL with team**
4. **Monitor usage** in Railway dashboard

---

**Ready to deploy?** Your code is already prepared for Railway!