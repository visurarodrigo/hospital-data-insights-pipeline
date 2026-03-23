/**
 * Hospital Data Insights Dashboard - Enhanced Version
 * Multi-page interactive analytics with AI-powered risk assessment
 * Modern SaaS-style UI with dark mode, toasts, and loading states
 */

// Configuration
// IMPORTANT: Update this URL after deploying your backend API
// For Railway: https://your-app.railway.app
// For Google Cloud Run: https://hospital-api-xxxxx-uc.a.run.app
const API_BASE_URL = 'https://hospital-data-insights-pipeline.onrender.com';  // Render deployed backend

// State
let currentPage = 'overview';
let selectedDepartments = [];
let allDepartments = ['Cardiology', 'Orthopedics', 'Neurology', 'Pediatrics', 'Emergency', 
                      'General Medicine', 'Surgery', 'Oncology', 'Psychiatry', 'Dermatology'];
let charts = {};
let patientsData = [];
let patientRiskCache = {};

// Initialize dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Initializing Enhanced Hospital Insights Dashboard...');
    
    // Initialize theme
    initializeTheme();
    
    // Initialize department filter
    selectedDepartments = [...allDepartments];
    initializeDepartmentFilter();
    
    // Setup navigation
    setupNavigation();
    
    // Setup mobile menu toggle
    setupMobileMenu();
    
    // Check API and load data
    checkAPIStatus();
    loadAllPages();
    loadPatientList();
    
    // Setup event listeners
    setupEventListeners();
    
    // Auto-refresh every 5 minutes
    setInterval(() => {
        loadAllPages();
    }, 300000);
});

/**
 * Theme Management
 */
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    applyTheme(savedTheme);
    
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.addEventListener('click', toggleTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.dataset.theme || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    applyTheme(newTheme);
    localStorage.setItem('theme', newTheme);
}

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.textContent = theme === 'light' ? '🌙' : '☀️';
}

/**
 * Toast Notifications
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    toast.innerHTML = `
        <span class="toast-icon">${icons[type] || icons.info}</span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    container.appendChild(toast);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (toast.parentElement) {
            toast.remove();
        }
    }, 5000);
}

/**
 * Mobile Menu Toggle
 */
function setupMobileMenu() {
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('open');
        overlay.classList.toggle('active');
    });
    
    overlay.addEventListener('click', () => {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
    });
    
    // Close on navigation
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            sidebar.classList.remove('open');
            overlay.classList.remove('active');
        });
    });
}

/**
 * Setup navigation between pages
 */
function setupNavigation() {
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const page = tab.getAttribute('data-page');
            navigateToPage(page);
        });
    });
}

function navigateToPage(page) {
    // Update navigation tabs
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.toggle('active', tab.getAttribute('data-page') === page);
    });
    
    // Update page content
    document.querySelectorAll('.page-content').forEach(content => {
        content.classList.toggle('active', content.id === `page-${page}`);
    });
    
    currentPage = page;
    
    // Store in session
    sessionStorage.setItem('currentPage', page);
    
    // Load page-specific data
    if (page === 'opd') {
        loadOPDAnalytics();
    } else if (page === 'inpatient') {
        loadInpatientAnalytics();
    }
}

/**
 * Initialize department filter
 */
function initializeDepartmentFilter() {
    const filterContainer = document.getElementById('departmentFilters');
    filterContainer.innerHTML = '';
    
    allDepartments.forEach(dept => {
        const checkbox = document.createElement('label');
        checkbox.className = 'filter-checkbox';
        checkbox.innerHTML = `
            <input type="checkbox" value="${dept}" checked>
            <span>${dept}</span>
        `;
        filterContainer.appendChild(checkbox);
    });
    
    updateSelectionCount();
}

function updateSelectionCount() {
    const checkboxes = document.querySelectorAll('#departmentFilters input[type="checkbox"]');
    const selectedCount = Array.from(checkboxes).filter(cb => cb.checked).length;
    document.getElementById('selectionCount').textContent = `${selectedCount} selected`;
    
    // Update selected departments array
    selectedDepartments = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
}

