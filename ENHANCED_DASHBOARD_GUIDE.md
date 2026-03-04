# 🏥 Enhanced Hospital Data Insights Dashboard - User Guide

## 📌 What's New

Your dashboard has been completely redesigned with a **modern SaaS-style interface** featuring advanced multi-page analytics, dark mode, and AI-powered clinical decision support!

### 🎨 Design System Highlights

**Modern SaaS Aesthetics:**
- 🌓 **Dark Mode Support** - Toggle between light and dark themes with persistent preference
- 📱 **Fully Responsive** - Optimized for desktop, tablet, and mobile devices
- 🔔 **Toast Notifications** - Real-time feedback for all user actions
- ⚡ **Loading States** - Skeleton loaders show progress during data fetching
- 🎨 **Design Tokens** - Consistent spacing, colors, typography, and shadows
- 📊 **Interactive Components** - Hover effects, transitions, and modern UI patterns
- 🎯 **Premium Feel** - Clean, professional interface with attention to detail

## ✨ Dashboard Features

### 🎨 Modern Multi-Page Interface

**4 Comprehensive Pages:**
1. **📊 Overview** - Real-time KPIs and high-level analytics
2. **🏥 OPD Analytics** - Outpatient department performance metrics
3. **🛏️ Inpatient & Ward Analytics** - Ward-level insights and admission trends
4. **🤖 AI Risk Assessment** - Advanced ML-powered patient risk stratification

**Modern Navigation:**
- Sidebar navigation with icon buttons and active state highlighting
- Smooth page transitions with fade effects
- Mobile-responsive with hamburger menu
- Persistent navigation state across sessions

**Enhanced Navigation:**
- 🎨 **Topbar** - Real-time API status, last updated time, theme toggle
- 🔍 **Toolbar** - Smart department filter with chip-style multi-select
- 📡 **Status Indicators** - Color-coded API health (green = healthy, red = offline)
- 🕒 **Timestamps** - Auto-updating relative time ("2 minutes ago")
- 💾 **Session Persistence** - Filter preferences saved in localStorage

### 📊 Overview Dashboard

**6 Modern KPI Cards:**
- 👥 Total Patients in System
- 🏥 OPD Visit Volumes
- 🛌 Inpatient Admissions
- ⏱️ Average Wait Times
- 🔄 30-Day Readmission Rates
- 💰 Total Billing Revenue

**Card Features:**
- Gradient backgrounds with hover effects
- Animated loading skeletons
- Icon indicators for each metric
- Responsive grid layout
- Clean typography hierarchy

**Interactive Visualizations:**
- Monthly visit trends line chart with modern color palette
- Department distribution doughnut chart
- Auto-refresh every 5 minutes
- Smooth animations and transitions
- Responsive chart sizing

### 🏥 OPD (Outpatient) Analytics

**Comprehensive Metrics:**
- Average wait times by department (horizontal bar chart with color coding)
- Wait time patterns by hour of day (line chart showing peak times)
- Visit volume by day of week (bar chart for staffing optimization)
- Department visit volume distribution (doughnut chart)

**Insights for:**
- Operational optimization
- Staffing decisions
- Resource allocation
- Patient flow management

### 🛏️ Inpatient & Ward Analytics

**Ward-Level Insights:**
- Average length of stay (LOS) by ward
- 30-day readmission rates by diagnosis code
- Monthly admission trends with seasonality patterns
- Ward performance comparative analysis

**Use Cases:**
- Capacity planning
- Discharge optimization
- Quality improvement initiatives
- Resource allocation

### 🤖 AI-Powered Patient Risk Assessment

#### **Individual Patient Assessment**

1. **Patient Selection**
   - Searchable dropdown with up to 1,000 patients
   - Patient ID, Age, Gender display

2. **Clinical Profile Display**
   - Demographics: Age, Gender, BMI, Smoking Status
   - Chronic Conditions: Diabetes, Hypertension, Asthma, Heart Disease
   - Healthcare Utilization: Recent visits, admissions, average LOS

3. **AI-Predicted Risk Assessment**
   - Interactive risk gauge visualization (0-100%)
   - Color-coded risk stratification:
     - 🟢 Low Risk (<35%)
     - 🟡 Medium Risk (35-60%)
     - 🔴 High Risk (≥60%)
   - Population comparison with percentile ranking
   - Delta indicators showing variance from baseline

