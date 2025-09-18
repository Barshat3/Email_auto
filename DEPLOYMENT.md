# Render Deployment Guide

## Prerequisites
1. GitHub account
2. Render account (free at render.com)
3. Your code pushed to GitHub

## Step 1: Prepare Your Code

Your app is now ready with:
- ✅ `requirements.txt` - Python dependencies
- ✅ `Procfile` - Tells Render how to run your app
- ✅ Updated `app.py` - Production-ready configuration
- ✅ `.gitignore` - Excludes unnecessary files

## Step 2: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Bulk Email Sender"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

1. **Sign up/Login** at [render.com](https://render.com)

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service**
   - **Name**: `bulk-email-sender` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

4. **Environment Variables**
   - Click "Environment" tab
   - Add: `FLASK_SECRET_KEY` = `your-random-secret-key-here`
   - Add: `FLASK_ENV` = `production`

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your app will be available at `https://your-app-name.onrender.com`

## Step 4: Test Your Deployment

1. Visit your Render URL
2. Test login with your Gmail
3. Upload a test CSV and send emails
4. Verify live progress tracking works

## Important Notes

### Free Tier Limitations:
- **Sleep**: App sleeps after 15 minutes of inactivity
- **Wake time**: ~30 seconds to wake up
- **Monthly hours**: 750 hours (31 days = 744 hours)
- **Perfect for**: Personal use with occasional sending

### Gmail Setup:
- Users still need Gmail App Passwords
- Share the Render URL with your 3-4 users
- Each user logs in with their own Gmail

### Monitoring:
- Check Render dashboard for logs
- Monitor usage in the dashboard
- Set up alerts if needed

## Troubleshooting

### Common Issues:

1. **App won't start**
   - Check build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`

2. **Environment variables not working**
   - Verify variables are set in Render dashboard
   - Restart the service after adding variables

3. **File upload issues**
   - Check file size limits (10MB max)
   - Verify file types are supported

4. **SSE not working**
   - Some proxies may buffer SSE
   - Check browser console for errors

### Getting Help:
- Render docs: https://render.com/docs
- Check service logs in Render dashboard
- Test locally first: `python app.py`

## Cost
- **Free tier**: 750 hours/month
- **Your usage**: ~24 hours/day × 31 days = 744 hours
- **Result**: Completely free for your use case!

## Next Steps
1. Deploy to Render
2. Test with your team
3. Share the URL
4. Monitor usage
5. Consider upgrading if you need more hours

---

**Success!** Your bulk email sender is now deployed and ready for your team to use.