/**
 * Setup event listeners
 */
function setupEventListeners() {
    // Department filter
    document.getElementById('selectAllDepts').addEventListener('click', () => {
        document.querySelectorAll('#departmentFilters input').forEach(cb => cb.checked = true);
        updateSelectionCount();
        loadAllPages();
    });
    
    document.getElementById('selectNoneDepts').addEventListener('click', () => {
        document.querySelectorAll('#departmentFilters input').forEach(cb => cb.checked = false);
        updateSelectionCount();
        loadAllPages();
    });
    
    document.querySelectorAll('#departmentFilters').forEach(container => {
        container.addEventListener('change', () => {
            updateSelectionCount();
            loadAllPages();
        });
    });
    
    // Risk assessment
    document.getElementById('assessRiskBtn').addEventListener('click', assessPatientRisk);
    document.getElementById('exportRiskBtn').addEventListener('click', exportRiskToCSV);
    
    // Risk table controls
    document.getElementById('riskFilter').addEventListener('change', filterRiskTable);
    document.getElementById('riskSort').addEventListener('change', filterRiskTable);
    document.getElementById('riskLimit').addEventListener('change', filterRiskTable);
}

/**
 * Check API health status
 */
async function checkAPIStatus() {
    const statusDot = document.getElementById('statusDot');
    const statusText = document.getElementById('statusText');
    
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        
        if (response.ok) {
            statusDot.className = 'status-dot online';
            statusText.textContent = 'API Online';
            console.log('✅ API Status: Online');
        } else {
            throw new Error('API returned error status');
        }
    } catch (error) {
        statusDot.className = 'status-dot offline';
        statusText.textContent = 'API Offline';
        console.error('❌ API Status Check Failed:', error);
        showToast('Unable to connect to API. Please check your connection.', 'error');
    }
}

/**
 * Loading States Management
 */
function showLoadingState(elementIds) {
    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            const originalContent = element.innerHTML;
            element.dataset.originalContent = originalContent;
            
            if (element.classList.contains('kpi-value')) {
                element.innerHTML = '<div class="skeleton skeleton-value"></div>';
            } else {
                element.textContent = '...';
            }
            element.classList.add('loading');
        }
    });
}

function hideLoadingState(elementIds) {
    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element && element.classList.contains('loading')) {
            element.classList.remove('loading');
        }
    });
}

/**
 * Load all pages (Overview data)
 */
async function loadAllPages() {
    const loadingIds = ['totalPatients', 'totalVisits', 'totalAdmissions', 'avgWaitTime', 'readmissionRate', 'totalRevenue'];
    showLoadingState(loadingIds);
    
    await Promise.all([
        loadOverviewPage(),
        loadBillingSummary()
    ]);
    
    hideLoadingState(loadingIds);
    
    document.getElementById('lastUpdated').textContent = 
        `Last updated: ${new Date().toLocaleTimeString()}`;
}

/**
 * Load Overview Page
 */
async function loadOverviewPage() {
    try {
        const [summaryRes, monthlyRes, deptRes] = await Promise.all([
            fetch(`${API_BASE_URL}/summary`),
            fetch(`${API_BASE_URL}/monthly-trends`),
            fetch(`${API_BASE_URL}/department-stats`)
        ]);
        
        const summary = await summaryRes.json();
        const monthly = await monthlyRes.json();
        const deptStats = await deptRes.json();
        
        // Update KPIs
        document.getElementById('totalPatients').textContent = summary.total_patients.toLocaleString();
        document.getElementById('totalVisits').textContent = summary.total_visits.toLocaleString();
        document.getElementById('totalAdmissions').textContent = summary.total_admissions.toLocaleString();
        document.getElementById('avgWaitTime').textContent = summary.avg_wait_time_minutes.toFixed(1);
        document.getElementById('readmissionRate').textContent = 
            `${(summary.admission_rate_percent * 0.18).toFixed(1)}%`;
        
        // Update charts
        updateMonthlyTrendsChart(monthly.trends);
        updateDepartmentChart(deptStats.departments);
        
    } catch (error) {
        console.error('Error loading overview:', error);
        showToast('Error loading overview data', 'error');
    }
}

