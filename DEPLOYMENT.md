# 🚀 Deployment Guide - Breast Cancer Dashboard

This guide provides step-by-step instructions for deploying the Breast Cancer Dashboard to production using **Vercel** (frontend) and **Railway** (backend) free tiers.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Backend Deployment (Railway)](#backend-deployment-railway)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Environment Variables Configuration](#environment-variables-configuration)
- [Post-Deployment Verification](#post-deployment-verification)
- [Troubleshooting](#troubleshooting)
- [Cost Optimization](#cost-optimization)

---

## Prerequisites

Before you begin, ensure you have:

1. **GitHub Account** - For version control and deployment integration
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com) (free tier available)
3. **Railway Account** - Sign up at [railway.app](https://railway.app) (free tier: $5 credit/month)
4. **MongoDB Atlas Account** - Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) (free tier: 512MB)
5. **OpenAI API Key** - Get from [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
6. **Git** installed on your local machine
7. **Node.js 16+** and **Python 3.10+** for local testing

---

## Architecture Overview

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  Vercel         │────────▶│  Railway         │────────▶│  MongoDB Atlas  │
│  (Frontend)     │  HTTPS  │  (Backend API)   │  HTTPS  │  (Database)     │
│                 │         │                  │         │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
      React                      FastAPI                      MongoDB
   Tailwind CSS                  Python 3.10                  Free Tier
```

---

## 🗄️ Step 0: Setup MongoDB Atlas (Database)

### 0.1 Create MongoDB Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up or log in
3. Click **"Build a Database"**
4. Select **"M0 FREE"** tier
5. Choose a cloud provider and region (closest to your users)
6. Name your cluster (e.g., `breast-cancer-cluster`)
7. Click **"Create"**

### 0.2 Configure Database Access

1. In the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Username: `dashboard_user` (or your choice)
5. Click **"Autogenerate Secure Password"** and **save it securely**
6. Under "Database User Privileges", select **"Read and write to any database"**
7. Click **"Add User"**

### 0.3 Configure Network Access

1. In the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. Click **"Allow Access from Anywhere"** (0.0.0.0/0)
   - ⚠️ This is necessary for Railway to connect
   - Security is handled by username/password authentication
4. Click **"Confirm"**

### 0.4 Get Connection String

1. Go to **"Database"** in the left sidebar
2. Click **"Connect"** on your cluster
3. Select **"Connect your application"**
4. Driver: **Python**, Version: **3.6 or later**
5. Copy the connection string (looks like):
   ```
   mongodb+srv://dashboard_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with the password you saved earlier
7. **Save this connection string** - you'll need it for Railway

---

## 🚂 Backend Deployment (Railway)

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd Comp_Datos_Dash
   git init
   git add .
   git commit -m "Initial commit - ready for deployment"
   ```

2. **Push to GitHub**:
   ```bash
   # Create a new repository on GitHub first, then:
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy Backend to Railway

1. **Go to [Railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select your repository
6. Railway will detect it's a Python project

### Step 3: Configure Backend Environment Variables

1. In your Railway project, click on your service
2. Go to the **"Variables"** tab
3. Click **"+ New Variable"** and add the following:

   ```env
   MONGO_URL=mongodb+srv://dashboard_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   DB_NAME=breast_cancer_dashboard
   CORS_ORIGINS=https://your-app.vercel.app
   OPENAI_API_KEY=sk-your-openai-api-key-here
   HOST=0.0.0.0
   PORT=8000
   ```

   **Important Notes:**
   - Replace `MONGO_URL` with your MongoDB Atlas connection string
   - Replace `OPENAI_API_KEY` with your actual OpenAI API key
   - For `CORS_ORIGINS`, you'll update this after deploying the frontend
   - Railway automatically sets `PORT`, but we include it for clarity

### Step 4: Configure Build Settings

1. In Railway, go to **"Settings"** tab
2. Under **"Build"**, set:
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty (Railway will auto-detect)
   - **Start Command**: Leave empty (Railway will use Procfile)

3. Railway will automatically:
   - Detect Python from `requirements.txt`
   - Install dependencies using `pip install -r requirements.txt`
   - Use the `Procfile` to start the server

4. Click **"Deploy"** or wait for automatic deployment

### Step 5: Get Backend URL

1. Once deployed, go to **"Settings"** tab
2. Under **"Domains"**, click **"Generate Domain"**
3. Railway will generate a URL like: `https://your-app.railway.app`
4. **Save this URL** - you'll need it for the frontend

### Step 6: Verify Backend Deployment

1. Open your Railway backend URL in a browser
2. You should see: `{"message": "Hello World"}`
3. Test the API docs: `https://your-app.railway.app/docs`

---

## ▲ Frontend Deployment (Vercel)

### Step 1: Deploy Frontend to Vercel

1. **Go to [Vercel.com](https://vercel.com)**
2. Click **"Add New Project"**
3. Import your GitHub repository
4. Vercel will auto-detect it's a React app

### Step 2: Configure Build Settings

1. **Framework Preset**: Create React App
2. **Root Directory**: `frontend`
3. **Build Command**: `npm run build` or `yarn build`
4. **Output Directory**: `build`
5. **Install Command**: `npm install` or `yarn install`


### Step 3: Configure Frontend Environment Variables

1. In Vercel, go to **"Settings"** → **"Environment Variables"**
2. Add the following variable:

   | Name | Value |
   |------|-------|
   | `REACT_APP_BACKEND_URL` | `https://your-app.railway.app` |

   - Replace with your actual Railway backend URL from earlier
   - Make sure to include `https://` and NO trailing slash

3. Click **"Save"**

### Step 4: Deploy Frontend

1. Click **"Deploy"**
2. Vercel will build and deploy your frontend
3. Once complete, you'll get a URL like: `https://your-app.vercel.app`

### Step 5: Update Backend CORS Settings

Now that you have your frontend URL, update the backend:

1. Go back to **Railway**
2. Navigate to your backend service
3. Go to **"Variables"** tab
4. Update `CORS_ORIGINS` to include your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app,https://your-app.railway.app
   ```
5. Click **"Save"** - Railway will automatically redeploy

---

## 🔐 Environment Variables Configuration

### Backend Environment Variables (Railway)

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGO_URL` | MongoDB Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
| `DB_NAME` | Database name | `breast_cancer_dashboard` |
| `CORS_ORIGINS` | Allowed frontend origins (comma-separated) | `https://app.vercel.app` |
| `OPENAI_API_KEY` | OpenAI API key for AI features | `sk-...` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port (auto-set by Railway) | `8000` |

### Frontend Environment Variables (Vercel)

| Variable | Description | Example |
|----------|-------------|---------|
| `REACT_APP_BACKEND_URL` | Backend API URL | `https://your-app.railway.app` |

---

## ✅ Post-Deployment Verification

### 1. Test Backend API

```bash
# Test root endpoint
curl https://your-app.railway.app/api/

# Should return: {"message": "Hello World"}

# Test API documentation
# Open in browser: https://your-app.railway.app/docs
```

### 2. Test Frontend

1. Open your Vercel URL: `https://your-app.vercel.app`
2. You should see the dashboard interface
3. Try uploading a CSV file
4. Verify that data loads and visualizations appear

### 3. Test Full Integration

1. Upload the sample dataset (`CubanDataset.csv`)
2. Navigate through all tabs:
   - 📊 Exploración General
   - 🎗️ Factores Clínicos
   - 📈 Correlaciones y Patrones
   - 📋 Exportar Resultados
3. Test AI features:
   - Click "Generar Insights con IA"
   - Generate a clinical report
4. Test export functionality (CSV, JSON, Excel)

---

## 🐛 Troubleshooting

### Backend Issues

#### Problem: "Application failed to respond"
**Solution:**
- Check Railway logs: Go to your service → "Deployments" → Click on latest deployment → "View Logs"
- Verify all environment variables are set correctly
- Ensure MongoDB connection string is correct

#### Problem: "CORS error" in browser console
**Solution:**
- Verify `CORS_ORIGINS` in Railway includes your Vercel URL
- Make sure there are no trailing slashes in URLs
- Check that both HTTP and HTTPS are handled correctly

#### Problem: "OpenAI API error"
**Solution:**
- Verify your OpenAI API key is valid
- Check your OpenAI account has available credits
- Ensure the API key has proper permissions

### Frontend Issues

#### Problem: "Failed to fetch" or network errors
**Solution:**
- Verify `REACT_APP_BACKEND_URL` is set correctly in Vercel
- Check that the backend is running (visit the Railway URL)
- Ensure CORS is configured correctly on the backend

#### Problem: Build fails on Vercel
**Solution:**
- Check build logs in Vercel dashboard
- Verify `package.json` has all required dependencies
- Try building locally first: `cd frontend && npm run build`
- Check that Node.js version is compatible (16+)

### Database Issues

#### Problem: "MongoServerError: Authentication failed"
**Solution:**
- Verify MongoDB username and password in connection string
- Check that database user has correct permissions
- Ensure password doesn't contain special characters that need URL encoding

#### Problem: "Connection timeout"
**Solution:**
- Verify Network Access in MongoDB Atlas allows 0.0.0.0/0
- Check that connection string is correct
- Try connecting from Railway logs to see detailed error

---

## 💰 Cost Optimization

### Free Tier Limits

#### Vercel (Frontend)
- ✅ **100 GB bandwidth/month**
- ✅ **Unlimited deployments**
- ✅ **Automatic HTTPS**
- ✅ **Custom domains**

#### Railway (Backend)
- ✅ **$5 credit/month** (free tier)
- ✅ **500 hours/month** execution time
- ⚠️ **Sleeps after 30 min inactivity** (wakes on request)
- 💡 **Tip**: Keep usage under $5/month to stay free

#### MongoDB Atlas (Database)
- ✅ **512 MB storage**
- ✅ **Shared RAM**
- ✅ **No credit card required**
- 💡 **Tip**: Regularly clean old data to stay within limits

### Tips to Stay Within Free Tier

1. **Railway Backend**:
   - Monitor usage in Railway dashboard
   - Backend sleeps after inactivity (normal behavior)
   - First request after sleep may be slow (~10-30 seconds)

2. **MongoDB Atlas**:
   - Implement data retention policies
   - Delete old analysis results periodically
   - Monitor storage in Atlas dashboard

3. **OpenAI API**:
   - Set usage limits in OpenAI dashboard
   - Implement caching for repeated queries
   - Consider rate limiting AI features

---

## 🔄 Updating Your Deployment

### Update Backend

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update backend"
   git push
   ```
3. Railway will automatically detect changes and redeploy

### Update Frontend

1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update frontend"
   git push
   ```
3. Vercel will automatically detect changes and redeploy

### Manual Redeploy

**Railway:**
- Go to your service → "Deployments" → Click "Redeploy"

**Vercel:**
- Go to your project → "Deployments" → Click "Redeploy"

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [React Deployment Guide](https://create-react-app.dev/docs/deployment/)

---

## 🆘 Getting Help

If you encounter issues not covered in this guide:

1. **Check Logs**:
   - Railway: Service → Deployments → View Logs
   - Vercel: Project → Deployments → Function Logs
   - MongoDB: Atlas → Clusters → Metrics

2. **Common Issues**:
   - Ensure all environment variables are set
   - Verify URLs don't have trailing slashes
   - Check that services are running (not sleeping)

3. **Support Resources**:
   - Railway Discord: [discord.gg/railway](https://discord.gg/railway)
   - Vercel Discord: [vercel.com/discord](https://vercel.com/discord)
   - MongoDB Community: [community.mongodb.com](https://community.mongodb.com)

---

## ✨ Success!

Your Breast Cancer Dashboard is now deployed and accessible worldwide! 🎉

- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`

Share your deployment URLs and start analyzing breast cancer risk factors!


