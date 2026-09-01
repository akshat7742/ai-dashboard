<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <div>
        <div class="eyebrow"><span class="status-dot"></span> AI POWERED ANALYTICS</div>
        <h1>Analytics Dashboard</h1>
        <p class="subtitle">Monitor your business performance and get intelligent insights.</p>
      </div>
      <div class="header-badge"><span class="sparkle">✦</span> Live Insights</div>
    </header>
    <!-- KPI Cards -->
    <section v-if="summary" class="cards">
      <div class="card sales-card">
        <div class="card-top">
          <div class="icon-box sales-icon">↗</div>
          <span class="trend positive">+12.5%</span>
        </div>
        <p class="card-label">Total Sales</p>
        <h2>{{ summary.sales }}</h2>
        <div class="card-footer"><span>Compared to last month</span></div>
      </div>
      <div class="card revenue-card">
        <div class="card-top">
          <div class="icon-box revenue-icon">$</div>
          <span class="trend positive">+8.2%</span>
        </div>
        <p class="card-label">Revenue</p>
        <h2>{{ summary.revenue }}</h2>
        <div class="card-footer"><span>Compared to last month</span></div>
      </div>
      <div class="card orders-card">
        <div class="card-top">
          <div class="icon-box orders-icon">▣</div>
          <span class="trend positive">+6.4%</span>
        </div>
        <p class="card-label">Total Orders</p>
        <h2>{{ summary.orders }}</h2>
        <div class="card-footer"><span>Compared to last month</span></div>
      </div>
      <div class="card customers-card">
        <div class="card-top">
          <div class="icon-box customers-icon">♙</div>
          <span class="trend positive">+10.1%</span>
        </div>
        <p class="card-label">Customers</p>
        <h2>{{ summary.customers }}</h2>
        <div class="card-footer"><span>Compared to last month</span></div>
      </div>
    </section>
    <!-- Charts -->
    <section class="charts-grid">
      <div class="chart chart-large">
        <div class="chart-header">
          <div>
            <span class="chart-kicker">PERFORMANCE</span>
            <h2>Revenue Trend</h2>
            <p>Track your revenue growth over time</p>
          </div>
          <div class="chart-action">Last 12 months ▾</div>
        </div>
        <div class="chart-content">
          <v-chart class="chart-box" :option="lineOption" autoresize />
        </div>
      </div>
      <div class="chart chart-large">
        <div class="chart-header">
          <div>
            <span class="chart-kicker">GEOGRAPHY</span>
            <h2>Sales by Region</h2>
            <p>Understand where your sales are coming from</p>
          </div>
          <div class="chart-action">All regions ▾</div>
        </div>
        <div class="chart-content">
          <v-chart class="chart-box" :option="barOption" autoresize />
        </div>
      </div>
    </section>
    <!-- AI Assistant -->
    <section class="ai-panel">
      <div class="ai-glow"></div>
      <div class="ai-header">
        <div class="ai-title-wrapper">
          <div class="ai-icon">✦</div>
          <div>
            <span class="ai-label">AI ASSISTANT</span>
            <h2>Ask your data anything</h2>
            <p>Get instant insights, trends and explanations from your dashboard.</p>
          </div>
        </div>
        <div class="ai-status"><span></span> AI Ready</div>
      </div>
      <!-- Question Input -->
      <div class="ai-input-wrapper">
        <div class="input-icon">✨</div>
        <input
          v-model="question"
          type="text"
          placeholder="Ask something about your dashboard..."
          @keyup.enter="askQuestion"
        />
        <button
          class="ask-button"
          :disabled="aiStore.loading || !question?.trim()"
          @click="askQuestion"
        >
          <span v-if="aiStore.loading" class="spinner"></span>
          <span> {{ aiStore.loading ? 'Analyzing...' : 'Ask AI' }} </span>
          <span v-if="!aiStore.loading" class="arrow">→</span>
        </button>
      </div>
      <!-- AI Answer -->
      <div v-if="aiStore.answer" class="ai-answer">
        <div class="answer-icon">✦</div>
        <div class="answer-content">
          <div class="answer-header">
            <h3>AI Analysis</h3>
            <span>Just now</span>
          </div>
          <p>{{ aiStore.answer }}</p>
        </div>
      </div>
      <!-- Empty State -->
      <div v-else-if="!aiStore.loading" class="ai-suggestions">
        <span>Try asking:</span>
        <button @click="question = 'What is my best performing region?'">
          Best performing region
        </button>
        <button @click="question = 'How is revenue trending?'">Revenue trend</button>
        <button @click="question = 'Which metric needs attention?'">What needs attention?</button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useDashboardStore } from '../stores/dashboard'

