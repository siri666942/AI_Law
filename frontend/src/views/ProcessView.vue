<template>
  <div class="process-view">
    <div class="page-header">
      <h2>法律流程查询</h2>
      <p>了解各类法律业务的办理流程、所需材料和注意事项</p>
    </div>

    <div class="filter-section">
      <div class="filter-grid">
        <div class="filter-item">
          <label>业务类型</label>
          <select v-model="filters.businessType">
            <option value="">全部</option>
            <option v-for="t in filterOptions.businessTypes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
        <div class="filter-item">
          <label>主体类型</label>
          <select v-model="filters.entityType">
            <option value="">全部</option>
            <option v-for="t in filterOptions.entityTypes" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
        <div class="filter-item">
          <label>所属行业</label>
          <select v-model="filters.industry">
            <option value="">全部</option>
            <option v-for="i in filterOptions.industries" :key="i" :value="i">{{ i }}</option>
          </select>
        </div>
        <div class="filter-item">
          <label>所在地区</label>
          <select v-model="filters.region">
            <option value="">全部</option>
            <option v-for="r in filterOptions.regions" :key="r" :value="r">{{ r }}</option>
          </select>
        </div>
        <div class="filter-item">
          <label>办理场景</label>
          <select v-model="filters.scenario">
            <option value="">全部</option>
            <option v-for="s in filterOptions.scenarios" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>
        <div class="filter-item">
          <button class="reset-btn" @click="resetFilters">重置</button>
        </div>
      </div>
    </div>

    <div class="process-list">
      <div v-if="filteredProcesses.length === 0" class="empty-state">
        <p>暂无符合条件的流程</p>
      </div>
      <div
        v-for="process in filteredProcesses"
        :key="process.id"
        class="process-card"
        @click="showProcessDetail(process)"
      >
        <div class="process-header">
          <div class="process-title">
            <h3>{{ process.title }}</h3>
            <div class="process-meta">
              <span class="meta-tag">{{ process.businessType }}</span>
              <span class="meta-tag">{{ process.entityType }}</span>
              <span class="meta-tag">{{ process.industry }}</span>
              <span class="difficulty" :class="process.difficulty">{{ process.difficulty }}</span>
            </div>
          </div>
          <div class="process-time">
            <div class="time-label">预计周期</div>
            <div class="time-value">{{ process.estimatedTime }}</div>
          </div>
        </div>
        <p class="process-desc">{{ process.description }}</p>
        <div class="process-footer">
          <div class="process-steps">
            <span class="steps-count">{{ process.steps.length }} 个步骤</span>
            <span class="materials-count">{{ process.materials.length }} 份材料</span>
          </div>
          <div class="view-detail">查看详情 →</div>
        </div>
      </div>
    </div>

    <div v-if="currentProcess" class="modal-overlay" @click="closeDetail">
      <div class="process-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ currentProcess.title }}</h3>
          <button class="close-btn" @click="closeDetail">×</button>
        </div>
        <div class="modal-body">
          <div class="modal-summary">
            <div class="summary-item">
              <span class="label">业务类型</span>
              <span class="value">{{ currentProcess.businessType }}</span>
            </div>
            <div class="summary-item">
              <span class="label">主体类型</span>
              <span class="value">{{ currentProcess.entityType }}</span>
            </div>
            <div class="summary-item">
              <span class="label">所属行业</span>
              <span class="value">{{ currentProcess.industry }}</span>
            </div>
            <div class="summary-item">
              <span class="label">所在地区</span>
              <span class="value">{{ currentProcess.region }}</span>
            </div>
            <div class="summary-item">
              <span class="label">办理场景</span>
              <span class="value">{{ currentProcess.scenario }}</span>
            </div>
            <div class="summary-item">
              <span class="label">预计周期</span>
              <span class="value">{{ currentProcess.estimatedTime }}</span>
            </div>
            <div class="summary-item">
              <span class="label">难度等级</span>
              <span class="value difficulty" :class="currentProcess.difficulty">{{ currentProcess.difficulty }}</span>
            </div>
          </div>

          <div class="section">
            <h4>办理流程</h4>
            <div class="steps-timeline">
              <div v-for="step in currentProcess.steps" :key="step.order" class="step-item">
                <div class="step-number">{{ step.order }}</div>
                <div class="step-content">
                  <h5>{{ step.title }}</h5>
                  <p>{{ step.description }}</p>
                  <div class="step-meta">
                    <span v-if="step.duration" class="step-duration">⏱ {{ step.duration }}</span>
                    <span v-if="step.tips" class="step-tips">💡 {{ step.tips }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="section">
            <h4>所需材料</h4>
            <ul class="materials-list">
              <li v-for="(material, index) in currentProcess.materials" :key="index">
                📋 {{ material }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { mockProcesses, processFilterOptions } from '../data/mockProcess'
import type { LegalProcess, ProcessFilters } from '../types/process'

const filters = ref<ProcessFilters>({
  businessType: '',
  entityType: '',
  industry: '',
  region: '',
  scenario: ''
})

const currentProcess = ref<LegalProcess | null>(null)
const filterOptions = processFilterOptions

const filteredProcesses = computed(() => {
  return mockProcesses.filter(process => {
    if (filters.value.businessType && process.businessType !== filters.value.businessType) return false
    if (filters.value.entityType && process.entityType !== filters.value.entityType) return false
    if (filters.value.industry && process.industry !== filters.value.industry) return false
    if (filters.value.region && process.region !== filters.value.region) return false
    if (filters.value.scenario && process.scenario !== filters.value.scenario) return false
    return true
  })
})

const resetFilters = () => {
  filters.value = {
    businessType: '',
    entityType: '',
    industry: '',
    region: '',
    scenario: ''
  }
}

const showProcessDetail = (process: LegalProcess) => {
  currentProcess.value = process
}

const closeDetail = () => {
  currentProcess.value = null
}
</script>

<style scoped>
.process-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h2 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.page-header p {
  font-size: 14px;
  color: #666;
}

.filter-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  align-items: end;
}

.filter-item label {
  display: block;
  font-size: 13px;
  color: #666;
  margin-bottom: 6px;
  font-weight: 500;
}

.filter-item select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: all 0.2s;
}

