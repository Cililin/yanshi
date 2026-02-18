import request from './request'

// 获取文章列表
export function getArticleList(params) {
  return request({
    url: '/articles',
    method: 'get',
    params
  })
}

// 获取文章详情
export function getArticleDetail(id) {
  return request({
    url: `/articles/${id}`,
    method: 'get'
  })
}

// 获取最新文章
export function getRecentArticles(limit = 10) {
  return request({
    url: '/articles/recent',
    method: 'get',
    params: { limit }
  })
}

// 获取文章统计信息
export function getArticleStatistics() {
  return request({
    url: '/articles/statistics',
    method: 'get'
  })
}

// 按来源统计
export function countBySource() {
  return request({
    url: '/articles/statistics/source',
    method: 'get'
  })
}

// 按分类统计
export function countByCategory() {
  return request({
    url: '/articles/statistics/category',
    method: 'get'
  })
}

// 按日期统计
export function countByDate(params) {
  return request({
    url: '/articles/statistics/date',
    method: 'get',
    params
  })
}
