<template>
  <div class="diagnosis-view">
    <div class="page-header">
      <h2>企业法律健康智能诊断</h2>
      <p>我们与资深律师合作，将初创公司最常见的五大类法律风险，沉淀为一个10分钟的智能诊断模型</p>
    </div>

    <div v-if="!isCompleted" class="diagnosis-container">
      <div class="progress-section">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
        </div>
        <div class="progress-text">第 {{ currentIndex + 1 }} / {{ totalQuestions }} 题</div>
      </div>

      <div class="question-card">
        <div class="question-number">问题 {{ currentQuestion.order }}</div>
        <h3 class="question-text">{{ currentQuestion.question }}</h3>
        <p v-if="currentQuestion.hint" class="question-hint">💡 {{ currentQuestion.hint }}</p>

        <div v-if="currentQuestion.type === 'single'" class="options-list">
          <button
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            class="option-btn"
            :class="{ selected: answers[currentQuestion.id] === option }"
            @click="selectAnswer(option)"
          >
            {{ option }}
          </button>
        </div>

        <div v-if="currentQuestion.type === 'text'" class="text-input-wrapper">
          <input
            v-model="answers[currentQuestion.id]"
            type="text"
            placeholder="请输入您的答案..."
            class="text-input"
            @input="onTextInput"
          />
        </div>

        <div v-if="currentIndex > 0 && showWarning" class="warning-box">
          <span class="warning-icon">⚠️</span>
          <span class="warning-text">这个选择可能存在法律风险，建议您关注</span>
        </div>

        <div class="button-group">
          <button v-if="currentIndex > 0" class="nav-btn prev" @click="prevQuestion">
            ← 上一题
          </button>
          <button
            v-if="currentIndex < totalQuestions - 1"
            class="nav-btn next"
            :disabled="!hasAnswer"
            @click="nextQuestion"
          >
            下一题 →
          </button>
          <button
            v-else
            class="nav-btn submit"
            :disabled="!hasAnswer"
            @click="submitDiagnosis"
          >
            生成诊断报告
          </button>
        </div>
      </div>
    </div>

    <div v-else class="completed-container">
      <div class="completed-icon">✅</div>
      <h3>问卷已完成！</h3>
      <p>正在为您生成诊断报告...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { diagnosisQuestions, riskLibrary } from '../data/mockDiagnosis'
import type { DiagnosisAnswer, DiagnosisResult } from '../types/diagnosis'

const router = useRouter()
const currentIndex = ref(0)
const answers = ref<Record<string, string>>({})
const isCompleted = ref(false)
const showWarning = ref(false)

const totalQuestions = diagnosisQuestions.length

const currentQuestion = computed(() => diagnosisQuestions[currentIndex.value])

const progressPercent = computed(() => ((currentIndex.value + 1) / totalQuestions) * 100)

const hasAnswer = computed(() => {
  return !!answers.value[currentQuestion.value.id]
})

const checkRisk = (questionId: string, answer: string) => {
  const question = diagnosisQuestions.find(q => q.id === questionId)
  if (!question || question.type !== 'single') return false

  const optionIndex = question.options?.indexOf(answer)
  if (optionIndex === undefined) return false

  const riskKey = `${questionId}-${optionIndex}`
  return !!riskLibrary[riskKey]
}

const selectAnswer = (option: string) => {
  answers.value[currentQuestion.value.id] = option
  showWarning.value = checkRisk(currentQuestion.value.id, option)
}

const onTextInput = () => {
  showWarning.value = false
}

const nextQuestion = () => {
  if (currentIndex.value < totalQuestions - 1) {
    currentIndex.value++
    showWarning.value = checkRisk(currentQuestion.value.id, answers.value[currentQuestion.value.id] || '')
  }
}

const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    showWarning.value = checkRisk(currentQuestion.value.id, answers.value[currentQuestion.value.id] || '')
  }
}

