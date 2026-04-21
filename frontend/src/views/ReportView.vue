<template>
  <div class="report-view">
    <div v-if="!diagnosisResult" class="no-report">
      <div class="no-report-icon">📋</div>
      <h3>暂无诊断报告</h3>
      <p>请先完成智能诊断问卷</p>
      <router-link to="/diagnosis" class="start-btn">开始诊断</router-link>
    </div>

    <div v-else class="report-container">
      <div class="report-header">
        <div class="header-left">
          <h2>企业法律健康诊断报告</h2>
          <p class="report-subtitle">为 {{ diagnosisResult.companyName }} 生成 · {{ currentDate }}</p>
        </div>
        <div class="header-right">
          <button class="action-btn secondary" @click="printReport">
            🖨️ 打印报告
          </button>
          <button class="action-btn primary" @click="createProject">
            📂 创建项目
          </button>
        </div>
      </div>

      <div class="score-section">
        <div class="score-card">
          <div class="score-circle" :class="scoreLevel">
            <div class="score-number">{{ diagnosisResult.score }}</div>
            <div class="score-label">健康分</div>
          </div>
          <div class="score-info">
            <div class="score-level-text" :class="scoreLevel">{{ scoreText }}</div>
            <div class="score-summary">{{ diagnosisResult.summary }}</div>
          </div>
        </div>
      </div>

      <div class="risks-section">
        <div class="section-title">
          <span class="title-icon">⚠️</span>
          <h3>风险清单</h3>
          <span class="risk-count">发现 {{ diagnosisResult.risks.length }} 个风险点</span>
        </div>
        <div class="risks-list">
          <div
            v-for="risk in diagnosisResult.risks"
            :key="risk.id"
            class="risk-item"
            :class="risk.level"
          >
            <div class="risk-level-badge" :class="risk.level">
              {{ risk.level }}
            </div>
            <div class="risk-content">
              <div class="risk-title">{{ risk.title }}</div>
              <div class="risk-desc">{{ risk.description }}</div>
            </div>
            <div class="score-impact">
              -{{ risk.scoreImpact }}分
            </div>
          </div>
        </div>
        <div v-if="diagnosisResult.risks.length === 0" class="no-risk">
          <div class="no-risk-icon">🎉</div>
          <p>太棒了！未发现明显的法律风险</p>
        </div>
      </div>

      <div class="suggestions-section">
        <div class="section-title">
          <span class="title-icon">💡</span>
          <h3>行动建议</h3>
        </div>
        <div class="suggestions-list">
          <div v-for="(suggestion, index) in diagnosisResult.suggestions" :key="index" class="suggestion-item">
            <div class="suggestion-number">{{ index + 1 }}</div>
            <div class="suggestion-content">{{ suggestion }}</div>
          </div>
        </div>
      </div>

      <div class="cta-section">
        <div class="cta-card">
          <div class="cta-icon">🤝</div>
          <div class="cta-content">
            <h4>需要专业律师帮助？</h4>
            <p>我们的专业律师团队可以为您提供一对一咨询服务</p>
          </div>
          <div class="cta-buttons">
            <router-link to="/chat" class="cta-btn chat">咨询律师</router-link>
            <router-link to="/diagnosis" class="cta-btn recheck">重新诊断</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { DiagnosisResult } from '../types/diagnosis'

const router = useRouter()
const route = useRoute()
const diagnosisResult = ref<DiagnosisResult | null>(null)
const currentDate = ref('')

