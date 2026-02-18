-- ==========================================
-- 研时 - 考研时政智能分析系统 数据库初始化脚本
-- 创建日期: 2026-02-16
-- 更新日期: 2026-02-18
-- ==========================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS yanshi DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE yanshi;

-- 删除已存在的表(开发阶段使用)
DROP TABLE IF EXISTS extraction_tasks;
DROP TABLE IF EXISTS knowledge_relations;
DROP TABLE IF EXISTS article_knowledge_relation;
DROP TABLE IF EXISTS article_knowledge;
DROP TABLE IF EXISTS knowledge_points;
DROP TABLE IF EXISTS articles;
DROP TABLE IF EXISTS crawl_stats;

-- ==========================================
-- 核心表结构
-- ==========================================

-- 文章表
CREATE TABLE articles (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '文章ID',
    title VARCHAR(500) NOT NULL COMMENT '文章标题',
    source VARCHAR(50) NOT NULL COMMENT '来源(新华网/人民网等)',
    url VARCHAR(1000) NOT NULL COMMENT '原文链接',
    url_hash VARCHAR(64) NOT NULL UNIQUE COMMENT 'URL的SHA256哈希值(用于去重)',
    content TEXT COMMENT '文章内容(HTML格式)',
    summary TEXT COMMENT 'AI生成的摘要',
    keywords VARCHAR(500) COMMENT '关键词(逗号分隔)',
    category VARCHAR(100) COMMENT '分类(会议活动/人民网评等)',
    publish_date DATE COMMENT '发布日期',
    publish_time DATETIME COMMENT '发布时间',
    crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '爬取时间',
    importance_score DECIMAL(3,2) DEFAULT 0.50 COMMENT '重要程度评分(0-1)',
    status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending' COMMENT '处理状态',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_publish_date (publish_date),
    INDEX idx_source (source),
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_crawl_time (crawl_time),
    INDEX idx_url_hash (url_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='时政文章表';

-- 知识点表
CREATE TABLE knowledge_points (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '知识点ID',
    name VARCHAR(200) NOT NULL COMMENT '知识点名称',
    type VARCHAR(20) COMMENT '类型：concept/person/event/policy/data',
    category VARCHAR(100) NOT NULL COMMENT '知识点分类',
    description TEXT COMMENT '知识点描述',
    keywords VARCHAR(500) COMMENT '关键词(逗号分隔)',
    importance_score DECIMAL(5,2) COMMENT '重要性评分0-100',
    article_count INT DEFAULT 0 COMMENT '关联文章数',
    first_seen_at TIMESTAMP NULL COMMENT '首次出现时间',
    last_seen_at TIMESTAMP NULL COMMENT '最后出现时间',
    parent_id BIGINT NULL COMMENT '父知识点ID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_category (category),
    INDEX idx_parent (parent_id),
    INDEX idx_type (type),
    INDEX idx_importance (importance_score DESC),
    INDEX idx_article_count (article_count DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='考研政治知识点表';

-- 文章-知识点关联表(多对多) - 保留兼容性
CREATE TABLE article_knowledge (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '关联ID',
    article_id BIGINT NOT NULL COMMENT '文章ID',
    knowledge_point_id BIGINT NOT NULL COMMENT '知识点ID',
    relevance_score DECIMAL(3,2) DEFAULT 0.50 COMMENT '关联程度(0-1)',
    matched_by VARCHAR(50) DEFAULT 'ai' COMMENT '匹配方式(ai/manual)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE,
    UNIQUE KEY uk_article_knowledge (article_id, knowledge_point_id),
    INDEX idx_article (article_id),
    INDEX idx_knowledge (knowledge_point_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章-知识点关联表';

-- 文章-知识点关联表(扩展版) - 用于AI抽取
CREATE TABLE article_knowledge_relation (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    article_id BIGINT NOT NULL COMMENT '文章ID',
    knowledge_point_id BIGINT NOT NULL COMMENT '知识点ID',
    relevance DECIMAL(3,2) DEFAULT 0.50 COMMENT '相关度0-1',
    context TEXT COMMENT '上下文片段',
    position INT DEFAULT 0 COMMENT '在文章中的位置',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_article_knowledge (article_id, knowledge_point_id),
    INDEX idx_article (article_id),
    INDEX idx_knowledge (knowledge_point_id),
    INDEX idx_relevance (relevance DESC),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='文章-知识点关联表(扩展版)';

-- 知识点关联表(知识点之间的关系)
CREATE TABLE knowledge_relations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    source_id BIGINT NOT NULL COMMENT '源知识点ID',
    target_id BIGINT NOT NULL COMMENT '目标知识点ID',
    relation_type VARCHAR(20) NOT NULL COMMENT '关系类型：include/related/cause/time',
    weight DECIMAL(3,2) DEFAULT 0.50 COMMENT '关系权重0-1',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_relation (source_id, target_id, relation_type),
    INDEX idx_source (source_id),
    INDEX idx_target (target_id),
    INDEX idx_relation_type (relation_type),
    FOREIGN KEY (source_id) REFERENCES knowledge_points(id) ON DELETE CASCADE,
    FOREIGN KEY (target_id) REFERENCES knowledge_points(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='知识点关联表';

-- AI抽取任务表
CREATE TABLE extraction_tasks (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '主键ID',
    article_id BIGINT NOT NULL COMMENT '文章ID',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '状态：pending/processing/completed/failed',
    error_message TEXT COMMENT '错误信息',
    extracted_count INT DEFAULT 0 COMMENT '抽取到的知识点数量',
    started_at TIMESTAMP NULL COMMENT '开始时间',
    completed_at TIMESTAMP NULL COMMENT '完成时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_article (article_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI抽取任务表';

-- 爬取统计表
CREATE TABLE crawl_stats (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '统计ID',
    source VARCHAR(50) NOT NULL COMMENT '数据源',
    crawl_date DATE NOT NULL COMMENT '爬取日期',
    total_count INT DEFAULT 0 COMMENT '总爬取数',
    success_count INT DEFAULT 0 COMMENT '成功数',
    failed_count INT DEFAULT 0 COMMENT '失败数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_source_date (source, crawl_date),
    INDEX idx_crawl_date (crawl_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='爬取统计表';

-- ==========================================
-- 视图
-- ==========================================

-- 知识点统计视图
CREATE OR REPLACE VIEW v_knowledge_stats AS
SELECT 
    category,
    type,
    COUNT(*) as total_count,
    AVG(importance_score) as avg_importance,
    SUM(article_count) as total_articles,
    MAX(importance_score) as max_importance
FROM knowledge_points
GROUP BY category, type
ORDER BY category, type;

-- ==========================================
-- 初始数据
-- ==========================================

-- 插入初始知识点数据
INSERT INTO knowledge_points (name, type, category, description, keywords, importance_score, article_count, first_seen_at, last_seen_at) VALUES
-- 马克思主义原理
('马克思主义基本原理概论', 'concept', '马克思主义原理', '马克思主义的科学体系、基本观点和方法论', '马克思主义,哲学,政治经济学', 95.00, 0, NOW(), NOW()),
('物质与意识', 'concept', '马克思主义原理', '辩证唯物主义关于物质和意识关系的基本观点', '物质,意识,辩证法', 85.00, 0, NOW(), NOW()),
('矛盾的普遍性和特殊性', 'concept', '马克思主义原理', '马克思主义哲学关于矛盾的基本原理', '矛盾,普遍性,特殊性', 87.00, 0, NOW(), NOW()),
('实践与认识', 'concept', '马克思主义原理', '马克思主义认识论的核心内容', '实践,认识,真理', 88.00, 0, NOW(), NOW()),
('生产力和生产关系', 'concept', '马克思主义原理', '历史唯物主义关于社会发展的基本规律', '生产力,生产关系,社会发展', 86.00, 0, NOW(), NOW()),

-- 习近平新时代中国特色社会主义思想
('习近平新时代中国特色社会主义思想概论', 'concept', '习近平新时代中国特色社会主义思想', '习近平思想的核心要义和精神实质', '习近平,思想,理论', 98.00, 0, NOW(), NOW()),
('中国梦', 'concept', '习近平新时代中国特色社会主义思想', '实现中华民族伟大复兴的中国梦', '中国梦,复兴,民族', 90.00, 0, NOW(), NOW()),
('五位一体总体布局', 'policy', '习近平新时代中国特色社会主义思想', '经济建设、政治建设、文化建设、社会建设、生态文明建设', '五位一体,总体布局,建设', 92.00, 0, NOW(), NOW()),
('四个全面战略布局', 'policy', '习近平新时代中国特色社会主义思想', '全面建成小康社会、全面深化改革、全面依法治国、全面从严治党', '四个全面,战略布局', 93.00, 0, NOW(), NOW()),
('新发展理念', 'policy', '习近平新时代中国特色社会主义思想', '创新、协调、绿色、开放、共享的发展理念', '新发展理念,创新,绿色', 94.00, 0, NOW(), NOW()),
('高质量发展', 'concept', '习近平新时代中国特色社会主义思想', '推动经济发展从量的积累转向质的飞跃', '高质量发展,经济转型', 96.00, 0, NOW(), NOW()),

-- 道德与法治
('思想道德修养', 'concept', '道德与法治', '社会主义核心价值观、社会公德、职业道德等', '道德,修养,价值观', 84.00, 0, NOW(), NOW()),
('法律基础', 'concept', '道德与法治', '宪法、民法、刑法、行政法等基本法律知识', '法律,宪法,法治', 85.00, 0, NOW(), NOW()),
('法治理念', 'concept', '道德与法治', '依法治国、建设社会主义法治国家的基本理念', '法治,依法治国', 86.00, 0, NOW(), NOW()),

-- 经济
('供给侧结构性改革', 'policy', '经济', '供给侧结构性改革是推动高质量发展的主线', '供给侧,结构性改革', 91.00, 0, NOW(), NOW()),
('双循环新发展格局', 'policy', '经济', '构建以国内大循环为主体、国内国际双循环相互促进的新发展格局', '双循环,新发展格局', 88.00, 0, NOW(), NOW()),
('共同富裕', 'concept', '经济', '实现全体人民共同富裕的目标', '共同富裕,收入分配', 89.00, 0, NOW(), NOW()),

-- 社会
('社会保障体系', 'policy', '社会', '完善覆盖全民的社会保障体系', '社保,医疗保险,养老保险', 87.00, 0, NOW(), NOW()),
('教育现代化', 'event', '社会', '推进教育现代化建设', '教育,改革', 85.00, 0, NOW(), NOW()),
('健康中国', 'concept', '社会', '实施健康中国战略', '健康,医疗', 86.00, 0, NOW(), NOW()),

-- 外交
('一带一路倡议', 'policy', '外交', '推进"一带一路"建设', '一带一路,合作', 97.00, 0, NOW(), NOW()),
('人类命运共同体', 'concept', '外交', '构建人类命运共同体', '人类命运共同体,外交', 95.00, 0, NOW(), NOW()),
('南南合作', 'event', '外交', '加强南南合作', '南南合作,发展中国家', 82.00, 0, NOW(), NOW()),

-- 时政热点
('国内时政', 'concept', '时政热点', '国内重大政治事件和政策解读', '国内,时政,政策', 80.00, 0, NOW(), NOW()),
('国际时政', 'concept', '时政热点', '国际重大政治事件和外交关系', '国际,时政,外交', 80.00, 0, NOW(), NOW()),
('经济形势', 'concept', '时政热点', '国家经济运行状况和政策', '经济,形势,政策', 81.00, 0, NOW(), NOW()),
('社会民生', 'concept', '时政热点', '教育、医疗、就业、住房等民生问题', '社会,民生,就业', 81.00, 0, NOW(), NOW());

-- ==========================================
-- 示例文章数据
-- ==========================================

INSERT INTO articles (title, source, url, url_hash, content, summary, keywords, category, publish_date, publish_time, crawl_time, importance_score, status) VALUES
(
  '深入学习贯彻习近平新时代中国特色社会主义思想',
  '人民网',
  'https://www.people.com.cn/article1',
  MD5('https://www.people.com.cn/article1'),
  '<p>习近平新时代中国特色社会主义思想是马克思主义中国化的最新成果，是全党全国人民为实现中华民族伟大复兴而奋斗的行动指南。这一思想深刻回答了新时代坚持和发展什么样的中国特色社会主义、怎样坚持和发展中国特色社会主义的重大时代课题。</p>
  <h2>一、习近平新时代中国特色社会主义思想的科学内涵</h2>
  <p>习近平新时代中国特色社会主义思想，体系严整、逻辑严密、内涵丰富、博大精深，集中体现在党的十九大报告、十九届历次全会报告和党章中，集中体现在《习近平著作选读》、《习近平谈治国理政》等重要著作中。</p>
  <p>这一思想的核心要义是坚持和发展中国特色社会主义，具体体现在"十个明确"、"十四个坚持"、"十三个方面成就"等重要内容中。</p>
  <h2>二、学习贯彻的重大意义</h2>
  <p>深入学习贯彻习近平新时代中国特色社会主义思想，对于统一思想、统一意志、统一行动，为全面建设社会主义现代化国家、全面推进中华民族伟大复兴提供强大思想武器和行动指南，具有重大的现实意义和深远的历史意义。</p>
  <ul>
  <li>理论意义：为马克思主义中国化时代化作出了原创性贡献</li>
  <li>实践意义：为新时代党和国家事业发展提供了根本遵循</li>
  <li>世界意义：为解决人类面临的共同问题提供了中国智慧和中国方案</li>
  </ul>',
  '习近平新时代中国特色社会主义思想是马克思主义中国化的最新成果，是全党全国人民为实现中华民族伟大复兴而奋斗的行动指南。',
  '习近平新时代中国特色社会主义思想,马克思主义,理论体系',
  '政治',
  CURDATE(),
  NOW(),
  NOW(),
  0.95,
  'completed'
),
(
  '推动经济高质量发展 实现共同富裕',
  '新华网',
  'https://www.xinhua.net/article2',
  MD5('https://www.xinhua.net/article2'),
  '<p>高质量发展是全面建设社会主义现代化国家的首要任务，是新时代我国经济发展的鲜明主题。推动高质量发展，必须坚持以供给侧结构性改革为主线，提高全要素生产率，着力提升产业链供应链韧性和安全水平。</p>
  <h2>一、高质量发展的内涵</h2>
  <p>高质量发展，就是能够很好满足人民日益增长的美好生活需要的发展，是体现新发展理念的发展，是创新成为第一动力、协调成为内生特点、绿色成为普遍形态、开放成为必由之路、共享成为根本目的的发展。</p>
  <blockquote>高质量发展不只是一个经济要求，而是对经济社会发展方方面面的总要求；不只是对经济发达地区的要求，而是所有地区发展都必须贯彻的要求；不是一时一事的要求，而是必须长期坚持的要求。</blockquote>
  <h2>二、扎实推进共同富裕</h2>
  <p>共同富裕是社会主义的本质要求，是中国式现代化的重要特征。推动共同富裕，必须坚持在高质量发展中促进共同富裕，正确处理效率和公平的关系，构建初次分配、再分配、三次分配协调配套的制度体系。</p>
  <p>要通过扩大中等收入群体、完善基本公共服务体系、规范收入分配秩序等措施，逐步实现全体人民共同富裕的目标。</p>',
  '推动经济高质量发展，促进共同富裕，是新时代的重要任务，需要在高质量发展中扎实推进共同富裕。',
  '高质量发展,共同富裕,供给侧改革',
  '经济',
  CURDATE(),
  NOW(),
  NOW(),
  0.90,
  'completed'
),
(
  '共建"一带一路" 构建人类命运共同体',
  '人民网',
  'https://www.people.com.cn/article3',
  MD5('https://www.people.com.cn/article3'),
  '<p>"一带一路"倡议是习近平总书记深刻思考人类前途命运、推动构建人类命运共同体提出的重大倡议。自2013年提出以来，"一带一路"建设从理念转化为行动，从愿景转变为现实，从总体布局的"大写意"到精谨细腻的"工笔画"，取得了实打实、沉甸甸的成就。</p>
  <h2>一、"一带一路"倡议的核心内涵</h2>
  <p>"一带一路"倡议以共商共建共享为原则，以和平合作、开放包容、互学互鉴、互利共赢的丝路精神为指引，以政策沟通、设施联通、贸易畅通、资金融通、民心相通为主要内容，致力于打造全球互联互通伙伴关系。</p>
  <h2>二、构建人类命运共同体的实践路径</h2>
  <p>构建人类命运共同体，是习近平外交思想的核心理念，是推动建设持久和平、共同繁荣的和谐世界的中国方案。"一带一路"建设作为构建人类命运共同体的重要实践平台，正在把沿线国家的前途命运紧密联系在一起。</p>
  <p>通过"一带一路"建设，各国可以携手应对世界经济发展面临的共同问题，推动建设开放型世界经济，促进贸易和投资自由化便利化，推动经济全球化朝着更加开放、包容、普惠、平衡、共赢的方向发展。</p>',
  '共建"一带一路"，推动构建人类命运共同体，是新时代中国特色大国外交的重要实践。',
  '一带一路,人类命运共同体,外交',
  '外交',
  CURDATE(),
  NOW(),
  NOW(),
  0.92,
  'completed'
),
(
  '完善社会保障体系 提升民生福祉',
  '新华网',
  'https://www.xinhua.net/article4',
  MD5('https://www.xinhua.net/article4'),
  '<p>社会保障是保障和改善民生、维护社会公平、增进人民福祉的基本制度保障。党的十八大以来，我国社会保障体系建设进入快车道，基本养老保险覆盖10.5亿人，基本医疗保险覆盖13.6亿人，社会保障网络织密扎牢。</p>
  <h2>一、社会保障体系建设成就</h2>
  <p>我国建成了世界上规模最大的社会保障体系，基本养老保险覆盖范围持续扩大，基本医疗保险参保率稳定在95%以上，失业保险、工伤保险制度不断完善，社会救助制度更加健全，人民群众的获得感、幸福感、安全感更加充实、更有保障、更可持续。</p>
  <h2>二、完善社会保障体系的重点任务</h2>
  <p>完善覆盖全民的社会保障体系，要坚持应保尽保原则，健全统筹城乡、可持续的基本养老保险制度和基本医疗保险制度，稳步提高保障水平。</p>
  <ul>
  <li><strong>养老保险：</strong>完善基本养老保险全国统筹制度，发展多层次、多支柱养老保险体系</li>
  <li><strong>医疗保险：</strong>健全基本医疗保险筹资和待遇调整机制，完善重大疾病医疗保险和救助制度</li>
  <li><strong>社会救助：</strong>健全分层分类的社会救助体系，扩大社会救助范围，提高救助精准度</li>
  </ul>',
  '完善覆盖全民的社会保障体系，不断提升人民群众的获得感、幸福感、安全感。',
  '社会保障,医疗保险,养老保险',
  '社会',
  CURDATE(),
  NOW(),
  NOW(),
  0.88,
  'completed'
),
(
  '供给侧结构性改革 推动经济转型升级',
  '人民网',
  'https://www.people.com.cn/article5',
  MD5('https://www.people.com.cn/article5'),
  '<p>供给侧结构性改革是推动经济高质量发展的重要抓手，是适应我国经济发展新常态的必然选择。自2015年提出以来，供给侧结构性改革取得重要成效，"三去一降一补"任务扎实推进，经济结构不断优化，发展质量持续提升。</p>
  <h2>一、供给侧结构性改革的核心要义</h2>
  <p>供给侧结构性改革，重点是解放和发展社会生产力，用改革的办法推进结构调整，减少无效和低端供给，扩大有效和中高端供给，增强供给结构对需求变化的适应性和灵活性，提高全要素生产率。</p>
  <h2>二、深化供给侧结构性改革的重点</h2>
  <p>深化供给侧结构性改革，要坚持以供给侧结构性改革为主线，着力提升供给体系质量和水平，推动质量变革、效率变革、动力变革。</p>
  <p>重点包括：巩固"三去一降一补"成果，增强微观主体活力，提升产业链水平，畅通国民经济循环。通过深化要素市场化配置改革，加快建设现代化经济体系，推动经济高质量发展。</p>',
  '深化供给侧结构性改革，推动经济转型升级，实现经济高质量发展。',
  '供给侧,结构性改革,经济转型',
  '经济',
  CURDATE(),
  NOW(),
  NOW(),
  0.89,
  'completed'
);

-- ==========================================
-- 文章-知识点关联数据
-- ==========================================

INSERT INTO article_knowledge_relation (article_id, knowledge_point_id, relevance, context, position) VALUES
-- 文章1的知识点关联
(1, 6, 0.95, '习近平新时代中国特色社会主义思想是马克思主义中国化的最新成果', 1),
(1, 1, 0.93, '习近平新时代中国特色社会主义思想是马克思主义中国化的最新成果', 1),

-- 文章2的知识点关联
(2, 12, 0.92, '高质量发展是全面建设社会主义现代化国家的首要任务', 1),
(2, 14, 0.88, '促进共同富裕，是新时代的重要任务', 2),

-- 文章3的知识点关联
(3, 15, 0.94, '"一带一路"倡议是推动构建人类命运共同体的重要平台', 1),
(3, 16, 0.93, '推动构建人类命运共同体，是新时代中国特色大国外交的重要实践', 1),

-- 文章4的知识点关联
(4, 17, 0.90, '完善覆盖全民的社会保障体系', 1),

-- 文章5的知识点关联
(5, 13, 0.91, '供给侧结构性改革是推动经济高质量发展的重要抓手', 1);

-- ==========================================
-- 数据库初始化完成
-- ==========================================