4. **Evidence-Based Clinical Recommendations**
   
   **High Risk (≥60%)** - Immediate Interventions:
   - Discharge planning meeting within 24 hours
   - Follow-up within 3 days
   - Home health services referral
   - Daily monitoring for first week
   - Medication reconciliation with pharmacist
   
   **Medium Risk (35-60%)** - Enhanced Monitoring:
   - Follow-up within 7 days
   - Medication reconciliation
   - Bi-weekly check-ins
   - Care coordinator assignment
   
   **Low Risk (<35%)** - Standard Procedures:
   - Routine follow-up within 14-30 days
   - Standard educational materials

5. **Detailed Risk Factor Analysis**
   
   **Risk Factors with Impact Scores:**
   - Diabetes (+18%), Hypertension (+12%), Heart Disease (+20%)
   - Advanced age (+15%), Obesity (+10%), Smoking (+8%)
   - Frequent admissions (+12%)
   
   **Protective Factors:**
   - Healthy weight (-5%)
   - Non-smoker (-3%)
   - Younger age (-8%)
   
   **Severity Classification:**
   - 🔴 Critical Impact
   - 🟠 High Impact
   - 🟡 Medium Impact
   - 🟢 Protective Factor

#### **Population-Level Risk Stratification**

**Advanced Filtering & Sorting:**
- Filter by: All Patients, High Risk Only, Med-High Risk, Low Risk
- Sort by: Risk (high/low), Age (old/young)
- Display control: 20/50/100/200 patients

**Comprehensive Patient Table:**
All patients displayed with:
- Risk percentage and category
- Age and BMI
- Comorbidity count
- Recent visits and admissions
- Condition indicators (✓ for Diabetes, Hypertension)

**Population Statistics Dashboard:**
- Total patients analyzed
- Count and percentage for each risk category
- Visual stat badges with color coding

**Export Functionality:**
- Download high-risk patient list as CSV
- Includes all patient metadata for care coordination

**Model Transparency:**
- Uses Large Tabular Model (LTM) with intelligent fallback
- 97.9% accuracy on readmission prediction
- Hybrid foundation model approach for optimal performance
- All recommendations require clinical review

## 🚀 How to Use

### Step 1: Start the System

```powershell
# If data needs regeneration
python scripts/run_pipeline.py

# Start API server (if not already running)
python -m uvicorn backend.api:app --reload --port 3000
```

### Step 2: Open the Enhanced Dashboard

Open `frontend/index.html` in your browser

**Quick Access:**
- 🖥️ Double-click the HTML file
- 🌐 Or serve with: `python -m http.server 8080` in frontend folder

**First-Time Setup:**
1. Dashboard opens in light mode by default
2. Try the 🌓 theme toggle in top-right corner
3. Your preference is saved automatically
4. Green dot indicates API is connected

### Step 3: Navigate the Dashboard

1. **Select a Page** using the sidebar navigation (Overview/OPD/Inpatient/AI Risk)
2. **Toggle Theme** using the 🌓 button in top-right corner
3. **Filter by Department** using chip-style buttons in the toolbar
4. **Explore Visualizations** - all charts are interactive with hover tooltips
5. **Monitor API Status** - watch the colored dot next to "API Status" in topbar
6. **Check Updates** - see "Last updated" timestamp in topbar

### Step 4: AI Risk Assessment Workflow

1. Navigate to **🤖 AI Risk Assessment** page
2. Select a patient from the dropdown
3. Click **Assess Risk** button
4. Review:
   - Clinical profile
   - AI-predicted risk score (gauge visualization)
   - Evidence-based recommendations
   - Detailed risk factors with impact scores
5. Scroll down to view population-level stratification
6. Use filters and sorting to find high-risk patients
7. Export to CSV for care coordination

## 📊 Enhanced Data Structure

**New Fields Added:**
- `triage_level` - Emergency priority classification (5 levels)
- `ward` - Ward assignment for admitted patients
- `diagnosis_code` - ICD-10 diagnosis codes
- `hour_of_day` - Visit hour (0-23)
- `day_of_week` - Visit day (0-6)
- `billing_amount` - Billing/revenue data
- `readmitted_30d_flag` - Binary readmission indicator

## 🔌 New API Endpoints

### OPD Analytics
```http
GET /opd-analytics
```
Returns: Wait times by department, hour, day of week

