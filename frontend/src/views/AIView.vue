<template>
  <div class="ai-view">
    <div class="page-header">
      <h2>AI 智能助手</h2>
      <p>智能化文档生成、合规审查、法律问答，提升您的工作效率</p>
    </div>

    <div class="ai-layout">
      <div class="function-sidebar">
        <div
          v-for="func in functions"
          :key="func.id"
          class="function-item"
          :class="{ active: activeFunction === func.id }"
          @click="activeFunction = func.id"
        >
          <div class="func-icon">{{ func.icon }}</div>
          <div class="func-info">
            <div class="func-name">{{ func.name }}</div>
            <div class="func-desc">{{ func.description }}</div>
          </div>
        </div>
      </div>

      <div class="function-content">
        <div v-if="activeFunction === 'document'" class="document-section">
          <div class="section-header">
            <h3>标准化文档生成</h3>
            <p>选择文档类型，快速生成标准化法律文档初稿</p>
          </div>
          <div class="document-templates">
            <div
              v-for="tpl in documentTemplates"
              :key="tpl.id"
              class="template-card"
              @click="selectTemplate(tpl)"
            >
              <div class="tpl-icon">{{ tpl.icon }}</div>
              <div class="tpl-name">{{ tpl.name }}</div>
              <div class="tpl-desc">{{ tpl.description }}</div>
            </div>
          </div>
        </div>

        <div v-if="activeFunction === 'review'" class="review-section">
          <div class="section-header">
            <h3>合规性初筛与风险提示</h3>
            <p>上传合同或文档，AI 将自动进行合规性初步审查</p>
          </div>
          <div class="upload-area" @click="triggerUpload" @dragover.prevent @drop.prevent="handleDrop">
            <input type="file" ref="fileInput" @change="handleFileChange" accept=".doc,.docx,.pdf,.txt" style="display: none" />
            <div class="upload-icon">📄</div>
            <div class="upload-text">
              <div class="upload-title">点击或拖拽文件到此处上传</div>
              <div class="upload-hint">支持 .doc .docx .pdf .txt 格式</div>
            </div>
          </div>
          <div v-if="reviewResult" class="review-result">
            <h4>风险审查结果</h4>
            <div class="risk-list">
              <div v-for="(risk, index) in reviewResult.risks" :key="index" class="risk-item" :class="risk.level">
                <span class="risk-level">{{ risk.level === '高' ? '🔴' : risk.level === '中' ? '🟡' : '🟢' }}</span>
                <span class="risk-text">{{ risk.text }}</span>
              </div>
            </div>
            <div class="suggestions">
              <h5>💡 修改建议</h5>
              <ul>
                <li v-for="(suggestion, index) in reviewResult.suggestions" :key="index">{{ suggestion }}</li>
              </ul>
            </div>
          </div>
        </div>

        <div v-if="activeFunction === 'qa'" class="qa-section">
          <div class="chat-container">
            <div class="chat-messages" ref="chatMessagesRef">
              <div class="welcome-message">
                <div class="welcome-icon">🤖</div>
                <h4>您好，我是您的法律智能助手</h4>
                <p>我可以为您提供法律知识咨询、法律流程解答等服务。请问有什么可以帮助您的？</p>
                <div class="quick-questions">
                  <button v-for="q in quickQuestions" :key="q" @click="sendQuickQuestion(q)" class="quick-btn">{{ q }}</button>
                </div>
              </div>
              <div
                v-for="(msg, index) in chatMessages"
                :key="index"
                class="chat-message"
                :class="msg.role"
              >
                <div class="msg-avatar">{{ msg.role === 'user' ? '👤' : '🤖' }}</div>
                <div class="msg-content">
                  <div class="msg-text">{{ msg.content }}</div>
                </div>
              </div>
              <div v-if="isTyping" class="chat-message ai">
                <div class="msg-avatar">🤖</div>
                <div class="msg-content typing">
                  <span></span><span></span><span></span>
                </div>
              </div>
            </div>
            <div class="chat-input-area">
              <textarea
                v-model="userInput"
                placeholder="输入您的法律问题..."
                @keydown.enter.prevent="sendMessage"
                rows="1"
              ></textarea>
              <button @click="sendMessage" :disabled="!userInput.trim() || isTyping" class="send-btn">
                发送
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { aiApi } from '../services/api'

