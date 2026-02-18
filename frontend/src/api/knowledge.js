import request from './request'

// 获取所有知识点
export function getAllKnowledgePoints() {
  return request({
    url: '/knowledge-points',
    method: 'get'
  })
}

// 根据ID查询知识点
export function getKnowledgePointById(id) {
  return request({
    url: `/knowledge-points/${id}`,
    method: 'get'
  })
}

// 根据分类查询知识点
export function getKnowledgePointsByCategory(category) {
  return request({
    url: `/knowledge-points/category/${category}`,
    method: 'get'
  })
}

// 获取顶级知识点
export function getTopLevelKnowledgePoints() {
  return request({
    url: '/knowledge-points/top',
    method: 'get'
  })
}
