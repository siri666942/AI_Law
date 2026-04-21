import type { LegalProcess } from '../types/process'

export const processFilterOptions = {
  businessTypes: ['公司设立', '变更登记', '注销清算', '知识产权申请', '资质许可', '融资合规', '劳动用工备案', '跨境业务'],
  entityTypes: ['有限责任公司', '股份有限公司', '合伙企业', '个人独资企业', '个体工商户', '外商投资企业'],
  industries: ['科技/软件', '文化传媒', '教育培训', '医疗健康', '电子商务', '金融服务', '制造业'],
  regions: ['国家', '北京市', '上海市', '广东省', '浙江省', '江苏省'],
  scenarios: ['首次办理', '延期/变更', '补办', '注销']
}

export const mockProcesses: LegalProcess[] = [
  {
    id: 'proc1',
    title: '有限责任公司设立流程',
    description: '从名称预核准到领取营业执照的完整公司设立流程',
    businessType: '公司设立',
    entityType: '有限责任公司',
    industry: '科技/软件',
    region: '北京市',
    scenario: '首次办理',
    estimatedTime: '7-15个工作日',
    difficulty: '中等',
    steps: [
      { order: 1, title: '企业名称预先核准', description: '在市场监督管理局网上登记平台提交名称申请', duration: '1-3个工作日', tips: '建议准备3-5个备选名称' },
      { order: 2, title: '提交设立登记材料', description: '在线填写并提交公司章程、股东信息、注册地址等材料', duration: '1个工作日', tips: '确保所有股东签字完整' },
      { order: 3, title: '领取营业执照', description: '审核通过后，前往工商窗口或邮寄领取营业执照正副本', duration: '3-5个工作日', tips: '领取后及时刻制公章' },
      { order: 4, title: '刻制印章', description: '到公安局指定的刻章机构刻制公章、财务章、法人章等', duration: '1-2个工作日', tips: '需要营业执照原件' },
      { order: 5, title: '银行开户', description: '选择银行开立企业基本存款账户', duration: '5-7个工作日', tips: '提前预约银行客户经理' },
      { order: 6, title: '税务报到', description: '到税务局完成税务登记、税种核定、申领发票', duration: '3-5个工作日', tips: '需在领取营业执照30日内办理' }
    ],
    materials: [
      '股东身份证明文件',
      '公司章程',
      '注册地址证明（房产证或租赁合同）',
      '法定代表人身份证明',
      '企业名称预先核准通知书'
    ]
  },
  {
    id: 'proc2',
    title: '商标注册申请流程',
    description: '商标从查询到下证的完整注册流程',
    businessType: '知识产权申请',
    entityType: '有限责任公司',
    industry: '科技/软件',
    region: '国家',
    scenario: '首次办理',
    estimatedTime: '12-18个月',
    difficulty: '复杂',
    steps: [
      { order: 1, title: '商标查询', description: '在中国商标网进行近似查询，评估注册风险', duration: '1-3个工作日', tips: '建议委托专业代理机构进行详细查询' },
      { order: 2, title: '准备申请材料', description: '确定商标标识、指定商品/服务类别、准备主体资格证明', duration: '1-2个工作日', tips: '建议注册第35类广告销售类' },
      { order: 3, title: '提交申请', description: '通过商标局官网或委托代理机构提交注册申请', duration: '1个工作日', tips: '可同时申请多个类别' },
      { order: 4, title: '形式审查', description: '商标局对申请材料进行形式审查', duration: '1-2个月', tips: '材料无误将下发受理通知书' },
      { order: 5, title: '实质审查', description: '商标局进行实质审查，检查是否存在近似商标', duration: '6-9个月', tips: '此阶段最为关键，可能被驳回' },
      { order: 6, title: '初审公告', description: '通过实质审查后进入3个月异议期', duration: '3个月', tips: '无人异议将进入下一阶段' },
      { order: 7, title: '注册公告及发证', description: '异议期结束无异议，颁发商标注册证书', duration: '1-2个月', tips: '商标有效期10年' }
    ],
    materials: [
      '商标标识图样',
      '主体资格证明（营业执照）',
      '商标注册申请书',
      '代理委托书（如委托代理机构）'
    ]
  },
  {
    id: 'proc3',
    title: '劳动合同签订及社保开户流程',
    description: '企业与员工签订劳动合同并办理社保开户的流程',
    businessType: '劳动用工备案',
    entityType: '有限责任公司',
    industry: '科技/软件',
    region: '北京市',
    scenario: '首次办理',
    estimatedTime: '5-10个工作日',
    difficulty: '简单',
    steps: [
      { order: 1, title: '劳动合同准备', description: '根据劳动合同法制定符合法律规定的劳动合同文本', duration: '1-2个工作日', tips: '应包含必备条款' },
      { order: 2, title: '双方签订合同', description: '企业与员工协商一致后签署劳动合同', duration: '1个工作日', tips: '双方各执一份' },
      { order: 3, title: '社保单位开户', description: '到社保经办机构办理单位社保登记', duration: '3-5个工作日', tips: '需先办理税务登记' },
      { order: 4, title: '办理用工备案', description: '在人力资源和社会保障部门进行用工登记备案', duration: '2-3个工作日', tips: '可网上办理' },
      { order: 5, title: '员工社保增员', description: '为新入职员工办理社保增员手续', duration: '1-2个工作日', tips: '每月固定期限前办理' }
    ],
    materials: [
      '劳动合同文本',
      '员工身份证复印件',
      '企业营业执照副本',
      '银行开户许可证'
    ]
  },
  {
    id: 'proc4',
    title: '公司变更登记流程',
    description: '公司名称、地址、法定代表人等变更的登记流程',
    businessType: '变更登记',
    entityType: '有限责任公司',
    industry: '科技/软件',
    region: '北京市',
    scenario: '延期/变更',
    estimatedTime: '5-10个工作日',
    difficulty: '简单',
    steps: [
      { order: 1, title: '召开股东会决议', description: '就变更事项召开股东会并作出决议', duration: '1个工作日', tips: '需三分之二以上表决权通过' },
      { order: 2, title: '修改公司章程', description: '根据变更事项修改公司章程', duration: '1个工作日', tips: '需股东签字确认' },
      { order: 3, title: '网上提交申请', description: '在市场监管局网站提交变更登记申请', duration: '1个工作日', tips: '按要求上传材料' },
      { order: 4, title: '工商审核', description: '市场监管部门审核变更材料', duration: '3-5个工作日', tips: '如有问题需补正' },
      { order: 5, title: '领取新营业执照', description: '审核通过后领取新的营业执照', duration: '1-2个工作日', tips: '需交回旧执照' }
    ],
    materials: [
      '股东会决议',
      '修改后的公司章程',
      '变更登记申请书',
      '原营业执照正副本',
      '法定代表人身份证明'
    ]
  }
]
