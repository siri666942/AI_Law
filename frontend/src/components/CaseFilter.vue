<template>
  <div class="filter-container">
    <div class="filter-section">
      <h3>案件类型</h3>
      <div class="filter-options">
        <label v-for="type in filterOptions.caseTypes" :key="type" class="filter-option">
          <input
            type="checkbox"
            :value="type"
            v-model="filters.caseTypes"
            @change="emitFilters"
          />
          <span>{{ type }}</span>
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h3>审理法院</h3>
      <div class="filter-options">
        <label v-for="court in filterOptions.courts" :key="court" class="filter-option">
          <input
            type="checkbox"
            :value="court"
            v-model="filters.courts"
            @change="emitFilters"
          />
          <span>{{ court }}</span>
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h3>审理程序</h3>
      <div class="filter-options">
        <label v-for="procedure in filterOptions.procedures" :key="procedure" class="filter-option">
          <input
            type="checkbox"
            :value="procedure"
            v-model="filters.procedures"
            @change="emitFilters"
          />
          <span>{{ procedure }}</span>
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h3>年份</h3>
      <div class="filter-options">
        <label v-for="year in filterOptions.years" :key="year" class="filter-option">
          <input
            type="checkbox"
            :value="year"
            v-model="filters.years"
            @change="emitFilters"
          />
          <span>{{ year }}</span>
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h3>裁判结果</h3>
      <div class="filter-options">
        <label v-for="result in filterOptions.results" :key="result" class="filter-option">
          <input
            type="checkbox"
            :value="result"
            v-model="filters.results"
            @change="emitFilters"
          />
          <span>{{ result }}</span>
        </label>
      </div>
    </div>

    <div class="filter-section">
      <h3>关键词搜索</h3>
      <input
        type="text"
        v-model="filters.keyword"
        placeholder="输入关键词搜索..."
        @input="emitFilters"
        class="search-input"
      />
    </div>

    <button @click="resetFilters" class="reset-btn">重置筛选</button>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import type { FilterOptions } from '../types/case'

interface Props {
  filterOptions: FilterOptions
}

const props = defineProps<Props>()

interface Filters {
  caseTypes: string[]
  courts: string[]
  procedures: string[]
  years: number[]
  results: string[]
  keyword: string
}

const filters = reactive<Filters>({
  caseTypes: [],
  courts: [],
  procedures: [],
  years: [],
  results: [],
  keyword: ''
})

const emit = defineEmits<{
  (e: 'filter', filters: Filters): void
}>()

const emitFilters = () => {
  emit('filter', { ...filters })
}

const resetFilters = () => {
  filters.caseTypes = []
  filters.courts = []
  filters.procedures = []
  filters.years = []
  filters.results = []
  filters.keyword = ''
  emitFilters()
}
</script>

<style scoped>
.filter-container {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-section h3 {
  margin: 0 0 12px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
  color: #555;
}

.filter-option input {
  cursor: pointer;
}

.search-input {
  width: 100%;
  max-width: 400px;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: #409eff;
}

.reset-btn {
  padding: 10px 20px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: all 0.2s;
}

.reset-btn:hover {
  border-color: #409eff;
  color: #409eff;
}
</style>
