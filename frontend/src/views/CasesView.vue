<template>
  <div class="cases-view">
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <template v-else>
      <CaseFilter :filter-options="filterOptions" @filter="handleFilter" />
      <CaseList :cases="filteredCases" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import CaseFilter from '../components/CaseFilter.vue'
import CaseList from '../components/CaseList.vue'
import { caseApi } from '../services/api'
import type { LegalCase, FilterOptions as ApiFilterOptions } from '../services/api'
import type { FilterOptions } from '../types/case'

const allCases = ref<LegalCase[]>([])
const filterOptions = ref<FilterOptions>({
  caseTypes: [],
  courts: [],
  procedures: [],
  years: [],
  results: []
})
const loading = ref(true)
const error = ref('')
const currentFilters = ref({
  caseTypes: [] as string[],
  courts: [] as string[],
  procedures: [] as string[],
  years: [] as number[],
  results: [] as string[],
  keyword: ''
})

const filteredCases = computed(() => {
  return allCases.value.filter(caseItem => {
    if (currentFilters.value.caseTypes.length > 0 && !currentFilters.value.caseTypes.includes(caseItem.caseType)) {
      return false
    }
    if (currentFilters.value.courts.length > 0 && !currentFilters.value.courts.includes(caseItem.court)) {
      return false
    }
    if (currentFilters.value.procedures.length > 0 && !currentFilters.value.procedures.includes(caseItem.procedure)) {
      return false
    }
    if (currentFilters.value.years.length > 0 && !currentFilters.value.years.includes(caseItem.year)) {
      return false
    }
    if (currentFilters.value.results.length > 0 && !currentFilters.value.results.includes(caseItem.result)) {
      return false
    }
    if (currentFilters.value.keyword) {
      const keyword = currentFilters.value.keyword.toLowerCase()
      const matchTitle = caseItem.title.toLowerCase().includes(keyword)
      const matchSummary = caseItem.summary.toLowerCase().includes(keyword)
      const matchTags = caseItem.tags.some(tag => tag.toLowerCase().includes(keyword))
      const matchParties = caseItem.parties.plaintiff.toLowerCase().includes(keyword) || caseItem.parties.defendant.toLowerCase().includes(keyword)
      if (!matchTitle && !matchSummary && !matchTags && !matchParties) {
        return false
      }
    }
    return true
  })
})

const loadData = async () => {
  try {
    loading.value = true
    error.value = ''
    // 首先尝试使用新的API端点获取与前端期望一致的数据结构
    const legalCases = await caseApi.getLegalCases()
    allCases.value = legalCases
    
    // 尝试获取过滤选项
    try {
      const filters = await caseApi.getFilterOptions()
      filterOptions.value = filters
    } catch (filterErr) {
      // 如果获取过滤选项失败，使用默认选项
      console.warn('获取过滤选项失败，使用默认选项:', filterErr)
      filterOptions.value = {
        caseTypes: ['合同纠纷', '劳动争议', '知识产权', '公司纠纷'],
        courts: ['北京市第一中级人民法院', '上海市第二中级人民法院', '深圳市中级人民法院'],
        procedures: ['一审', '二审', '再审'],
        years: [2024, 2023, 2022],
        results: ['原告胜诉', '被告胜诉', '调解结案']
      }
    }
  } catch (err) {
    console.error('加载数据失败:', err)
    error.value = '加载数据失败，请确保后端服务已启动'
  } finally {
    loading.value = false
  }
}

const handleFilter = (filters: typeof currentFilters.value) => {
  currentFilters.value = { ...filters }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.cases-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.loading, .error {
  text-align: center;
  padding: 64px 24px;
  font-size: 18px;
  color: #666;
}

.error {
  color: #e74c3c;
}
</style>
