import type { DiagnosisQuestion, RiskItem } from '../types/diagnosis'

export const diagnosisQuestions: DiagnosisQuestion[] = [
  {
    id: 'q1',
    order: 1,
    question: '您的公司名称是什么？',
    type: 'text',
    hint: '用于生成个性化诊断报告'
  },
  {
    id: 'q2',
    order: 2,
    question: '您的公司有几个创始人？股权是怎么分配的？',
    type: 'single',
    options: ['平分股权', '按出资比例分配', '其他分配方式'],
    hint: '平均分配可能导致决策僵局'
  },
  {
    id: 'q3',
    order: 3,
    question: '公司的品牌名（或核心产品名）注册商标了吗？',
    type: 'single',
    options: ['已注册', '正在申请中', '还没有'],
    hint: '未注册商标可能被他人抢注'
  },
  {
    id: 'q4',
    order: 4,
    question: '核心技术的源代码或设计文档，主要是由员工开发的吗？',
    type: 'single',
    options: ['是，都是员工开发', '部分是员工开发', '不是，主要是外部开发'],
    hint: '员工开发的技术成果归属需要明确约定'
  },
  {
    id: 'q5',
    order: 5,
    question: '和最重要的客户或供应商，有签署正式合同吗？',
    type: 'single',
    options: ['都有签署', '部分签署', '基本没有'],
    hint: '口头协议存在法律风险'
  },
  {
    id: 'q6',
    order: 6,
    question: '所有员工都签了劳动合同并缴纳社保了吗？',
    type: 'single',
    options: ['全部签署并缴纳', '大部分签署并缴纳', '部分签署或缴纳'],
    hint: '不签劳动合同可能面临双倍工资赔偿'
  },
  {
    id: 'q7',
    order: 7,
    question: '公司有制定保密制度或与员工签署保密协议吗？',
    type: 'single',
    options: ['有保密制度和协议', '只有保密协议', '都没有'],
    hint: '商业秘密需要采取保密措施才能获得法律保护'
  },
  {
    id: 'q8',
    order: 8,
    question: '公司有建立规范的财务和发票管理制度吗？',
    type: 'single',
    options: ['有完善的制度', '有基本制度', '制度不完善'],
    hint: '财税不合规可能面临行政处罚'
  }
]

export const riskLibrary: Record<string, Omit<RiskItem, 'id'>> = {
  'q2-0': {
    title: '股权结构隐患',
    description: '平均分配股权容易导致公司决策僵局，建议调整股权架构或建立有效的决策机制。',
    level: '高',
    scoreImpact: 15
  },
  'q3-2': {
    title: '商标未注册',
    description: '品牌未注册商标，存在被他人抢注的风险，建议尽快申请商标注册。',
    level: '高',
    scoreImpact: 12
  },
  'q4-0': {
    title: '职务作品权属风险',
    description: '员工开发的技术成果需要明确约定权属，建议完善知识产权归属协议。',
    level: '中',
    scoreImpact: 8
  },
  'q5-2': {
    title: '合同缺失风险',
    description: '重要交易未签署书面合同，发生纠纷时难以维权，建议补签书面合同。',
    level: '高',
    scoreImpact: 14
  },
  'q6-2': {
    title: '劳动用工不合规',
    description: '未签劳动合同或未缴社保，可能面临双倍工资、补缴社保等法律责任。',
    level: '高',
    scoreImpact: 18
  },
  'q7-2': {
    title: '商业秘密保护缺失',
    description: '未采取保密措施，商业秘密难以获得法律保护，建议完善保密制度。',
    level: '中',
    scoreImpact: 10
  },
  'q8-2': {
    title: '财税管理不规范',
    description: '财务和发票管理制度不完善，可能面临税务合规风险，建议规范财务管理。',
    level: '中',
    scoreImpact: 8
  }
}
