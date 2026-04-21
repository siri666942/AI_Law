import type { LawCategory } from '../types/knowledge'

export const lawCategories: LawCategory[] = [
  {
    id: 'market',
    name: '市场主体与公司治理',
    description: '公司设立、治理、变更、注销等相关法律法规',
    laws: [
      { id: 'law1', number: 1, name: '公司法', fullName: '《中华人民共和国公司法》', category: 'market', publishDate: '2024-01-01', effectiveDate: '2024-07-01', content: '规范公司的组织和行为，保护公司、股东和债权人的合法权益，维护社会经济秩序。' },
      { id: 'law2', number: 2, name: '合伙企业法', fullName: '《中华人民共和国合伙企业法》', category: 'market', content: '规范合伙企业的行为，保护合伙企业及其合伙人、债权人的合法权益。' },
      { id: 'law3', number: 3, name: '个人独资企业法', fullName: '《中华人民共和国个人独资企业法》', category: 'market', content: '规范个人独资企业的行为，保护个人独资企业投资人和债权人的合法权益。' },
      { id: 'law4', number: 4, name: '市场主体登记管理条例', fullName: '《中华人民共和国市场主体登记管理条例》', category: 'market', content: '规范市场主体登记管理行为，推进法治化市场建设。' },
      { id: 'law5', number: 5, name: '公司登记管理条例', fullName: '《中华人民共和国公司登记管理条例》', category: 'market', content: '确认公司的企业法人资格，规范公司登记行为。' },
      { id: 'law6', number: 6, name: '企业名称登记管理规定', fullName: '《企业名称登记管理规定》', category: 'market', content: '规范企业名称登记管理，保护企业名称所有人的合法权益。' },
      { id: 'law7', number: 7, name: '企业法人登记管理条例', fullName: '《中华人民共和国企业法人登记管理条例》', category: 'market', content: '建立企业法人登记管理制度，确认企业法人资格。' }
    ]
  },
  {
    id: 'contract',
    name: '合同与交易',
    description: '合同订立、履行、物权、电子交易等相关法律法规',
    laws: [
      { id: 'law8', number: 8, name: '民法典·合同编', fullName: '《中华人民共和国民法典》（第三编 合同）', category: 'contract', content: '规范因合同产生的民事关系。' },
      { id: 'law9', number: 9, name: '民法典·物权编', fullName: '《中华人民共和国民法典》（第二编 物权）', category: 'contract', content: '规范因物的归属和利用产生的民事关系。' },
      { id: 'law10', number: 10, name: '电子签名法', fullName: '《中华人民共和国电子签名法》', category: 'contract', content: '规范电子签名行为，确立电子签名的法律效力。' },
      { id: 'law11', number: 11, name: '消费者权益保护法', fullName: '《中华人民共和国消费者权益保护法》（部分条款）', category: 'contract', content: '保护消费者的合法权益，维护社会经济秩序。' },
      { id: 'law12', number: 12, name: '网络交易管理办法', fullName: '《网络交易管理办法》', category: 'contract', content: '规范网络商品交易及有关服务，保护消费者和经营者的合法权益。' }
    ]
  },
  {
    id: 'labor',
    name: '劳动用工',
    description: '劳动合同、社会保险、劳动争议等相关法律法规',
    laws: [
      { id: 'law13', number: 13, name: '劳动法', fullName: '《中华人民共和国劳动法》', category: 'labor', content: '保护劳动者的合法权益，调整劳动关系。' },
      { id: 'law14', number: 14, name: '劳动合同法', fullName: '《中华人民共和国劳动合同法》', category: 'labor', content: '完善劳动合同制度，明确劳动合同双方当事人的权利和义务。' },
      { id: 'law15', number: 15, name: '劳动合同法实施条例', fullName: '《中华人民共和国劳动合同法实施条例》', category: 'labor', content: '贯彻实施劳动合同法。' },
      { id: 'law16', number: 16, name: '社会保险法', fullName: '《中华人民共和国社会保险法》', category: 'labor', content: '规范社会保险关系，维护公民参加社会保险和享受社会保险待遇的合法权益。' },
      { id: 'law17', number: 17, name: '工伤保险条例', fullName: '《工伤保险条例》', category: 'labor', content: '保障因工作遭受事故伤害或者患职业病的职工获得医疗救治和经济补偿。' },
      { id: 'law18', number: 18, name: '失业保险条例', fullName: '《失业保险条例》', category: 'labor', content: '保障失业人员失业期间的基本生活，促进其再就业。' },
      { id: 'law19', number: 19, name: '女职工劳动保护特别规定', fullName: '《女职工劳动保护特别规定》', category: 'labor', content: '减少和解决女职工在劳动中因生理特点造成的特殊困难。' },
      { id: 'law20', number: 20, name: '职工带薪年休假条例', fullName: '《职工带薪年休假条例》', category: 'labor', content: '维护职工休息休假权利，调动职工工作积极性。' },
      { id: 'law21', number: 21, name: '劳动争议调解仲裁法', fullName: '《中华人民共和国劳动争议调解仲裁法》', category: 'labor', content: '公正及时解决劳动争议，保护当事人合法权益。' }
    ]
  },
  {
    id: 'ip',
    name: '知识产权',
    description: '商标、专利、著作权、商业秘密等相关法律法规',
    laws: [
      { id: 'law22', number: 22, name: '商标法', fullName: '《中华人民共和国商标法》', category: 'ip', content: '加强商标管理，保护商标专用权。' },
      { id: 'law23', number: 23, name: '商标法实施条例', fullName: '《中华人民共和国商标法实施条例》', category: 'ip', content: '配合商标法的实施。' },
      { id: 'law24', number: 24, name: '专利法', fullName: '《中华人民共和国专利法》', category: 'ip', content: '保护发明创造专利权，鼓励发明创造。' },
      { id: 'law25', number: 25, name: '专利法实施细则', fullName: '《中华人民共和国专利法实施细则》', category: 'ip', content: '配合专利法的实施。' },
      { id: 'law26', number: 26, name: '著作权法', fullName: '《中华人民共和国著作权法》', category: 'ip', content: '保护文学、艺术和科学作品作者的著作权。' },
      { id: 'law27', number: 27, name: '著作权法实施条例', fullName: '《中华人民共和国著作权法实施条例》', category: 'ip', content: '配合著作权法的实施。' },
      { id: 'law28', number: 28, name: '计算机软件保护条例', fullName: '《计算机软件保护条例》', category: 'ip', content: '保护计算机软件著作权人的权益。' },
      { id: 'law29', number: 29, name: '集成电路布图设计保护条例', fullName: '《集成电路布图设计保护条例》', category: 'ip', content: '保护集成电路布图设计专有权。' },
      { id: 'law30', number: 30, name: '反不正当竞争法·商业秘密', fullName: '《中华人民共和国反不正当竞争法》（第六条 商业秘密）', category: 'ip', content: '保护商业秘密，促进公平竞争。' }
    ]
  },
  {
    id: 'finance',
    name: '财税与审计',
    description: '企业所得税、增值税、会计审计等相关法律法规',
    laws: [
      { id: 'law31', number: 31, name: '企业所得税法', fullName: '《中华人民共和国企业所得税法》', category: 'finance', content: '规范企业所得税的征收和缴纳。' },
      { id: 'law32', number: 32, name: '企业所得税法实施条例', fullName: '《中华人民共和国企业所得税法实施条例》', category: 'finance', content: '配合企业所得税法的实施。' },
      { id: 'law33', number: 33, name: '个人所得税法', fullName: '《中华人民共和国个人所得税法》', category: 'finance', content: '规范个人所得税的征收和缴纳。' },
      { id: 'law34', number: 34, name: '个人所得税法实施条例', fullName: '《中华人民共和国个人所得税法实施条例》', category: 'finance', content: '配合个人所得税法的实施。' },
      { id: 'law35', number: 35, name: '增值税暂行条例', fullName: '《中华人民共和国增值税暂行条例》', category: 'finance', content: '规范增值税的征收和缴纳。' },
      { id: 'law36', number: 36, name: '税收征收管理法', fullName: '《中华人民共和国税收征收管理法》', category: 'finance', content: '规范税收征收和缴纳行为。' },
      { id: 'law37', number: 37, name: '发票管理办法', fullName: '《中华人民共和国发票管理办法》', category: 'finance', content: '加强发票管理和财务监督。' },
      { id: 'law38', number: 38, name: '会计法', fullName: '《中华人民共和国会计法》', category: 'finance', content: '规范会计行为，保证会计资料真实、完整。' },
      { id: 'law39', number: 39, name: '企业财务通则', fullName: '《企业财务通则》', category: 'finance', content: '加强企业财务管理，规范企业财务行为。' }
    ]
  },
  {
    id: 'securities',
    name: '融资与证券',
    description: '证券法、创业投资、私募基金等相关法律法规',
    laws: [
      { id: 'law40', number: 40, name: '证券法', fullName: '《中华人民共和国证券法》', category: 'securities', content: '规范证券发行和交易行为，保护投资者的合法权益。' },
      { id: 'law41', number: 41, name: '创业投资企业管理暂行办法', fullName: '《创业投资企业管理暂行办法》', category: 'securities', content: '促进创业投资企业发展。' },
      { id: 'law42', number: 42, name: '私募投资基金监督管理暂行办法', fullName: '《私募投资基金监督管理暂行办法》', category: 'securities', content: '规范私募投资基金活动。' },
      { id: 'law43', number: 43, name: '公司债券发行与交易管理办法', fullName: '《公司债券发行与交易管理办法》', category: 'securities', content: '规范公司债券的发行、交易或转让行为。' },
      { id: 'law44', number: 44, name: '证券投资基金法', fullName: '《中华人民共和国证券投资基金法》', category: 'securities', content: '规范证券投资基金活动，保护投资人及相关当事人的合法权益。' }
    ]
  },
  {
    id: 'industry',
    name: '行业特定与特殊许可',
    description: '网络安全、数据安全、个人信息保护、食品安全等相关法律法规',
    laws: [
      { id: 'law45', number: 45, name: '网络安全法', fullName: '《中华人民共和国网络安全法》', category: 'industry', content: '保障网络安全，维护网络空间主权和国家安全。' },
      { id: 'law46', number: 46, name: '数据安全法', fullName: '《中华人民共和国数据安全法》', category: 'industry', content: '规范数据处理活动，保障数据安全。' },
      { id: 'law47', number: 47, name: '个人信息保护法', fullName: '《中华人民共和国个人信息保护法》', category: 'industry', content: '保护个人信息权益，规范个人信息处理活动。' },
      { id: 'law48', number: 48, name: '互联网信息服务管理办法', fullName: '《互联网信息服务管理办法》', category: 'industry', content: '规范互联网信息服务活动。' },
      { id: 'law49', number: 49, name: '网络出版服务管理规定', fullName: '《网络出版服务管理规定》', category: 'industry', content: '规范网络出版服务秩序。' },
      { id: 'law50', number: 50, name: '食品安全法', fullName: '《中华人民共和国食品安全法》（如涉及相关行业）', category: 'industry', content: '保证食品安全，保障公众身体健康和生命安全。' },
      { id: 'law51', number: 51, name: '医疗器械监督管理条例', fullName: '《医疗器械监督管理条例》（如涉及相关行业）', category: 'industry', content: '保证医疗器械安全、有效，保障人体健康和生命安全。' },
      { id: 'law52', number: 52, name: '药品管理法', fullName: '《中华人民共和国药品管理法》（如涉及相关行业）', category: 'industry', content: '加强药品管理，保证药品质量，保障公众用药安全。' }
    ]
  },
  {
    id: 'competition',
    name: '公平竞争与广告',
    description: '反垄断、反不正当竞争、广告等相关法律法规',
    laws: [
      { id: 'law53', number: 53, name: '反垄断法', fullName: '《中华人民共和国反垄断法》', category: 'competition', content: '预防和制止垄断行为，保护市场公平竞争。' },
      { id: 'law54', number: 54, name: '反不正当竞争法', fullName: '《中华人民共和国反不正当竞争法》', category: 'competition', content: '促进社会主义市场经济健康发展，鼓励和保护公平竞争。' },
      { id: 'law55', number: 55, name: '广告法', fullName: '《中华人民共和国广告法》', category: 'competition', content: '规范广告活动，保护消费者的合法权益。' },
      { id: 'law56', number: 56, name: '互联网广告管理办法', fullName: '《互联网广告管理办法》', category: 'competition', content: '规范互联网广告活动，促进互联网广告业健康发展。' }
    ]
  },
  {
    id: 'liquidation',
    name: '解散与清算',
    description: '公司解散清算、企业破产等相关法律法规',
    laws: [
      { id: 'law57', number: 57, name: '公司法·解散清算', fullName: '《中华人民共和国公司法》（第十章 公司解散和清算）', category: 'liquidation', content: '规范公司解散和清算程序。' },
      { id: 'law58', number: 58, name: '企业破产法', fullName: '《中华人民共和国企业破产法》', category: 'liquidation', content: '规范企业破产程序，公平清理债权债务。' }
    ]
  }
]