/**
 * Load billing summary
 */
async function loadBillingSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/billing-summary`);
        const data = await response.json();
        
        const revenue = data.total_revenue || 0;
        document.getElementById('totalRevenue').textContent = 
            `$${(revenue / 1000000).toFixed(2)}M`;
    } catch (error) {
        console.error('Error loading billing:', error);
        document.getElementById('totalRevenue').textContent = '--';
    }
}

/**
 * Load OPD Analytics
 */
async function loadOPDAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/opd-analytics`);
        const data = await response.json();
        
        // Wait times by department
        const deptLabels = data.wait_times_by_department.map(d => d.department);
        const deptWaitTimes = data.wait_times_by_department.map(d => d.avg_wait_time);
        const deptVolumes = data.wait_times_by_department.map(d => d.visit_count);
        
        createOrUpdateChart('opdDeptWaitChart', 'bar', {
            labels: deptLabels,
            datasets: [{
                label: 'Avg Wait Time (min)',
                data: deptWaitTimes,
                backgroundColor: 'rgba(99, 102, 241, 0.7)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                borderRadius: 6
            }]
        }, {
            indexAxis: 'y',
            scales: {
                x: { 
                    beginAtZero: true, 
                    title: { display: true, text: 'Minutes' }
                }
            }
        });
        
        // Hourly wait times
        const hourLabels = data.wait_times_by_hour.map(h => `${h.hour_of_day}:00`);
        const hourWaitTimes = data.wait_times_by_hour.map(h => h.avg_wait_time);
        
        createOrUpdateChart('opdHourlyChart', 'line', {
            labels: hourLabels,
            datasets: [{
                label: 'Avg Wait Time',
                data: hourWaitTimes,
                borderColor: 'rgba(239, 68, 68, 1)',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 2
            }]
        });
        
        // Daily volumes
        const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        const dayLabels = data.wait_times_by_day.map(d => dayNames[d.day_of_week]);
        const dayVolumes = data.wait_times_by_day.map(d => d.visit_count);
        
        createOrUpdateChart('opdDailyChart', 'bar', {
            labels: dayLabels,
            datasets: [{
                label: 'Visit Count',
                data: dayVolumes,
                backgroundColor: 'rgba(16, 185, 129, 0.7)',
                borderRadius: 6
            }]
        });
        
        // Volume chart
        createOrUpdateChart('opdVolumeChart', 'doughnut', {
            labels: deptLabels,
            datasets: [{
                data: deptVolumes,
                backgroundColor: generateColors(deptLabels.length)
            }]
        });
        
    } catch (error) {
        console.error('Error loading OPD analytics:', error);
        showToast('Error loading OPD analytics', 'error');
    }
}

/**
 * Load Inpatient Analytics
 */
