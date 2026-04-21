<template>
  <div class="case-list-container">
    <div class="list-header">
      <h2>法律案例列表</h2>
      <span class="case-count">共 {{ cases.length }} 个案例</span>
    </div>

    <div v-if="cases.length === 0" class="empty-state">
      <p>暂无符合条件的案例</p>
    </div>

    <div v-else class="case-list">
      <div v-for="caseItem in cases" :key="caseItem.id" class="case-card">
        <div class="case-header">
          <h3 class="case-title">{{ caseItem.title }}</h3>
          <div class="case-tags">
            <span class="tag tag-type">{{ caseItem.caseType }}</span>
            <span class="tag tag-procedure">{{ caseItem.procedure }}</span>
            <span class="tag tag-result">{{ caseItem.result }}</span>
          </div>
        </div>

        <div class="case-info">
          <div class="info-item">
            <span class="info-label">案号：</span>
            <span class="info-value">{{ caseItem.caseNumber }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">法院：</span>
            <span class="info-value">{{ caseItem.court }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">年份：</span>
            <span class="info-value">{{ caseItem.year }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">日期：</span>
            <span class="info-value">{{ caseItem.date }}</span>
          </div>
        </div>

        <div class="case-parties">
          <div class="party-item">
            <span class="party-label">原告：</span>
            <span class="party-value">{{ caseItem.parties.plaintiff }}</span>
          </div>
          <div class="party-item">
            <span class="party-label">被告：</span>
            <span class="party-value">{{ caseItem.parties.defendant }}</span>
          </div>
        </div>

        <div class="case-summary">
          <p>{{ caseItem.summary }}</p>
        </div>

        <div class="case-keywords">
          <span class="keywords-label">标签：</span>
          <span v-for="tag in caseItem.tags" :key="tag" class="keyword-tag">{{ tag }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { LegalCase } from '../types/case'

interface Props {
  cases: LegalCase[]
}

defineProps<Props>()
</script>

<style scoped>
.case-list-container {
  background: #fff;
  border-radius: 8px;
  padding: 24px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.list-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.case-count {
  font-size: 14px;
  color: #999;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #999;
}

.case-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.case-card {
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.2s;
}

.case-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-color: #409eff;
}

.case-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  gap: 16px;
}

.case-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.case-tags {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.tag {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.tag-type {
  background: #e6f7ff;
  color: #1890ff;
}

.tag-procedure {
  background: #f6ffed;
  color: #52c41a;
}

.tag-result {
  background: #fff7e6;
  color: #fa8c16;
}

.case-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
  padding: 12px;
  background: #fafafa;
  border-radius: 4px;
}

.info-item {
  display: flex;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.info-value {
  font-size: 14px;
  color: #333;
}

.case-parties {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.party-item {
  display: flex;
  gap: 4px;
}

.party-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.party-value {
  font-size: 14px;
  color: #333;
}

.case-summary {
  margin-bottom: 16px;
}

.case-summary p {
  margin: 0;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
}

.case-keywords {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.keywords-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.keyword-tag {
  padding: 4px 10px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
}
</style>