import { useAiStore } from '@/stores/aiStore'

const aiStore = useAiStore()

const question = ref('')

const askQuestion = async () => {
  await aiStore.askQuestion(question.value)
}

const store = useDashboardStore()

onMounted(() => {
  store.loadDashboard()
})

const summary = computed(() => store.summary)

const lineOption = computed(() => ({
  tooltip: {},
  xAxis: {
    type: 'category',
    data: store.monthlySales.map((x: any) => x.month),
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      type: 'line',
      data: store.monthlySales.map((x: any) => x.sales),
      smooth: true,
    },
  ],
}))

const barOption = computed(() => ({
  tooltip: {},
  xAxis: {
    type: 'category',
    data: store.regions.map((x: any) => x.name),
  },
  yAxis: {
    type: 'value',
  },
  series: [
    {
      type: 'bar',
      data: store.regions.map((x: any) => x.sales),
    },
  ],
}))
</script>

<style scoped>
/* ======================================== Dashboard ======================================== */
.dashboard {
  min-height: 100vh;
  padding: 40px;
  color: #e8eefc;
  background:
    radial-gradient(circle at 10% 0%, rgba(99, 102, 241, 0.18), transparent 30%),
    radial-gradient(circle at 90% 10%, rgba(14, 165, 233, 0.12), transparent 25%), #080b16;
  font-family:
    Inter,
    ui-sans-serif,
    system-ui,
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;
} /* ======================================== Header ======================================== */
.dashboard-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 30px;
  margin-bottom: 36px;
}
.eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  color: #8b9cff;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.16em;
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #6ee7b7;
  box-shadow: 0 0 12px #6ee7b7;
}
.dashboard-header h1 {
  margin: 0;
  font-size: clamp(32px, 4vw, 48px);
  line-height: 1.05;
  letter-spacing: -0.04em;
  background: linear-gradient(135deg, #ffffff 20%, #aebcff 70%, #7dd3fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.subtitle {
  margin: 12px 0 0;
  color: #7f8aa7;
  font-size: 15px;
}
.header-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  border: 1px solid rgba(129, 140, 248, 0.2);
  border-radius: 999px;
  background: rgba(99, 102, 241, 0.08);
  color: #aeb8ff;
  font-size: 12px;
  font-weight: 700;
}
.sparkle {
  color: #8b9cff;
  font-size: 15px;
} /* ======================================== KPI Cards ======================================== */
.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 22px;
}
.card {
  position: relative;
  overflow: hidden;
  min-height: 185px;
  padding: 22px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(30, 36, 58, 0.92), rgba(15, 18, 31, 0.92));
  box-shadow:
    0 20px 45px rgba(0, 0, 0, 0.18),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
  transition:
    transform 0.25s ease,
    border-color 0.25s ease,
    box-shadow 0.25s ease;
}
.card::after {
  content: '';
  position: absolute;
  width: 130px;
  height: 130px;
  right: -60px;
  bottom: -70px;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.12);
  filter: blur(20px);
}
.card:hover {
  transform: translateY(-4px);
  border-color: rgba(129, 140, 248, 0.25);
  box-shadow:
    0 25px 55px rgba(0, 0, 0, 0.25),
    0 0 30px rgba(99, 102, 241, 0.05);
}
.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.icon-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 13px;
  font-size: 18px;
  font-weight: 800;
}
.sales-icon {
  color: #8b9cff;
  background: rgba(99, 102, 241, 0.14);
}
.revenue-icon {
  color: #67e8f9;
  background: rgba(6, 182, 212, 0.12);
}
.orders-icon {
  color: #c084fc;
  background: rgba(168, 85, 247, 0.12);
}
.customers-icon {
  color: #6ee7b7;
  background: rgba(16, 185, 129, 0.12);
}
.trend {
  padding: 5px 9px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}