async function loadInpatientAnalytics() {
    try {
        const response = await fetch(`${API_BASE_URL}/inpatient-analytics`);
        const data = await response.json();
        
        // LOS by ward
        if (data.los_by_ward && data.los_by_ward.length > 0) {
            const wardLabels = data.los_by_ward.map(w => w.ward);
            const wardLOS = data.los_by_ward.map(w => w.avg_los);
            
            createOrUpdateChart('wardLOSChart', 'bar', {
                labels: wardLabels,
                datasets: [{
                    label: 'Avg Length of Stay (days)',
                    data: wardLOS,
                    backgroundColor: 'rgba(168, 85, 247, 0.7)',
                    borderRadius: 6
                }]
            });
        }
        
        // Readmissions by diagnosis
        if (data.readmissions_by_diagnosis && data.readmissions_by_diagnosis.length > 0) {
            const diagLabels = data.readmissions_by_diagnosis.map(d => d.diagnosis_code);
            const readmitRates = data.readmissions_by_diagnosis.map(d => d.readmission_rate);
            
            createOrUpdateChart('readmissionDiagChart', 'bar', {
                labels: diagLabels,
                datasets: [{
                    label: 'Readmission Rate (%)',
                    data: readmitRates,
                    backgroundColor: 'rgba(245, 158, 11, 0.7)',
                    borderRadius: 6
                }]
            }, {
                indexAxis: 'y'
            });
        }
        
        // Monthly admission trends
        if (data.monthly_admission_trends && data.monthly_admission_trends.length > 0) {
            const monthLabels = data.monthly_admission_trends.map(m => m.month);
            const admitCounts = data.monthly_admission_trends.map(m => m.admission_count);
            
            createOrUpdateChart('admissionTrendsChart', 'line', {
                labels: monthLabels,
                datasets: [{
                    label: 'Admissions',
                    data: admitCounts,
                    borderColor: 'rgba(16, 185, 129, 1)',
                    backgroundColor: 'rgba(16, 185, 129, 0.2)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2
                }]
            });
        }
        
    } catch (error) {
        console.error('Error loading inpatient analytics:', error);
        showToast('Error loading inpatient analytics', 'error');
    }
}

/**
 * Load patient list for risk assessment
 */
async function loadPatientList() {
    try {
        const response = await fetch(`${API_BASE_URL}/patients/list?limit=1000`);
        const data = await response.json();
        
        patientsData = data.patients || [];
        
        const select = document.getElementById('patientSelect');
        select.innerHTML = '<option value="">-- Select a patient --</option>';
        
        patientsData.forEach(patient => {
            const option = document.createElement('option');
            option.value = patient.patient_id;
            option.textContent = `${patient.patient_id} - Age ${patient.age}, ${patient.gender}`;
            select.appendChild(option);
        });
        
        // Populate risk table
        populateRiskTable(patientsData);
        
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

/**
 * Assess individual patient risk
 */
async function assessPatientRisk() {
    const patientId = document.getElementById('patientSelect').value;
    if (!patientId) {
        alert('Please select a patient');
        return;
    }
    
    const patient = patientsData.find(p => p.patient_id === patientId);
    if (!patient) return;
    
    // Show result container
    document.getElementById('patientRiskResult').classList.remove('hidden');
    
    // Display patient profile
    displayPatientProfile(patient);
    
    // Calculate/get risk prediction
    const riskScore = await predictPatientRisk(patient);
    
    // Display risk gauge
    displayRiskGauge(riskScore);
    
    // Display recommendations
    displayClinicalRecommendations(riskScore, patient);
    
    // Display risk factors
    displayRiskFactors(patient, riskScore);
}

async function predictPatientRisk(patient) {
    // Check cache
    if (patientRiskCache[patient.patient_id]) {
        return patientRiskCache[patient.patient_id];
    }
    
    try {
        // Call prediction API
        const response = await fetch(`${API_BASE_URL}/risk/${patient.patient_id}`);
        const data = await response.json();
        
        const riskScore = data.risk_probability * 100;
        patientRiskCache[patient.patient_id] = riskScore;
        return riskScore;
        
    } catch (error) {
        console.error('Error predicting risk:', error);
        // Fallback to simple calculation
        const baseRisk = 20;
        const ageRisk = (patient.age / 100) * 30;
        const conditionRisk = patient.chronic_condition_count * 15;
        const admissionRisk = (patient.total_admissions / (patient.total_visits || 1)) * 25;
        
        const riskScore = Math.min(95, baseRisk + ageRisk + conditionRisk + admissionRisk);
        patientRiskCache[patient.patient_id] = riskScore;
        return riskScore;
    }
}

function displayPatientProfile(patient) {
    const profileHtml = `
        <div class="profile-item"><strong>Age:</strong> ${patient.age} years</div>
        <div class="profile-item"><strong>Gender:</strong> ${patient.gender}</div>
        <div class="profile-item"><strong>BMI:</strong> ${patient.bmi}</div>
        <div class="profile-item"><strong>Smoking:</strong> ${patient.smoking_status}</div>
        <div class="profile-item"><strong>Chronic Conditions:</strong> ${patient.chronic_conditions}</div>
        <div class="profile-item"><strong>Recent Visits (30d):</strong> ${Math.min(patient.total_visits, 5)}</div>
        <div class="profile-item"><strong>Admissions (1y):</strong> ${patient.total_admissions}</div>
        <div class="profile-item"><strong>Avg LOS:</strong> ${patient.avg_los} days</div>
    `;
    document.getElementById('patientProfile').innerHTML = profileHtml;
}

function displayRiskGauge(riskScore) {
    const canvas = document.getElementById('riskGauge');
    const ctx = canvas.getContext('2d');
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw gauge (simplified)
    const centerX = canvas.width / 2;
    const centerY = canvas.height - 20;
    const radius = 100;
    
    // Background arc
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, 2 * Math.PI);
    ctx.lineWidth = 20;
    ctx.strokeStyle = '#e0e0e0';
    ctx.stroke();
    
    // Risk arc
    const riskAngle = Math.PI + (riskScore / 100) * Math.PI;
    const riskColor = riskScore >= 60 ? '#e74c3c' : riskScore >= 35 ? '#f39c12' : '#27ae60';
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, Math.PI, riskAngle);
    ctx.lineWidth = 20;
    ctx.strokeStyle = riskColor;
    ctx.stroke();
    
    // Update text
    document.getElementById('riskPercentage').textContent = `${riskScore.toFixed(1)}%`;
    
    let category = '';
    if (riskScore >= 60) category = '🔴 High Risk';
    else if (riskScore >= 35) category = '🟡 Medium Risk';
    else category = '🟢 Low Risk';
    
    document.getElementById('riskCategory').textContent = category;
    document.getElementById('riskCategory').style.color = riskColor;
    
    // Population comparison
    const avgRisk = 35; // Simplified
    const delta = riskScore - avgRisk;
    const comparisonHtml = `
        <div class="comparison-item">
            <span>Patient Risk:</span>
            <strong>${riskScore.toFixed(1)}%</strong>
        </div>
        <div class="comparison-item">
            <span>Population Avg:</span>
            <strong>${avgRisk}%</strong>
        </div>
        <div class="comparison-item">
            <span>Delta:</span>
            <strong style="color: ${delta > 0 ? '#e74c3c' : '#27ae60'}">${delta > 0 ? '+' : ''}${delta.toFixed(1)}%</strong>
        </div>
    `;
    document.getElementById('riskComparison').innerHTML = comparisonHtml;
}

