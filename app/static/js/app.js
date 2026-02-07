// Customer Segmentation Prediction - Frontend JavaScript

// API base URL
const API_BASE = "/api/v1";

// Update range input display values
function updateRangeValue(inputId, displayId) {
  const input = document.getElementById(inputId);
  const display = document.getElementById(displayId);

  if (input && display) {
    display.textContent = input.value;
    input.addEventListener("input", (e) => {
      display.textContent = e.target.value;
    });
  }
}

// Initialize range inputs
document.addEventListener("DOMContentLoaded", () => {
  updateRangeValue("income", "incomeValue");
  updateRangeValue("spending", "spendingValue");
});

// Predict customer segment
async function predictSegment(event) {
  event.preventDefault();

  const submitBtn = document.getElementById("submitBtn");
  const resultDiv = document.getElementById("result");
  const errorDiv = document.getElementById("error");

  // Get form values
  const annualIncome = parseFloat(document.getElementById("income").value);
  const spendingScore = parseInt(document.getElementById("spending").value);

  // Validate inputs
  if (isNaN(annualIncome) || isNaN(spendingScore)) {
    showError("Please enter valid values");
    return;
  }

  // Show loading state
  submitBtn.disabled = true;
  submitBtn.innerHTML = '<span class="loading"></span> Analyzing...';
  resultDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");

  try {
    // Make API call
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        annual_income: annualIncome,
        spending_score: spendingScore,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Prediction failed");
    }

    const data = await response.json();
    displayResult(data);
  } catch (error) {
    console.error("Error:", error);
    showError(error.message);
  } finally {
    // Reset button
    submitBtn.disabled = false;
    submitBtn.innerHTML = "Predict Segment";
  }
}

// Display prediction result
function displayResult(data) {
  const resultDiv = document.getElementById("result");

  // Get cluster color
  const clusterColors = {
    0: "#8b5cf6", // Purple - Average
    1: "#ef4444", // Red - VIP
    2: "#f59e0b", // Orange - Young Trendsetter
    3: "#10b981", // Green - High Earner Saver
    4: "#3b82f6", // Blue - Budget Conscious
  };

  const color = clusterColors[data.cluster_id] || "#667eea";

  resultDiv.innerHTML = `
        <div class="result-card" style="background: linear-gradient(135deg, ${color} 0%, ${color}dd 100%);">
            <div class="result-header">
                <h2>Customer Segment Identified</h2>
                <div class="cluster-badge">${data.cluster_name}</div>
                <p style="opacity: 0.9;">Cluster ID: ${data.cluster_id}</p>
            </div>
            
            <div class="info-grid">
                <div class="info-item">
                    <div class="icon">$</div>
                    <div class="label">Annual Income</div>
                    <div class="value">$${data.annual_income}k</div>
                </div>
                <div class="info-item">
                    <div class="icon">Chart</div>
                    <div class="label">Spending Score</div>
                    <div class="value">${data.spending_score}/100</div>
                </div>
            </div>
            
            <div class="result-section">
                <h3>Description</h3>
                <p>${data.description}</p>
            </div>
            
            <div class="result-section">
                <h3>Marketing Strategy</h3>
                <p>${data.marketing_strategy}</p>
            </div>
        </div>
    `;

  resultDiv.classList.remove("hidden");

  // Smooth scroll to result
  resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// Show error message
function showError(message) {
  const errorDiv = document.getElementById("error");
  errorDiv.innerHTML = `
        <div class="alert alert-danger">
            <strong>Error:</strong> ${message}
        </div>
    `;
  errorDiv.classList.remove("hidden");
}

// Load cluster statistics (for about page)
async function loadClusterStats() {
  try {
    const response = await fetch(`${API_BASE}/clusters`);
    if (!response.ok) throw new Error("Failed to load statistics");

    const stats = await response.json();
    displayClusterStats(stats);
  } catch (error) {
    console.error("Error loading stats:", error);
  }
}

// Display cluster statistics
function displayClusterStats(stats) {
  const container = document.getElementById("clusterStats");
  if (!container) return;

  container.innerHTML = stats
    .map(
      (stat) => `
        <div class="cluster-card">
            <h3>${stat.cluster_name}</h3>
            <p><strong>Customers:</strong> ${stat.count}</p>
            <p><strong>Avg Income:</strong> $${stat.avg_income}k</p>
            <p><strong>Avg Spending Score:</strong> ${stat.avg_spending_score}/100</p>
            ${stat.avg_age ? `<p><strong>Avg Age:</strong> ${stat.avg_age} years</p>` : ""}
        </div>
    `,
    )
    .join("");
}

// Load model info
async function loadModelInfo() {
  try {
    const response = await fetch(`${API_BASE}/model/info`);
    if (!response.ok) throw new Error("Failed to load model info");

    const info = await response.json();
    displayModelInfo(info);
  } catch (error) {
    console.error("Error loading model info:", error);
  }
}

// Display model info
function displayModelInfo(info) {
  const container = document.getElementById("modelInfo");
  if (!container) return;

  const statusBadge = info.model_loaded
    ? '<span style="color: #10b981;">Loaded</span>'
    : '<span style="color: #ef4444;">Not Loaded</span>';

  container.innerHTML = `
        <div class="info-grid">
            <div class="info-item">
                <div class="label">Model Type</div>
                <div class="value">${info.model_type}</div>
            </div>
            <div class="info-item">
                <div class="label">Number of Clusters</div>
                <div class="value">${info.n_clusters}</div>
            </div>
            <div class="info-item">
                <div class="label">Status</div>
                <div class="value">${statusBadge}</div>
            </div>
        </div>
    `;
}

// Auto-load stats and info on about page
if (window.location.pathname === "/about") {
  document.addEventListener("DOMContentLoaded", () => {
    loadClusterStats();
    loadModelInfo();
  });
}