.positive {
  color: #6ee7b7;
  background: rgba(16, 185, 129, 0.1);
}
.card-label {
  margin: 22px 0 5px;
  color: #7f8aa7;
  font-size: 13px;
  font-weight: 600;
}
.card h2 {
  margin: 0;
  color: #f8fafc;
  font-size: 30px;
  letter-spacing: -0.03em;
}
.card-footer {
  margin-top: 9px;
  color: #59647e;
  font-size: 11px;
} /* ======================================== Charts ======================================== */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 18px;
}
.chart {
  min-width: 0;
  padding: 25px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 20px;
  background: linear-gradient(145deg, rgba(23, 28, 47, 0.94), rgba(12, 15, 27, 0.94));
  box-shadow:
    0 20px 45px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.03);
}
.chart-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
}
.chart-kicker {
  color: #727e9c;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.14em;
}
.chart-header h2 {
  margin: 6px 0 4px;
  color: #f1f5f9;
  font-size: 20px;
  letter-spacing: -0.025em;
}
.chart-header p {
  margin: 0;
  color: #68738d;
  font-size: 12px;
}
.chart-action {
  padding: 8px 11px;
  border: 1px solid rgba(148, 163, 184, 0.12);
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.025);
  color: #7f8aa7;
  font-size: 11px;
  white-space: nowrap;
}
.chart-content {
  height: 320px;
  margin-top: 18px;
}
.chart-box {
  width: 100%;
  height: 100%;
} /* ======================================== AI Panel ======================================== */
.ai-panel {
  position: relative;
  overflow: hidden;
  margin-top: 22px;
  padding: 28px;
  border: 1px solid rgba(129, 140, 248, 0.18);
  border-radius: 24px;
  background: linear-gradient(135deg, rgba(34, 39, 73, 0.95), rgba(16, 20, 37, 0.96));
  box-shadow:
    0 25px 60px rgba(0, 0, 0, 0.25),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}