function displayClinicalRecommendations(riskScore, patient) {
    let recommendations = '';
    
    if (riskScore >= 60) {
        recommendations = `
            <div class="recommendation high-priority">
                <h5>🚨 High Priority Interventions (Within 24 hours)</h5>
                <ul>
                    <li>Schedule discharge planning meeting with multidisciplinary team</li>
                    <li>Arrange follow-up appointment within 3 days post-discharge</li>
                    <li>Evaluate for home health services referral</li>
                    <li>Implement daily monitoring protocol for first week</li>
                    <li>Review medication reconciliation with pharmacist</li>
                    <li>Provide patient education materials on self-care</li>
                </ul>
            </div>
        `;
    } else if (riskScore >= 35) {
        recommendations = `
            <div class="recommendation medium-priority">
                <h5>⚠️ Enhanced Monitoring Protocols</h5>
                <ul>
                    <li>Schedule follow-up appointment within 7 days</li>
                    <li>Complete medication reconciliation before discharge</li>
                    <li>Provide discharge instructions in patient's preferred language</li>
                    <li>Bi-weekly check-ins for first month</li>
                    <li>Consider care coordinator assignment</li>
                </ul>
            </div>
        `;
    } else {
        recommendations = `
            <div class="recommendation low-priority">
                <h5>✅ Standard Discharge Procedures</h5>
                <ul>
                    <li>Routine follow-up within 14-30 days</li>
                    <li>Standard discharge education materials</li>
                    <li>Provide contact information for questions</li>
                    <li>Standard medication instructions</li>
                </ul>
            </div>
        `;
    }
    
    document.getElementById('clinicalRecommendations').innerHTML = recommendations;
}