.filter-item select:focus {
  border-color: #667eea;
}

.reset-btn {
  padding: 10px 24px;
  background: #f5f5f5;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.reset-btn:hover {
  background: #e8e8e8;
}

.process-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-state {
  background: #fff;
  border-radius: 12px;
  padding: 60px 24px;
  text-align: center;
  color: #999;
  font-size: 15px;
}

.process-card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.process-card:hover {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.process-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  gap: 24px;
}

.process-title h3 {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.process-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.meta-tag {
  padding: 4px 12px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}

.difficulty {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
}

.difficulty.简单 {
  background: #e6f7ff;
  color: #1890ff;
}

.difficulty.中等 {
  background: #fff7e6;
  color: #fa8c16;
}

.difficulty.复杂 {
  background: #fff1f0;
  color: #ff4d4f;
}

.process-time {
  text-align: right;
  flex-shrink: 0;
}

.time-label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.time-value {
  font-size: 16px;
  font-weight: 700;
  color: #667eea;
}

.process-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
}

.process-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.process-steps {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: #888;
}

.view-detail {
  color: #667eea;
  font-size: 14px;
  font-weight: 500;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 24px;
}

.process-modal {
  background: #fff;
  border-radius: 16px;
  max-width: 900px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
}

.modal-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  margin: 0;
  flex: 1;
  padding-right: 16px;
}

.close-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  line-height: 1;
}

.close-btn:hover {
  background: #e8e8e8;
  color: #333;
}

.modal-body {
  padding: 24px;
}

.modal-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f5ff 100%);
  border-radius: 12px;
  margin-bottom: 28px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.summary-item .label {
  font-size: 12px;
  color: #888;
}

.summary-item .value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.section {
  margin-bottom: 32px;
}

.section h4 {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.steps-timeline {
  position: relative;
  padding-left: 40px;
}

.step-item {
  position: relative;
  padding-bottom: 32px;
}

.step-item:last-child {
  padding-bottom: 0;
}

.step-item::before {
  content: '';
  position: absolute;
  left: -32px;
  top: 36px;
  bottom: 0;
  width: 2px;
  background: #e8e8e8;
}

.step-item:last-child::before {
  display: none;
}

.step-number {
  position: absolute;
  left: -40px;
  top: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}

.step-content h5 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.step-content p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 12px;
}

.step-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.step-duration,
.step-tips {
  font-size: 13px;
  color: #888;
}

.materials-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.materials-list li {
  padding: 12px 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #333;
}
</style>