.ai-glow {
  position: absolute;
  width: 280px;
  height: 280px;
  top: -180px;
  right: 5%;
  border-radius: 50%;
  background: rgba(99, 102, 241, 0.18);
  filter: blur(50px);
  pointer-events: none;
}
.ai-header {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 22px;
}
.ai-title-wrapper {
  display: flex;
  align-items: center;
  gap: 15px;
}
.ai-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border: 1px solid rgba(165, 180, 252, 0.2);
  border-radius: 15px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(168, 85, 247, 0.18));
  color: #b8c1ff;
  font-size: 22px;
  box-shadow: 0 0 25px rgba(99, 102, 241, 0.15);
}
.ai-label {
  color: #8f9cff;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.16em;
}
.ai-header h2 {
  margin: 3px 0;
  color: #f8fafc;
  font-size: 20px;
}
.ai-header p {
  margin: 0;
  color: #707b96;
  font-size: 12px;
}
.ai-status {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 7px 10px;
  border: 1px solid rgba(52, 211, 153, 0.12);
  border-radius: 999px;
  color: #6ee7b7;
  background: rgba(16, 185, 129, 0.06);
  font-size: 11px;
  font-weight: 700;
}
.ai-status span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #34d399;
  box-shadow: 0 0 10px #34d399;
} /* ======================================== AI Input ======================================== */
.ai-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  padding: 7px;
  border: 1px solid rgba(148, 163, 184, 0.13);
  border-radius: 15px;
  background: rgba(4, 7, 17, 0.55);
  transition:
    border-color 0.2s ease,
    box-shadow 0.2s ease;
}
.ai-input-wrapper:focus-within {
  border-color: rgba(129, 140, 248, 0.45);
  box-shadow:
    0 0 0 4px rgba(99, 102, 241, 0.06),
    0 0 25px rgba(99, 102, 241, 0.08);
}
.input-icon {
  width: 42px;
  color: #8b9cff;
  text-align: center;
  font-size: 16px;
}
.ai-input-wrapper input {
  flex: 1;
  min-width: 0;
  padding: 13px 8px;
  border: none;
  outline: none;
  background: transparent;
  color: #e5e7eb;
  font-size: 14px;
}
.ai-input-wrapper input::placeholder {
  color: #56617a;
}
.ask-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 9px;
  min-width: 112px;
  padding: 12px 16px;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-size: 12px;
  font-weight: 800;
  cursor: pointer;
  box-shadow: 0 8px 20px rgba(99, 102, 241, 0.25);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease,
    opacity 0.2s ease;
}
.ask-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 12px 28px rgba(99, 102, 241, 0.35);
}
.ask-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.arrow {
  font-size: 16px;
}
.spinner {
  width: 13px;
  height: 13px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
} /* ======================================== AI Answer ======================================== */
.ai-answer {
  display: flex;
  gap: 15px;
  margin-top: 18px;
  padding: 20px;
  border: 1px solid rgba(129, 140, 248, 0.12);
  border-radius: 15px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.07), rgba(255, 255, 255, 0.018));
  animation: answerIn 0.35s ease;
}
@keyframes answerIn {
  from {
    opacity: 0;
    transform: translateY(7px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.answer-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: rgba(99, 102, 241, 0.14);
  color: #a5b4fc;
}
.answer-content {
  min-width: 0;
}
.answer-header {
  display: flex;
  align-items: center;
  gap: 10px;
}
.answer-header h3 {
  margin: 0;
  color: #eef2ff;
  font-size: 13px;
}
.answer-header span {
  color: #59647d;
  font-size: 10px;
}
.answer-content p {
  margin: 8px 0 0;
  color: #9ca8c0;
  font-size: 13px;
  line-height: 1.7;
  white-space: pre-wrap;
} /* ======================================== AI Suggestions ======================================== */
.ai-suggestions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 15px;
  color: #59647d;
  font-size: 11px;
}
.ai-suggestions button {
  padding: 7px 10px;
  border: 1px solid rgba(148, 163, 184, 0.1);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.025);
  color: #77829b;
  font-size: 10px;
  cursor: pointer;
  transition:
    color 0.2s ease,
    border-color 0.2s ease,
    background 0.2s ease;
}
.ai-suggestions button:hover {
  color: #b7c0ff;
  border-color: rgba(129, 140, 248, 0.25);
  background: rgba(99, 102, 241, 0.08);
} /* ======================================== Responsive ======================================== */
@media (max-width: 1100px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 700px) {
  .dashboard {
    padding: 22px 15px;
  }
  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
  }
  .header-badge {
    display: none;
  }
  .cards {
    grid-template-columns: 1fr;
  }
  .chart {
    padding: 18px;
  }
  .chart-header {
    flex-direction: column;
  }
  .chart-action {
    display: none;
  }
  .chart-content {
    height: 260px;
  }
  .ai-panel {
    padding: 20px 15px;
  }
  .ai-header {
    align-items: flex-start;
    flex-direction: column;
  }
  .ai-status {
    display: none;
  }
  .ai-input-wrapper {
    padding: 6px;
  }
  .input-icon {
    display: none;
  }
  .ai-input-wrapper input {
    padding-left: 10px;
  }
  .ask-button {
    min-width: 92px;
    padding: 11px 12px;
  }
  .ai-suggestions {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