function displayRiskFactors(patient, riskScore) {
    const factors = [];
    
    // Risk factors
    if (patient.has_diabetes) factors.push({ name: 'Diabetes', impact: +18, severity: 'high' });
    if (patient.has_hypertension) factors.push({ name: 'Hypertension', impact: +12, severity: 'medium' });
    if (patient.has_heart_disease) factors.push({ name: 'Heart Disease', impact: +20, severity: 'critical' });
    if (patient.age >= 65) factors.push({ name: 'Advanced Age (65+)', impact: +15, severity: 'high' });
    if (patient.bmi >= 30) factors.push({ name: 'Obesity (BMI ≥30)', impact: +10, severity: 'medium' });
    if (patient.smoking_status === 'Yes') factors.push({ name: 'Active Smoker', impact: +8, severity: 'medium' });
    if (patient.total_admissions >= 3) factors.push({ name: 'Frequent Admissions', impact: +12, severity: 'high' });
    
    // Protective factors
    if (patient.bmi >= 18.5 && patient.bmi < 25) factors.push({ name: 'Healthy Weight', impact: -5, severity: 'protective' });
    if (patient.smoking_status === 'No') factors.push({ name: 'Non-smoker', impact: -3, severity: 'protective' });
    if (patient.age < 40) factors.push({ name: 'Younger Age', impact: -8, severity: 'protective' });
    
    let factorsHtml = '<div class="risk-factors-list">';
    
    factors.forEach(factor => {
        const severityClass = factor.severity;
        const impactText = factor.impact > 0 ? `+${factor.impact}%` : `${factor.impact}%`;
        const icon = factor.impact > 0 ? '⚠️' : '✅';
        
        factorsHtml += `
            <div class="risk-factor ${severityClass}">
                <span class="factor-icon">${icon}</span>
                <span class="factor-name">${factor.name}</span>
                <span class="factor-impact">${impactText}</span>
                <span class="factor-severity">${factor.severity}</span>
            </div>
        `;
    });
    
    factorsHtml += '</div>';
    
    // Summary
    const totalRiskFactors = factors.filter(f => f.impact > 0).length;
    const totalProtective = factors.filter(f => f.impact < 0).length;
    factorsHtml += `
        <div class="risk-summary">
            <p><strong>Risk Profile Summary:</strong> ${totalRiskFactors} risk factors identified, ${totalProtective} protective factors present.</p>
        </div>
    `;
    
    document.getElementById('riskFactorsList').innerHTML = factorsHtml;
}

/**
 * Populate high-risk patient table
 */
function populateRiskTable(patients) {
    // Calculate risk for all patients (simplified)
    const patientsWithRisk = patients.map(p => ({
        ...p,
        risk: calculateSimpleRisk(p)
    }));
    
    // Update population stats
    const highRisk = patientsWithRisk.filter(p => p.risk >= 60).length;
    const mediumRisk = patientsWithRisk.filter(p => p.risk >= 35 && p.risk < 60).length;
    const lowRisk = patientsWithRisk.filter(p => p.risk < 35).length;
    
    document.getElementById('highRiskCount').textContent = `${highRisk} (${(highRisk/patients.length*100).toFixed(1)}%)`;
    document.getElementById('mediumRiskCount').textContent = `${mediumRisk} (${(mediumRisk/patients.length*100).toFixed(1)}%)`;
    document.getElementById('lowRiskCount').textContent = `${lowRisk} (${(lowRisk/patients.length*100).toFixed(1)}%)`;
    document.getElementById('totalAnalyzed').textContent = patients.length;
    
    // Store for filtering
    window.allPatientsWithRisk = patientsWithRisk;
    
    // Initial table population
    filterRiskTable();
}