const submitDiagnosis = () => {
  isCompleted.value = true

  setTimeout(() => {
    let score = 100
    const risks: any[] = []
    const companyName = answers.value['q1'] || '您的公司'

    diagnosisQuestions.forEach((question, qIndex) => {
      const answer = answers.value[question.id]
      if (question.type === 'single' && answer) {
        const optionIndex = question.options?.indexOf(answer)
        if (optionIndex !== undefined) {
          const riskKey = `${question.id}-${optionIndex}`
          const riskInfo = riskLibrary[riskKey]
          if (riskInfo) {
            score -= riskInfo.scoreImpact
            risks.push({
              id: riskKey,
              title: riskInfo.title,
              description: riskInfo.description.replace('您的公司', companyName),
              level: riskInfo.level,
              scoreImpact: riskInfo.scoreImpact
            })
          }
        }
      }
    })

    score = Math.max(score, 40)

    const result: DiagnosisResult = {
      score,
      risks,
      companyName,
      summary: generateSummary(score, risks, companyName),
      suggestions: generateSuggestions(risks)
    }

    router.push({
      name: 'Report',
      state: { diagnosisResult: result }
    })
  }, 1500)
}

const generateSummary = (score: number, risks: any[], companyName: string) => {
  const highRisks = risks.filter(r => r.level === '高')
  const hasHighRisk = highRisks.length > 0

  if (score >= 80) {
    return `${companyName}的法律健康状况总体良好，但仍有${risks.length}个需要关注的风险点，建议及时处理。`
  } else if (score >= 60) {
    return `${companyName}存在${risks.length}个法律风险点，其中${hasHighRisk ? highRisks.length + '个高风险问题' : ''}需要优先处理，建议尽快完善。`
  } else {
    return `${companyName}的法律健康状况堪忧，发现${risks.length}个风险点，其中${hasHighRisk ? highRisks.length + '个高风险问题' : ''}亟待解决，建议立即采取行动。`
  }
}

const generateSuggestions = (risks: any[]) => {
  const suggestions: string[] = []
  const highRisks = risks.filter(r => r.level === '高').slice(0, 2)

  highRisks.forEach(risk => {
    if (risk.title.includes('股权')) {
      suggestions.push('建议咨询专业律师，优化公司股权结构，建立有效的决策机制。')
    } else if (risk.title.includes('商标')) {
      suggestions.push('立即开展商标查询，尽快申请商标注册，保护品牌资产。')
    } else if (risk.title.includes('合同')) {
      suggestions.push('对重要交易补签书面合同，明确双方权利义务。')
    } else if (risk.title.includes('劳动')) {
      suggestions.push('尽快与所有员工签订劳动合同并缴纳社保，避免劳动仲裁风险。')
    }
  })

  if (suggestions.length === 0) {
    suggestions.push('建议建立常态化的法律风险排查机制，防患于未然。')
  }

  return suggestions
}
</script>

<style scoped>
.diagnosis-view {
  max-width: 700px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.page-header p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.progress-section {
  margin-bottom: 24px;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  text-align: center;
  font-size: 13px;
  color: #888;
}

.question-card {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.question-number {
  display: inline-block;
  padding: 6px 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 16px;
}

.question-text {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
  line-height: 1.4;
}

.question-hint {
  font-size: 14px;
  color: #fa8c16;
  background: #fff7e6;
  padding: 10px 14px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.option-btn {
  padding: 16px 20px;
  background: #f8f9fa;
  border: 2px solid transparent;
  border-radius: 10px;
  font-size: 15px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.option-btn:hover {
  background: #f0f0f0;
}

.option-btn.selected {
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f5ff 100%);
  border-color: #667eea;
  color: #667eea;
  font-weight: 600;
}

.text-input-wrapper {
  margin-bottom: 24px;
}

.text-input {
  width: 100%;
  padding: 16px 20px;
  border: 2px solid #f0f0f0;
  border-radius: 10px;
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
}

.text-input:focus {
  border-color: #667eea;
}

.warning-box {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: #fff1f0;
  border: 1px solid #ffa39e;
  border-radius: 8px;
  margin-bottom: 24px;
}

.warning-icon {
  font-size: 20px;
}

.warning-text {
  font-size: 14px;
  color: #ff4d4f;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.nav-btn {
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.nav-btn.prev {
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  color: #666;
}

.nav-btn.prev:hover {
  background: #e8e8e8;
}

.nav-btn.next,
.nav-btn.submit {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: #fff;
}

.nav-btn.next:hover:not(:disabled),
.nav-btn.submit:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.completed-container {
  background: #fff;
  border-radius: 16px;
  padding: 60px 32px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.completed-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 0.6s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.completed-container h3 {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.completed-container p {
  font-size: 15px;
  color: #666;
}
</style>