const activeFunction = ref('qa')
const fileInput = ref<HTMLInputElement>()
const chatMessages = ref<Array<{ role: 'user' | 'ai'; content: string }>>([])
const userInput = ref('')
const isTyping = ref(false)
const chatMessagesRef = ref<HTMLElement>()
const reviewResult = ref<any>(null)

const functions = [
  { id: 'document', name: '文档生成', description: '标准化文档起草', icon: '📝' },
  { id: 'review', name: '合规审查', description: '风险提示与建议', icon: '🔍' },
  { id: 'qa', name: '法律问答', description: '智能法律咨询', icon: '💬' }
]

const documentTemplates = [
  { id: '1', name: '劳动合同', description: '标准版劳动合同模板', icon: '📄' },
  { id: '2', name: '买卖合同', description: '货物采购合同模板', icon: '🛒' },
  { id: '3', name: '保密协议', description: 'NDA保密协议模板', icon: '🔒' },
  { id: '4', name: '公司章程', description: '有限责任公司章程', icon: '🏢' },
  { id: '5', name: '授权委托书', description: '授权委托文书模板', icon: '📋' },
  { id: '6', name: '股东会决议', description: '股东会决议模板', icon: '📊' }
]

const quickQuestions = [
  '公司设立需要哪些材料？',
  '劳动合同有哪些必备条款？',
  '商标注册流程是怎样的？',
  '如何保护商业秘密？'
]

const aiResponses: Record<string, string> = {
  '公司设立需要哪些材料？': '公司设立通常需要以下材料：\n\n1. 股东身份证明文件\n2. 公司章程\n3. 注册地址证明（房产证或租赁合同）\n4. 法定代表人身份证明\n5. 企业名称预先核准通知书\n\n具体要求可能因地区而异，建议咨询当地市场监督管理部门。',
  '劳动合同有哪些必备条款？': '根据《劳动合同法》规定，劳动合同应当具备以下必备条款：\n\n1. 用人单位的名称、住所和法定代表人\n2. 劳动者的姓名、住址和居民身份证号\n3. 劳动合同期限\n4. 工作内容和工作地点\n5. 工作时间和休息休假\n6. 劳动报酬\n7. 社会保险\n8. 劳动保护、劳动条件和职业危害防护\n9. 法律、法规规定应当纳入劳动合同的其他事项',
  '商标注册流程是怎样的？': '商标注册流程大致如下：\n\n1. 商标查询（评估注册风险）\n2. 准备申请材料\n3. 提交注册申请\n4. 形式审查（1-2个月）\n5. 实质审查（6-9个月）\n6. 初审公告（3个月异议期）\n7. 注册公告及发证\n\n整个流程通常需要12-18个月。',
  '如何保护商业秘密？': '保护商业秘密可以从以下几个方面入手：\n\n1. 明确商业秘密范围，进行密级划分\n2. 与员工、合作伙伴签订保密协议\n3. 采取物理和技术保密措施\n4. 建立内部保密管理制度\n5. 定期进行保密培训\n6. 发现泄密及时采取法律手段\n\n建议委托专业律师制定完整的商业秘密保护方案。'
}

const selectTemplate = (tpl: any) => {
  alert(`您选择了：${tpl.name}\n\n功能演示：实际使用时，系统将引导您填写相关信息并生成文档初稿。`)
}

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  if (target.files && target.files[0]) {
    simulateReview()
  }
}

const handleDrop = () => {
  simulateReview()
}

const simulateReview = () => {
  reviewResult.value = {
    risks: [
      { level: '高', text: '合同中缺少违约责任条款，建议补充' },
      { level: '中', text: '争议解决方式约定不够明确' },
      { level: '低', text: '建议明确合同生效条件' }
    ],
    suggestions: [
      '建议在合同中明确约定违约金计算方式',
      '建议明确约定由原告所在地法院管辖',
      '建议增加合同附件清单条款'
    ]
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (chatMessagesRef.value) {
      chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
    }
  })
}

const sendQuickQuestion = (question: string) => {
  userInput.value = question
  sendMessage()
}