### Inpatient Analytics
```http
GET /inpatient-analytics
```
Returns: LOS by ward, readmissions by diagnosis, monthly trends

### Patient List
```http
GET /patients/list?limit=1000
```
Returns: Comprehensive patient profiles for risk assessment

### Billing Summary
```http
GET /billing-summary
```
Returns: Revenue metrics by department

## 🎨 Design Enhancements

**Modern UI/UX:**
- Gradient-styled KPI cards with hover effects
- Color-coded risk indicators
- Responsive grid layouts
- Professional medical theme
- Smooth page transitions
- Session persistence

**Accessibility:**
- Clear visual hierarchy
- Color-blind friendly palette
- Responsive design (mobile, tablet, desktop)
- Keyboard navigation support

## 📈 Key Metrics

**Model Performance:**
- Classifier Accuracy: 97.9%
- F1 Score: 98.95%
- ROC-AUC: 97.87%
- Regressor RMSE: 19.38 minutes

**Data Volume:**
- 5,000 patients
- 15,000 visits
- 7,524 admissions
- 50.2% admission rate

## 🔄 Workflow Integration

**Clinical Use Cases:**

1. **Daily Morning Huddle**
   - Review Overview page for overnight metrics
   - Check high-risk patients before rounds
   - Plan discharges using risk assessments

2. **Care Coordination**
   - Export high-risk patient list
   - Assign care managers
   - Schedule follow-ups

3. **Quality Improvement**
   - Analyze readmission trends by diagnosis
   - Identify wards with high LOS
   - Optimize OPD wait times

4. **Resource Planning**
   - Review hourly/daily visit patterns
   - Plan staffing based on demand
   - Forecast admission volumes

## 🌟 Best Practices

1. **Regular Data Refresh**: Run pipeline weekly to update data
2. **Risk Assessment Workflow**: Review high-risk patients daily
3. **Export Reports**: Download CSV files for team meetings
4. **Filter Optimization**: Use department filters for focused analysis
5. **Session Management**: Browser retains your filter preferences

## 🛠️ Troubleshooting

**Dashboard doesn't load?**
- Check API server is running: http://localhost:3000/health
- Verify file path to index.html
- Clear browser cache (Ctrl+Shift+Delete)
- Check browser console (F12) for errors

**No data showing?**
- Run: `python scripts/run_pipeline.py`
- Restart API server: `python -m uvicorn backend.api:app --reload --port 3000`
- Watch for toast notifications indicating errors

**Risk predictions not working?**
- Ensure models are trained (pipeline completed)
- Check backend/models/ folder has .pkl files

## 📝 Notes

- All AI recommendations require clinical professional review
- Risk scores are estimates based on historical data
- Population baseline is approximate (35% average risk)
- Export functionality works in modern browsers only
- Department filter affects Overview and OPD pages only
- **Dark mode preference is saved in browser localStorage**
- **Toast notifications appear in bottom-right corner**
- **Loading skeletons show while data is being fetched**
- **Mobile menu accessible via hamburger icon on small screens**

## 🎓 Training Resources

**For Clinical Staff:**
- Risk categories: Low (<35%), Medium (35-60%), High (≥60%)
- Protective vs. risk factors explained
- Clinical intervention protocols by risk level

**For Administrators:**
- KPI interpretation guide
- Revenue metrics explained
- Operational optimization insights

---

**Congratulations! 🎉** You now have a state-of-the-art healthcare analytics platform with AI-powered clinical decision support!

For questions or issues, please review the API documentation at: http://localhost:3000/docs

## 🎨 UI/UX Features Summary

**Design System:**
- 70+ CSS custom properties for consistent theming
- Light and dark color palettes
- 8-point spacing scale (4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px)
- Typography scale with system font stack
- Shadow system for depth (sm, md, lg, xl)
- Border radius tokens (sm: 6px, md: 8px, lg: 12px, xl: 16px, 2xl: 24px)

**Interactive Components:**
- Buttons with hover/active states
- Cards with shadow elevation
- Badges for status indicators
- Toast notifications (success, error, warning, info)
- Loading skeletons for async content
- Form controls with focus states
- Tables with hover rows

**Responsive Breakpoints:**
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

**Accessibility:**
- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- Focus indicators
- Color contrast compliant
- Reduced motion support