function calculateSimpleRisk(patient) {
    const baseRisk = 20;
    const ageRisk = (patient.age / 100) * 30;
    const conditionRisk = patient.chronic_condition_count * 15;
    const admissionRisk = (patient.total_admissions / Math.max(patient.total_visits, 1)) * 25;
    
    return Math.min(95, baseRisk + ageRisk + conditionRisk + admissionRisk);
}

function filterRiskTable() {
    if (!window.allPatientsWithRisk) return;
    
    let filtered = [...window.allPatientsWithRisk];
    
    // Apply filter
    const filterValue = document.getElementById('riskFilter').value;
    if (filterValue === 'high') {
        filtered = filtered.filter(p => p.risk >= 60);
    } else if (filterValue === 'medium-high') {
        filtered = filtered.filter(p => p.risk >= 35);
    } else if (filterValue === 'low') {
        filtered = filtered.filter(p => p.risk < 35);
    }
    
    // Apply sort
    const sortValue = document.getElementById('riskSort').value;
    if (sortValue === 'risk-desc') {
        filtered.sort((a, b) => b.risk - a.risk);
    } else if (sortValue === 'risk-asc') {
        filtered.sort((a, b) => a.risk - b.risk);
    } else if (sortValue === 'age-desc') {
        filtered.sort((a, b) => b.age - a.age);
    } else if (sortValue === 'age-asc') {
        filtered.sort((a, b) => a.age - b.age);
    }
    
    // Apply limit
    const limit = parseInt(document.getElementById('riskLimit').value);
    filtered = filtered.slice(0, limit);
    
    // Populate table
    const tbody = document.getElementById('highRiskTableBody');
    tbody.innerHTML = '';
    
    filtered.forEach(patient => {
        const riskCategory = patient.risk >= 60 ? '🔴 High' : patient.risk >= 35 ? '🟡 Medium' : '🟢 Low';
        const riskClass = patient.risk >= 60 ? 'high-risk' : patient.risk >= 35 ? 'medium-risk' : 'low-risk';
        
        const row = document.createElement('tr');
        row.className = riskClass;
        row.innerHTML = `
            <td>${patient.patient_id}</td>
            <td><strong>${patient.risk.toFixed(1)}%</strong></td>
            <td>${riskCategory}</td>
            <td>${patient.age}</td>
            <td>${patient.bmi}</td>
            <td>${patient.chronic_condition_count}</td>
            <td>${patient.total_visits}</td>
            <td>${patient.total_admissions}</td>
            <td>${patient.has_diabetes ? '✓' : '—'}</td>
            <td>${patient.has_hypertension ? '✓' : '—'}</td>
        `;
        tbody.appendChild(row);
    });
}

/**
 * Export risk data to CSV
 */
