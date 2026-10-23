# Kalyan Simulator Admin Operations Console & API

This repository houses the complete **Admin Operations Console & API** for the **Kalyan Simulator** platform, incorporating the comprehensive 13-section operational structure and workflows from the live Sara 777 control panel.

It is a high-performance monorepo consisting of:
- **`admin-frontend/`**: Node.js 20+ / Next.js 14 Web Operations Console.
- **`admin-backend/`**: Python 3.11+ / FastAPI backend connected to MongoDB Atlas.

---

## 🧭 Navigation & Feature Architecture (Matching SARA 777)

The admin panel follows the exact 13-section operational workflow:

1. **Dashboards (`/dashboard`)**: Key performance metrics (Total Users, Games, Bids, Payouts), live **Ank 0–9 bid distributions**, pending fund requests, and unapproved users.
2. **Declare Result (`/dashboard/results/publish`)**: Real-time result declaration console with 3-digit Pana selector (auto-calculating single digit Ank) and undo/correction history.
3. **Starline Management (`/dashboard/markets/starline`)**: Hourly markets (10 AM to 10 PM), Starline rates, bid ledger, hourly result declaration, and win reports.
4. **Gali Disswar (`/dashboard/markets/gali-disawar`)**: Gali, Disawar, Faridabad, Ghaziabad market schedules, left/right/jodi rates, result declaration, and reports.
5. **Report Management (`/dashboard/reports`)**: Complete User Bid History, Customer Sell Reports, Winning Reports, Transfer Point Reports, Bid Win Reports, and Withdraw Reports.
6. **Winning Prediction (`/dashboard/reports/number-frequency`)**: Pre-declaration liability and payout calculation engine across numbers 0–9.
7. **Wallet Management (`/dashboard/wallet-activity`)**: Fund request queue with payment slip preview, withdrawal approval with receipt upload, admin balance adjustments, and bid reverts.
8. **User Management (`/dashboard/students`)**: User search, balance management, and instant toggles for **Betting Allowed**, **Transfer Allowed**, and **Account Status**.
9. **Games Management (`/dashboard/markets/matka`)**: Main Matka games (Kalyan, Milan, Rajdhani, etc.), Hindi naming, market open/close timings, and rate charts.
10. **Game & Numbers (`/dashboard/game-config`)**: Single Digit (0–9), Jodi Digit (00–99), Single Pana (120), Double Pana (90), Triple Pana (10), Half Sangam, Full Sangam, and Panel Charts.
11. **Notice Management (`/dashboard/content/scrolling`)**: Scrolling notices, emergency tickers, and push notifications.
12. **Users Query (`/dashboard/support/queries`)**: User ticket inbox with admin reply modal.
13. **Settings (`/dashboard/system/settings`)**: Minimum deposit/withdrawal rules, WhatsApp/Telegram contact links, QR code management, and slider banners.

---

## 🚀 Deployment Guide

### 1. Deploy Frontend to Vercel

1. Open [vercel.com/new](https://vercel.com/new) in your browser.
2. Import repository: `https://github.com/visionmember54/sara777-admin`.
3. Configure project:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `admin-frontend`
4. Add Environment Variables:
   - `BACKEND_URL`: `https://kalyan-api-gotl.onrender.com` (or your Render URL)
   - `SESSION_COOKIE_NAME`: `sara777_admin_session`
5. Click **Deploy**.

---

### 2. Deploy Backend to Render

1. Open [dashboard.render.com](https://dashboard.render.com/).
2. Create a **New Web Service** connected to `visionmember54/sara777-admin` (or use Blueprint with `render.yaml`).
3. Settings:
   - **Environment**: `Python 3`
   - **Root Directory**: `admin-backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --proxy-headers --forwarded-allow-ips='*'`
4. Key Environment Variables:
   - `MONGODB_URL`: `mongodb+srv://visionmember54_db_user:m2tBvaFeikpWS1Cy@cluster0.t3a9ka9.mongodb.net/kalyandb?retryWrites=true&w=majority`
   - `MONGODB_DB_NAME`: `kalyandb`
   - `APP_ENV`: `production`
   - `JWT_SECRET`: *(auto-generated or set custom string)*
   - `CORS_ORIGINS`: Your Vercel frontend URL (e.g. `https://sara777-admin.vercel.app`)

---

## 💻 Local Development

### Backend (FastAPI)
```bash
cd admin-backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Swagger API docs available at `http://localhost:8000/docs`.

### Frontend (Next.js)
```bash
cd admin-frontend
npm install
npm run dev
```
Admin console accessible at `http://localhost:3000`.
