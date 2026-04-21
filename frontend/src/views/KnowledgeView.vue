<template>
  <div class="knowledge-view">
    <div class="page-header">
      <h2>法律知识库</h2>
      <p>全面覆盖企业经营所需的法律法规，随时查询最新内容</p>
    </div>

    <div class="search-bar">
      <input
        v-model="searchKeyword"
        type="text"
        placeholder="搜索法律法规..."
        class="search-input"
      />
    </div>

    <div class="knowledge-layout">
      <div class="category-sidebar">
        <div
          v-for="category in filteredCategories"
          :key="category.id"
          class="category-item"
          :class="{ active: selectedCategoryId === category.id }"
          @click="selectCategory(category.id)"
        >
          <div class="category-name">{{ category.name }}</div>
          <div class="category-count">{{ category.laws.length }} 部</div>
        </div>
      </div>

      <div class="laws-content">
        <div v-if="selectedCategory" class="category-detail">
          <div class="category-header">
            <h3>{{ selectedCategory.name }}</h3>
            <p>{{ selectedCategory.description }}</p>
          </div>

          <div class="laws-list">
            <div
              v-for="law in filteredLaws"
              :key="law.id"
              class="law-card"
              @click="showLawDetail(law)"
            >
              <div class="law-number">{{ law.number }}</div>
              <div class="law-info">
                <div class="law-title">{{ law.fullName }}</div>
                <div class="law-meta">
                  <span v-if="law.publishDate">发布日期：{{ law.publishDate }}</span>
                  <span v-if="law.effectiveDate">生效日期：{{ law.effectiveDate }}</span>
                </div>
                <div v-if="law.content" class="law-summary">{{ law.content }}</div>
              </div>
              <div class="law-arrow">→</div>
            </div>
          </div>
        </div>

        <div v-else class="empty-state">
          <p>请从左侧选择一个分类查看</p>
        </div>
      </div>
    </div>

    <div v-if="currentLaw" class="law-modal-overlay" @click="closeLawDetail">
      <div class="law-modal" @click.stop>
        <div class="modal-header">
          <h3>{{ currentLaw.fullName }}</h3>
          <button class="close-btn" @click="closeLawDetail">×</button>
        </div>
        <div class="modal-body">
          <div class="modal-info">
            <div v-if="currentLaw.publishDate">
              <span class="label">发布日期：</span>
              <span>{{ currentLaw.publishDate }}</span>
            </div>
            <div v-if="currentLaw.effectiveDate">
              <span class="label">生效日期：</span>
              <span>{{ currentLaw.effectiveDate }}</span>
            </div>
          </div>
          <div v-if="currentLaw.content" class="modal-content">
            <h4>法律简介</h4>
            <p>{{ currentLaw.content }}</p>
          </div>
          <div class="modal-tips">
            <p>💡 提示：本平台将持续更新最新法律法规内容，确保您获取的信息始终保持最新状态。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { lawCategories } from '../data/mockKnowledge'
import type { LawCategory, Law } from '../types/knowledge'

const searchKeyword = ref('')
const selectedCategoryId = ref<string>(lawCategories[0].id)
const currentLaw = ref<Law | null>(null)

const filteredCategories = computed(() => {
  if (!searchKeyword.value) return lawCategories
  const keyword = searchKeyword.value.toLowerCase()
  return lawCategories.filter(category =>
    category.name.toLowerCase().includes(keyword) ||
    category.laws.some(law =>
      law.name.toLowerCase().includes(keyword) ||
      law.fullName.toLowerCase().includes(keyword)
    )
  )
})

const selectedCategory = computed(() => {
  return lawCategories.find(cat => cat.id === selectedCategoryId.value)
})

const filteredLaws = computed(() => {
  if (!selectedCategory.value) return []
  if (!searchKeyword.value) return selectedCategory.value.laws
  const keyword = searchKeyword.value.toLowerCase()
  return selectedCategory.value.laws.filter(law =>
    law.name.toLowerCase().includes(keyword) ||
    law.fullName.toLowerCase().includes(keyword) ||
    (law.content && law.content.toLowerCase().includes(keyword))
  )
})

const selectCategory = (categoryId: string) => {
  selectedCategoryId.value = categoryId
}

const showLawDetail = (law: Law) => {
  currentLaw.value = law
}

const closeLawDetail = () => {
  currentLaw.value = null
}
</script>

<style scoped>
.knowledge-view {
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

.search-bar {
  margin-bottom: 24px;
}

.search-input {
  width: 100%;
  max-width: 600px;
  padding: 14px 20px;
  border: 2px solid #e8e8e8;
  border-radius: 12px;
  font-size: 15px;
  outline: none;
  transition: all 0.2s;
}

.search-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}

.knowledge-layout {
  display: flex;
  gap: 24px;
  min-height: 600px;
}

.category-sidebar {
  width: 280px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  max-height: calc(100vh - 220px);
  overflow-y: auto;
}

.category-item {
  padding: 14px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.category-item:hover {
  background: #f5f5f5;
}

.category-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.category-name {
  font-size: 14px;
  font-weight: 500;
}

.category-count {
  font-size: 12px;
  opacity: 0.8;
}

.laws-content {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  max-height: calc(100vh - 220px);
  overflow-y: auto;
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #999;
  font-size: 15px;
}

.category-header {
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.category-header h3 {
  font-size: 22px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.category-header p {
  font-size: 14px;
  color: #666;
}

.laws-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.law-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  border: 1px solid #f0f0f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  align-items: flex-start;
}

.law-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
  transform: translateY(-2px);
}

.law-number {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  flex-shrink: 0;
}

.law-info {
  flex: 1;
  min-width: 0;
}

.law-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.law-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
  font-size: 13px;
  color: #888;
}

.law-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
}

.law-arrow {
  font-size: 20px;
  color: #999;
  transition: all 0.2s;
}

.law-card:hover .law-arrow {
  color: #667eea;
  transform: translateX(4px);
}

.law-modal-overlay {
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

.law-modal {
  background: #fff;
  border-radius: 16px;
  max-width: 700px;
  width: 100%;
  max-height: 80vh;
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
}

.modal-header h3 {
  font-size: 20px;
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

.modal-info {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 24px;
}

.modal-info > div {
  font-size: 14px;
}

.modal-info .label {
  color: #888;
  margin-right: 4px;
}

.modal-content {
  margin-bottom: 24px;
}

.modal-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.modal-content p {
  font-size: 14px;
  color: #555;
  line-height: 1.8;
}

.modal-tips {
  padding: 16px;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f5ff 100%);
  border-radius: 8px;
}

.modal-tips p {
  margin: 0;
  font-size: 14px;
  color: #667eea;
}
</style>
