<template>
  <div class="home-view">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">律界法宝</h1>
      <p class="hero-subtitle">为初创企业提供全方位的法律智能服务，助力企业健康发展</p>
        <div class="hero-buttons">
          <router-link to="/diagnosis" class="btn primary">开始智能诊断</router-link>
          <router-link to="/knowledge" class="btn secondary">浏览法律知识库</router-link>
        </div>
      </div>
      <div class="hero-image">
        <img src="/logo.png" alt="律界法宝logo" class="hero-graphic" />
      </div>
    </div>

    <div class="features-section">
      <h2 class="section-title">核心功能</h2>
      <div class="features-grid">
        <router-link to="/knowledge" class="feature-card">
          <div class="feature-icon">📚</div>
          <h3 class="feature-title">法律知识库</h3>
          <p class="feature-desc">涵盖公司法、合同法、劳动法等58部法律法规，提供分类查询和全文检索</p>
        </router-link>
        <router-link to="/process" class="feature-card">
          <div class="feature-icon">🔄</div>
          <h3 class="feature-title">法律流程查询</h3>
          <p class="feature-desc">多维度筛选工商、知识产权、融资等业务流程，详细步骤和材料清单</p>
        </router-link>
        <router-link to="/ai" class="feature-card">
          <div class="feature-icon">🤖</div>
          <h3 class="feature-title">AI 智能助手</h3>
          <p class="feature-desc">智能文档生成、合规审查、法律问答，提升您的工作效率</p>
        </router-link>
        <router-link to="/diagnosis" class="feature-card">
          <div class="feature-icon">📊</div>
          <h3 class="feature-title">智能法律诊断</h3>
          <p class="feature-desc">10分钟快速诊断，精准定位企业法律风险，生成专业诊断报告</p>
        </router-link>
        <router-link to="/chat" class="feature-card">
          <div class="feature-icon">💬</div>
          <h3 class="feature-title">律师咨询</h3>
          <p class="feature-desc">与专业律师一对一沟通，获取专业的法律意见和建议</p>
        </router-link>
        <router-link to="/projects" class="feature-card">
          <div class="feature-icon">📂</div>
          <h3 class="feature-title">项目协同空间</h3>
          <p class="feature-desc">律师与客户高效协作，文件管理、任务分配、沟通记录全留存</p>
        </router-link>
      </div>
    </div>

    <div class="quick-section">
      <h2 class="section-title">快捷入口</h2>
      <div class="quick-grid">
        <div class="quick-item" @click="goToPage('/diagnosis')">
          <span class="quick-icon">🎯</span>
          <span class="quick-text">立即诊断</span>
        </div>
        <div class="quick-item" @click="goToPage('/knowledge')">
          <span class="quick-icon">📖</span>
          <span class="quick-text">查法律</span>
        </div>
        <div class="quick-item" @click="goToPage('/process')">
          <span class="quick-icon">📋</span>
          <span class="quick-text">看流程</span>
        </div>
        <div class="quick-item" @click="goToPage('/ai')">
          <span class="quick-icon">✨</span>
          <span class="quick-text">用AI</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToPage = (path: string) => {
  router.push(path)
}
</script>

<style scoped>
.home-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.hero-section {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 48px;
  align-items: center;
  padding: 48px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  margin-bottom: 48px;
}

.hero-title {
  font-size: 40px;
  font-weight: 800;
  color: #fff;
  margin-bottom: 16px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 32px;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 16px;
}

.btn {
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn.primary {
  background: #fff;
  color: #667eea;
}

.btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 255, 255, 0.3);
}

.btn.secondary {
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.btn.secondary:hover {
  background: rgba(255, 255, 255, 0.25);
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-graphic {
  max-width: 300px;
  max-height: 300px;
  object-fit: contain;
  opacity: 0.95;
}

.features-section {
  margin-bottom: 48px;
}

.section-title {
  font-size: 28px;
  font-weight: 800;
  color: #333;
  text-align: center;
  margin-bottom: 32px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.feature-card {
  padding: 32px 24px;
  background: #fff;
  border-radius: 16px;
  text-decoration: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
}

.feature-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.7;
}

.quick-section {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.quick-item {
  padding: 24px;
  background: linear-gradient(135deg, #f5f7ff 0%, #f0f5ff 100%);
  border-radius: 12px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-item:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.quick-item:hover .quick-icon,
.quick-item:hover .quick-text {
  color: #fff;
}

.quick-icon {
  font-size: 32px;
  display: block;
  margin-bottom: 8px;
  transition: all 0.2s;
}

.quick-text {
  font-size: 15px;
  font-weight: 600;
  color: #667eea;
  transition: all 0.2s;
}

@media (max-width: 968px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-buttons {
    justify-content: center;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .quick-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .features-grid {
    grid-template-columns: 1fr;
  }

  .quick-grid {
    grid-template-columns: 1fr;
  }
}
</style>
