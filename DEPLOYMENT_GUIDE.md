# Deployment Guide - Sales Data Analysis & Forecasting

## Quick Start - Run Locally

### 1. Clone Repository
```bash
git clone https://github.com/shashwatpathak002-glitch/sales-data-analysis-ai
cd sales-data-analysis-ai
```

### 2. Setup Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Enhanced App
```bash
streamlit run app_enhanced.py
```

The app will open at `http://localhost:8501`

## Test Credentials (Demo)
- **Username**: demo
- **Password**: demo123
- Or create a new account via Register tab

---

## Deploy to Streamlit Cloud (FREE & EASY)

### Step 1: Push Code to GitHub
Ensure all changes are committed and pushed.

### Step 2: Visit Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub account
3. Click "New app"

### Step 3: Configure Deployment
- **Repository**: shashwatpathak002-glitch/sales-data-analysis-ai
- **Branch**: main
- **Main file path**: app_enhanced.py

### Step 4: Deploy
- Click "Deploy"
- Wait 2-3 minutes for deployment
- Share your live URL

---

## Features Available After Deployment

✅ **User Authentication**
- Register new account
- Secure login with password hashing
- Persistent session management

✅ **Data Management**
- Upload CSV files
- Store data in SQLite database
- View all uploads
- Delete data as needed

✅ **Analysis & Forecasting**
- Exploratory Data Analysis (EDA)
- Time series forecasting
- Interactive visualizations
- Download reports

✅ **Professional UI/UX**
- Modern gradient design
- Responsive layout
- Dark theme support
- Mobile-friendly interface

---

## Database Details

### SQLite Tables
1. **users** - User accounts with password hashing
2. **user_data** - Uploaded CSV data storage
3. **forecasts** - Generated forecasts and metrics

### Stored Data
- User credentials (securely hashed)
- CSV file content (JSON format)
- Forecast results
- Analysis metadata

---

## Environment Variables (Optional)

Create `.env` file in root:
```
DATABASE_PATH=users.db
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"
**Solution**: Ensure you're running from project root directory

### Issue: "Database locked error"
**Solution**: Delete `users.db` and restart app (creates fresh database)

### Issue: "Streamlit Cloud shows blank page"
**Solution**: Check that `app_enhanced.py` is in root directory

---

## Production Considerations

1. **Use PostgreSQL instead of SQLite** for production
2. **Add SSL/TLS certificates** for HTTPS
3. **Implement email verification** for registration
4. **Add password reset functionality**
5. **Enable two-factor authentication (2FA)**
6. **Use environment variables** for sensitive data
7. **Set up automated backups** for database
8. **Enable logging and monitoring**

---

## Performance Tips

- Cache forecasts to avoid recomputation
- Use pagination for large datasets
- Optimize database queries with indexes
- Compress uploaded CSV files
- Use CDN for static assets

---

## Support

- GitHub Issues: [Create Issue](https://github.com/shashwatpathak002-glitch/sales-data-analysis-ai/issues)
- Email: shashwatpathak@example.com
- LinkedIn: [shashwat-pathak-6b8ab3337](https://linkedin.com/in/shashwat-pathak-6b8ab3337/)

---

**Last Updated**: January 2, 2026
**Status**: Production Ready
