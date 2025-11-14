# 📋 Deployment Checklist

Use this checklist to ensure you complete all deployment steps correctly.

## Pre-Deployment

- [ ] GitHub repository created and code pushed
- [ ] All sensitive data removed from code
- [ ] `.env` files are in `.gitignore`
- [ ] Local testing completed successfully

## MongoDB Atlas Setup

- [ ] MongoDB Atlas account created
- [ ] Free tier cluster created (M0)
- [ ] Database user created with password saved
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string obtained and saved

## Railway Backend Deployment

- [ ] Railway account created
- [ ] New project created from GitHub repo
- [ ] Root directory set to `backend`
- [ ] Environment variables configured:
  - [ ] `MONGO_URL`
  - [ ] `DB_NAME`
  - [ ] `OPENAI_API_KEY`
  - [ ] `CORS_ORIGINS` (will update after frontend deployment)
  - [ ] `HOST`
  - [ ] `PORT`
- [ ] Build command verified: `pip install -r requirements.txt`
- [ ] Start command verified: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- [ ] Domain generated
- [ ] Backend URL saved: `https://__________________.railway.app`
- [ ] Backend tested: `/api/` endpoint returns `{"message": "Hello World"}`
- [ ] API docs accessible: `/docs`

## Vercel Frontend Deployment

- [ ] Vercel account created
- [ ] New project created from GitHub repo
- [ ] Root directory set to `frontend`
- [ ] Build settings configured:
  - [ ] Build command: `npm run build` or `yarn build`
  - [ ] Output directory: `build`
- [ ] Environment variable configured:
  - [ ] `REACT_APP_BACKEND_URL` = Railway backend URL
- [ ] Deployment successful
- [ ] Frontend URL saved: `https://__________________.vercel.app`
- [ ] Frontend loads correctly in browser

## Post-Deployment Configuration

- [ ] Updated `CORS_ORIGINS` in Railway to include Vercel URL
- [ ] Railway backend redeployed with new CORS settings
- [ ] Tested full integration:
  - [ ] CSV file upload works
  - [ ] Data visualizations display correctly
  - [ ] AI insights generation works
  - [ ] Report generation works
  - [ ] Export functionality works (CSV, JSON, Excel)

## Verification

- [ ] Backend health check: `curl https://your-app.railway.app/api/`
- [ ] Frontend loads without errors
- [ ] No CORS errors in browser console
- [ ] All tabs functional:
  - [ ] 📊 Exploración General
  - [ ] 🎗️ Factores Clínicos
  - [ ] 📈 Correlaciones y Patrones
  - [ ] 📋 Exportar Resultados
- [ ] Sample dataset (`CubanDataset.csv`) processes successfully

## Documentation

- [ ] Deployment URLs documented
- [ ] Environment variables documented
- [ ] Access credentials stored securely (password manager)
- [ ] Team members notified of deployment

## Optional Enhancements

- [ ] Custom domain configured on Vercel
- [ ] Custom domain configured on Railway
- [ ] Monitoring/analytics set up
- [ ] Error tracking configured (e.g., Sentry)
- [ ] Usage limits set on OpenAI dashboard

---

## Quick Reference

**MongoDB Atlas**: https://cloud.mongodb.com  
**Railway Dashboard**: https://railway.app/dashboard  
**Vercel Dashboard**: https://vercel.com/dashboard  
**OpenAI API Keys**: https://platform.openai.com/api-keys

**Your Deployment URLs**:
- Frontend: `https://__________________.vercel.app`
- Backend: `https://__________________.railway.app`
- API Docs: `https://__________________.railway.app/docs`

---

## Troubleshooting Quick Links

- [Full Deployment Guide](./DEPLOYMENT.md)
- [Railway Logs](https://railway.app/dashboard) → Your Service → Deployments → View Logs
- [Vercel Logs](https://vercel.com/dashboard) → Your Project → Deployments → Function Logs
- [MongoDB Metrics](https://cloud.mongodb.com) → Clusters → Metrics

---

**Last Updated**: 2025-11-14

