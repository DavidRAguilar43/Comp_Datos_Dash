# 🚀 Quick Start - Deployment Guide

This project is ready to deploy to **Vercel** (frontend) and **Railway** (backend) using their free tiers!

## 📁 Deployment Files Overview

This repository includes all necessary configuration files for deployment:

### Backend (Railway)
- `backend/Procfile` - Tells Railway how to start the server
- `backend/railway.json` - Railway-specific configuration
- `backend/runtime.txt` - Specifies Python version
- `backend/.env.example` - Template for environment variables
- `backend/requirements.txt` - Python dependencies

### Frontend (Vercel)
- `frontend/vercel.json` - Vercel-specific configuration
- `frontend/.env.example` - Template for environment variables
- `frontend/package.json` - Node.js dependencies

### Documentation
- `DEPLOYMENT.md` - **Complete step-by-step deployment guide** ⭐
- `DEPLOYMENT_CHECKLIST.md` - Checklist to track your progress
- `.gitignore` - Ensures sensitive files are never committed

## 🎯 Quick Deployment Steps

### 1️⃣ Prerequisites (5 minutes)
- Create accounts on:
  - [GitHub](https://github.com) (for code hosting)
  - [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (free database)
  - [Railway](https://railway.app) (free backend hosting)
  - [Vercel](https://vercel.com) (free frontend hosting)
  - [OpenAI](https://platform.openai.com) (for AI features)

### 2️⃣ Setup Database (10 minutes)
1. Create a free MongoDB Atlas cluster
2. Get your connection string
3. Save it securely

### 3️⃣ Deploy Backend (10 minutes)
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Set environment variables in Railway
4. Deploy!

### 4️⃣ Deploy Frontend (5 minutes)
1. Connect Vercel to your GitHub repo
2. Set backend URL in Vercel environment variables
3. Deploy!

### 5️⃣ Final Configuration (5 minutes)
1. Update CORS settings in Railway with your Vercel URL
2. Test the application
3. Done! 🎉

**Total Time: ~35 minutes**

## 📖 Detailed Instructions

For complete step-by-step instructions with screenshots and troubleshooting:

👉 **[Read the Full Deployment Guide](./DEPLOYMENT.md)** 👈

## ✅ Deployment Checklist

Track your progress using the checklist:

👉 **[Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)** 👈

## 🔐 Security Notes

✅ **Already configured for you:**
- `.gitignore` blocks all `.env` files
- `.env.example` files show required variables (no secrets)
- CORS configured for security
- HTTPS enforced on both platforms

⚠️ **Important:**
- Never commit `.env` files
- Keep API keys secure
- Use strong passwords for MongoDB

## 💰 Cost Breakdown

### Free Tier Limits
- **Vercel**: 100 GB bandwidth/month (plenty for most use cases)
- **Railway**: $5 credit/month (backend sleeps after 30 min inactivity)
- **MongoDB Atlas**: 512 MB storage (sufficient for testing/small datasets)
- **OpenAI**: Pay-per-use (set limits in dashboard)

**Expected Monthly Cost**: $0-5 for light usage

## 🆘 Need Help?

1. **Check the troubleshooting section** in [DEPLOYMENT.md](./DEPLOYMENT.md)
2. **Review logs**:
   - Railway: Dashboard → Service → Deployments → View Logs
   - Vercel: Dashboard → Project → Deployments → Function Logs
3. **Common issues**:
   - CORS errors → Update `CORS_ORIGINS` in Railway
   - Build failures → Check logs for missing dependencies
   - Connection errors → Verify environment variables

## 🎓 What You'll Learn

By deploying this project, you'll gain experience with:
- ✅ Git and GitHub workflows
- ✅ Environment variable management
- ✅ Cloud database setup (MongoDB Atlas)
- ✅ Backend deployment (Railway)
- ✅ Frontend deployment (Vercel)
- ✅ CORS configuration
- ✅ API integration
- ✅ Production best practices

## 🚀 Ready to Deploy?

Start here: **[DEPLOYMENT.md](./DEPLOYMENT.md)**

Good luck! 🍀