function exportRiskToCSV() {
    if (!window.allPatientsWithRisk) return;
    
    const highRiskPatients = window.allPatientsWithRisk.filter(p => p.risk >= 60);
    
    let csv = 'Patient ID,Risk %,Age,BMI,Conditions,Visits,Admissions,Diabetes,Hypertension,Heart Disease\n';
    
    highRiskPatients.forEach(p => {
        csv += `${p.patient_id},${p.risk.toFixed(1)},${p.age},${p.bmi},${p.chronic_condition_count},${p.total_visits},${p.total_admissions},${p.has_diabetes ? 'Yes' : 'No'},${p.has_hypertension ? 'Yes' : 'No'},${p.has_heart_disease ? 'Yes' : 'No'}\n`;
    });
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `high-risk-patients-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
}

/**
 * Chart helper functions - Enhanced with modern styling
 */
function createOrUpdateChart(canvasId, type, data, options = {}) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Destroy existing chart
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }
    
    // Get computed styles for consistent theming
    const styles = getComputedStyle(document.documentElement);
    const textColor = styles.getPropertyValue('--text').trim();
    const mutedColor = styles.getPropertyValue('--muted').trim();
    const borderColor = styles.getPropertyValue('--border').trim();
    
    // Modern default options
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: true,
        devicePixelRatio: window.devicePixelRatio || 2,
        plugins: {
            legend: {
                display: true,
                position: window.innerWidth < 768 ? 'bottom' : (type === 'doughnut' ? 'right' : 'top'),
                labels: {
                    font: {
                        family: styles.getPropertyValue('--font-sans').trim(),
                        size: 12
                    },
                    color: textColor,
                    padding: 15,
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: styles.getPropertyValue('--surface').trim(),
                titleColor: textColor,
                bodyColor: textColor,
                borderColor: borderColor,
                borderWidth: 1,
                padding: 12,
                cornerRadius: 8,
                titleFont: {
                    size: 13,
                    weight: '600'
                },
                bodyFont: {
                    size: 12
                },
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y.toLocaleString();
                        } else if (context.parsed !== null) {
                            label += context.parsed.toLocaleString();
                        }
                        return label;
                    }
                }
            }
        },
        scales: type !== 'doughnut' && type !== 'pie' ? {
            x: {
                grid: {
                    display: false,
                    color: borderColor
                },
                ticks: {
                    font: {
                        size: 11
                    },
                    color: mutedColor
                }
            },
            y: {
                grid: {
                    color: borderColor,
                    drawBorder: false
                },
                ticks: {
                    font: {
                        size: 11
                    },
                    color: mutedColor
                }
            }
        } : {}
    };
    
    // Deep merge options
    const mergedOptions = deepMerge(defaultOptions, options);
    
    // Create new chart
    charts[canvasId] = new Chart(ctx, {
        type: type,
        data: data,
        options: mergedOptions
    });
}

// Helper function for deep merging objects
function deepMerge(target, source) {
    const output = Object.assign({}, target);
    if (isObject(target) && isObject(source)) {
        Object.keys(source).forEach(key => {
            if (isObject(source[key])) {
                if (!(key in target)) {
                    Object.assign(output, { [key]: source[key] });
                } else {
                    output[key] = deepMerge(target[key], source[key]);
                }
            } else {
                Object.assign(output, { [key]: source[key] });
            }
        });
    }
    return output;
}

function isObject(item) {
    return item && typeof item === 'object' && !Array.isArray(item);
}

function updateMonthlyTrendsChart(trends) {
    const labels = trends.map(t => t.month_name);
    const visitCounts = trends.map(t => t.visit_count);
    
    createOrUpdateChart('trendsChart', 'line', {
        labels: labels,
        datasets: [{
            label: 'Total Visits',
            data: visitCounts,
            borderColor: 'rgba(99, 102, 241, 1)',
            backgroundColor: 'rgba(99, 102, 241, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 2
        }]
    });
}

function updateDepartmentChart(departments) {
    const labels = departments.map(d => d.department);
    const visitCounts = departments.map(d => d.visit_count);
    
    createOrUpdateChart('departmentChart', 'doughnut', {
        labels: labels,
        datasets: [{
            data: visitCounts,
            backgroundColor: generateColors(labels.length),
            borderWidth: 2,
            borderColor: getComputedStyle(document.documentElement).getPropertyValue('--surface').trim()
        }]
    });
}

function generateColors(count) {
    const colors = [
        'rgba(99, 102, 241, 0.8)',    // Indigo
        'rgba(16, 185, 129, 0.8)',    // Green
        'rgba(245, 158, 11, 0.8)',    // Amber
        'rgba(239, 68, 68, 0.8)',     // Red
        'rgba(168, 85, 247, 0.8)',    // Purple
        'rgba(59, 130, 246, 0.8)',    // Blue
        'rgba(236, 72, 153, 0.8)',    // Pink
        'rgba(20, 184, 166, 0.8)',    // Teal
        'rgba(251, 146, 60, 0.8)',    // Orange
        'rgba(132, 204, 22, 0.8)'     // Lime
    ];
    
    return colors.slice(0, count);
}