onMounted(() => {
  const state = route.state as any
  if (state?.diagnosisResult) {
    diagnosisResult.value = state.diagnosisResult
  } else {
    const saved = localStorage.getItem('lastDiagnosisResult')
    if (saved) {
      diagnosisResult.value = JSON.parse(saved)
    }
  }

  const now = new Date()
  currentDate.value = `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
})

const scoreLevel = computed(() => {
  if (!diagnosisResult.value) return ''
  const score = diagnosisResult.value.score
  if (score >= 80) return 'good'
  if (score >= 60) return 'medium'
  return 'warning'
})

const scoreText = computed(() => {
  if (!diagnosisResult.value) return ''
  const score = diagnosisResult.value.score
  if (score >= 80) return '法律健康状况良好'
  if (score >= 60) return '存在一定风险'
  return '风险较高，需立即处理'
})

const printReport = () => {
  window.print()
}

const createProject = () => {
  if (diagnosisResult.value) {
    localStorage.setItem('lastDiagnosisResult', JSON.stringify(diagnosisResult.value))
  }
  router.push('/projects')
}
</script>

<style scoped>
.report-view {
  max-width: 900px;
  margin: 0 auto;
  padding: 24px;
}

.no-report {
  background: #fff;
  border-radius: 16px;
  padding: 80px 24px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.no-report-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.no-report h3 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.no-report p {
  font-size: 15px;
  color: #666;
  margin-bottom: 24px;
}

.start-btn {
  display: inline-block;
  padding: 14px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  text-decoration: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.2s;
}

.start-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.report-container {
  background: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 28px 32px;
  border-bottom: 1px solid #f0f0f0;
  background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
}

.header-left h2 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 6px;
}

.report-subtitle {
  font-size: 14px;
  color: #888;
}

.header-right {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.action-btn.secondary {
  background: #f5f5f5;
  color: #666;
}

.action-btn.secondary:hover {
  background: #e8e8e8;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.score-section {
  padding: 32px;
}

.score-card {
  display: flex;
  gap: 32px;
  align-items: center;
}

.score-circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.score-circle.good {
  background: linear-gradient(135deg, #52c41a 0%, #95de64 100%);
}

.score-circle.medium {
  background: linear-gradient(135deg, #fa8c16 0%, #ffc53d 100%);
}

.score-circle.warning {
  background: linear-gradient(135deg, #ff4d4f 0%, #ff7875 100%);
}

.score-number {
  font-size: 48px;
  font-weight: 700;
  color: #fff;
  line-height: 1;
}

.score-label {
  font-size: 14px;
  color: #fff;
  opacity: 0.9;
  margin-top: 4px;
}

.score-info {
  flex: 1;
}

.score-level-text {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 12px;
}

.score-level-text.good {
  color: #52c41a;
}

.score-level-text.medium {
  color: #fa8c16;
}

.score-level-text.warning {
  color: #ff4d4f;
}

.score-summary {
  font-size: 15px;
  color: #555;
  line-height: 1.8;
}

.risks-section,
.suggestions-section {
  padding: 0 32px 32px;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.title-icon {
  font-size: 24px;
}

.section-title h3 {
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.risk-count {
  margin-left: auto;
  font-size: 14px;
  color: #888;
}

.risks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.risk-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  align-items: flex-start;
}

.risk-item.高 {
  background: linear-gradient(135deg, #fff1f0 0%, #fff5f5 100%);
  border-left: 4px solid #ff4d4f;
}

.risk-item.中 {
  background: linear-gradient(135deg, #fff7e6 0%, #fffbf0 100%);
  border-left: 4px solid #fa8c16;
}

.risk-item.低 {
  background: linear-gradient(135deg, #f6ffed 0%, #fcfff5 100%);
  border-left: 4px solid #52c41a;
}

.risk-level-badge {
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.risk-level-badge.高 {
  background: #ff4d4f;
  color: #fff;
}

.risk-level-badge.中 {
  background: #fa8c16;
  color: #fff;
}

.risk-level-badge.低 {
  background: #52c41a;
  color: #fff;
}

.risk-content {
  flex: 1;
}

.risk-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 6px;
}

.risk-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.score-impact {
  font-size: 16px;
  font-weight: 700;
  color: #ff4d4f;
  flex-shrink: 0;
}

.no-risk {
  text-align: center;
  padding: 40px 24px;
}

.no-risk-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.no-risk p {
  font-size: 15px;
  color: #52c41a;
}

.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.suggestion-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f5ff 100%);
  border-radius: 12px;
  align-items: flex-start;
}

.suggestion-number {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  flex-shrink: 0;
}

.suggestion-content {
  font-size: 15px;
  color: #333;
  line-height: 1.8;
}

.cta-section {
  padding: 0 32px 32px;
}

.cta-card {
  display: flex;
  gap: 24px;
  padding: 28px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  align-items: center;
}

.cta-icon {
  font-size: 48px;
  flex-shrink: 0;
}

.cta-content {
  flex: 1;
}

.cta-content h4 {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 6px;
}

.cta-content p {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.9);
}

.cta-buttons {
  display: flex;
  gap: 12px;
  flex-shrink: 0;
}

.cta-btn {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.cta-btn.chat {
  background: #fff;
  color: #667eea;
}

.cta-btn.chat:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.3);
}

.cta-btn.recheck {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.cta-btn.recheck:hover {
  background: rgba(255, 255, 255, 0.3);
}

@media print {
  .header-right,
  .cta-section,
  .no-print {
    display: none !important;
  }

  .report-view {
    padding: 0;
  }

  .report-container {
    box-shadow: none;
  }
}
</style>