const sendMessage = async () => {
  if (!userInput.value.trim() || isTyping.value) return

  const question = userInput.value
  chatMessages.value.push({ role: 'user', content: question })
  userInput.value = ''
  isTyping.value = true
  scrollToBottom()

  try {
    const answer = await aiApi.ask(question)
    chatMessages.value.push({ role: 'ai', content: answer || '未从模型获得有效回复。' })
  } catch (error: any) {
    const message = error?.message || '调用 AI 模型失败，请稍后重试。'
    chatMessages.value.push({ role: 'ai', content: message })
  } finally {
    isTyping.value = false
    scrollToBottom()
  }
}
</script>

<style scoped>
.ai-view {
  max-width: 1400px;
  margin: 0 auto;
  padding: 24px;
  height: calc(100vh - 96px);
  display: flex;
  flex-direction: column;
}

.page-header {
  margin-bottom: 24px;
  flex-shrink: 0;
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

.ai-layout {
  display: flex;
  gap: 24px;
  flex: 1;
  min-height: 0;
}

.function-sidebar {
  width: 260px;
  flex-shrink: 0;
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.function-item {
  padding: 16px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  gap: 12px;
  align-items: center;
}

.function-item:hover {
  background: #f5f5f5;
}

.function-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.func-icon {
  font-size: 24px;
}

.func-name {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 2px;
}

.func-desc {
  font-size: 12px;
  opacity: 0.8;
}

.function-content {
  flex: 1;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow-y: auto;
}

.section-header {
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.section-header p {
  font-size: 14px;
  color: #666;
}

.document-templates {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
}

.template-card {
  padding: 24px;
  border: 2px solid #f0f0f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
}

.template-card:hover {
  border-color: #667eea;
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.tpl-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.tpl-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.tpl-desc {
  font-size: 13px;
  color: #888;
}

.upload-area {
  border: 2px dashed #d9d9d9;
  border-radius: 12px;
  padding: 60px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-area:hover {
  border-color: #667eea;
  background: #f5f7ff;
}

.upload-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.upload-title {
  font-size: 16px;
  color: #333;
  margin-bottom: 4px;
}

.upload-hint {
  font-size: 13px;
  color: #999;
}

.review-result {
  margin-top: 24px;
  padding: 24px;
  background: linear-gradient(135deg, #fff7f7 0%, #fff5f5 100%);
  border-radius: 12px;
}

.review-result h4 {
  font-size: 18px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.risk-list {
  margin-bottom: 20px;
}

.risk-item {
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  margin-bottom: 8px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.risk-level {
  font-size: 18px;
}

.risk-text {
  font-size: 14px;
  color: #333;
}

.suggestions {
  padding: 16px;
  background: #fff;
  border-radius: 8px;
}

.suggestions h5 {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.suggestions li {
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}

.qa-section {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding-bottom: 20px;
}

.welcome-message {
  text-align: center;
  padding: 40px 20px;
}

.welcome-icon {
  font-size: 56px;
  margin-bottom: 16px;
}

.welcome-message h4 {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 8px;
}

.welcome-message p {
  font-size: 14px;
  color: #666;
  max-width: 500px;
  margin: 0 auto 24px;
  line-height: 1.6;
}

.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.quick-btn {
  padding: 10px 20px;
  background: #f0f0f0;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: all 0.2s;
}

.quick-btn:hover {
  background: #667eea;
  color: #fff;
}

.chat-message {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.chat-message.user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.chat-message.user .msg-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.msg-content {
  max-width: 70%;
}

.chat-message.ai .msg-content {
  background: #f5f5f5;
  border-radius: 12px 12px 12px 4px;
  padding: 14px 18px;
}

.chat-message.user .msg-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 12px 12px 4px 12px;
  padding: 14px 18px;
}

.msg-text {
  font-size: 14px;
  line-height: 1.8;
  white-space: pre-wrap;
}

.typing {
  display: flex;
  gap: 4px;
  padding: 14px 18px;
}

.typing span {
  width: 8px;
  height: 8px;
  background: #999;
  border-radius: 50%;
  animation: typing 1.4s infinite;
}

.typing span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
  }
  30% {
    transform: translateY(-8px);
  }
}

.chat-input-area {
  display: flex;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
  flex-shrink: 0;
}

.chat-input-area textarea {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #f0f0f0;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  resize: none;
  outline: none;
  transition: all 0.2s;
  max-height: 120px;
}

.chat-input-area textarea:focus {
  border-color: #667eea;
}

.send-btn {
  padding: 12px 32px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
