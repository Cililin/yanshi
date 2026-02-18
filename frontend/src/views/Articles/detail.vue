<template>
  <div class="article-detail-page">
    <div class="back-section">
      <el-button
        :icon="ArrowLeft"
        @click="$router.back()"
        class="back-btn"
        text
      >
        返回列表
      </el-button>
    </div>

    <div v-if="article" class="detail-container">
      <!-- 文章头部 -->
      <div class="article-header">
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <span class="meta-item">
            <el-icon><Document /></el-icon>
            {{ article.source || '未知来源' }}
          </span>
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            {{ article.publishDate || article.publish_date || '未知日期' }}
          </span>
          <span v-if="article.publishTime || article.publish_time" class="meta-item">
            <el-icon><Clock /></el-icon>
            {{ article.publishTime || article.publish_time }}
          </span>
        </div>
      </div>

      <!-- 摘要 -->
      <div v-if="article.summary" class="article-summary-section">
        <h2 class="section-title">摘要</h2>
        <p class="summary-text">{{ article.summary }}</p>
      </div>

      <!-- 文章内容 -->
      <div class="article-content-wrapper">
        <div v-if="article.content" class="article-content" v-html="article.content"></div>
        <div v-else class="no-content">
          <el-empty description="暂无文章内容" />
        </div>
      </div>

      <!-- 关键词 -->
      <div v-if="article.keywords" class="keywords-section">
        <h2 class="section-title">关键词</h2>
        <div class="keywords-list">
          <el-tag
            v-for="keyword in getKeywords(article.keywords)"
            :key="keyword"
            class="keyword-item"
          >
            {{ keyword }}
          </el-tag>
        </div>
      </div>

      <!-- 原文链接 -->
      <div v-if="article.url" class="link-section">
        <el-link :href="article.url" target="_blank" type="primary" :icon="Link" :underline="false">
          查看原文
        </el-link>
      </div>
    </div>

    <el-skeleton v-else :rows="15" animated />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Link, Document, Clock, Calendar } from '@element-plus/icons-vue'
import { getArticleDetail } from '@/api/article'

const route = useRoute()
const article = ref(null)

const fetchArticleDetail = async () => {
  try {
    const id = route.params.id
    console.log('正在获取文章详情，ID:', id)
    const res = await getArticleDetail(id)
    console.log('文章详情数据:', res)
    console.log('文章详情类型:', typeof res)
    console.log('文章详情内容:', JSON.stringify(res, null, 2))
    article.value = res
  } catch (error) {
    console.error('获取文章详情失败:', error)
    ElMessage.error('获取文章详情失败: ' + error.message)
  }
}

// 获取关键词
const getKeywords = (keywords) => {
  return keywords ? keywords.split(',').filter(k => k.trim()) : []
}

onMounted(() => {
  fetchArticleDetail()
})
</script>

<style scoped lang="scss">
.article-detail-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.back-section {
  padding-bottom: 10px;
}

.back-btn {
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.detail-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.article-header {
  padding-bottom: 20px;
  border-bottom: 1px solid var(--color-border);
}

.article-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 20px 0;
  line-height: 1.4;
}

.article-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  align-items: center;
  color: var(--color-text-secondary);
  font-size: 15px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.article-content-wrapper {
  background: var(--color-bg-1);
  padding: 40px;
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.article-summary-section {
  background: var(--color-bg-2);
  padding: 20px 24px;
  border-radius: var(--radius-md);
  border-left: 4px solid var(--color-wood-1);

  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 10px 0;
  }

  .summary-text {
    margin: 0;
    line-height: 1.6;
    color: var(--color-text-secondary);
  }
}

.article-content {
  font-size: 18px;
  line-height: 1.8;
  color: var(--color-text-primary);

  :deep(p) {
    margin-bottom: 20px;
    text-align: justify;
  }

  :deep(h2),
  :deep(h3) {
    margin-top: 30px;
    margin-bottom: 16px;
    color: var(--color-text-primary);
    font-weight: 600;
  }

  :deep(h2) {
    font-size: 24px;
  }

  :deep(h3) {
    font-size: 20px;
  }

  :deep(ul),
  :deep(ol) {
    margin-bottom: 20px;
    padding-left: 24px;
  }

  :deep(li) {
    margin-bottom: 8px;
  }

  :deep(blockquote) {
    border-left: 4px solid var(--color-wood-1);
    padding: 16px 20px;
    margin: 20px 0;
    background: var(--color-bg-2);
    font-style: italic;
  }
}

.no-content {
  padding: 40px 0;
}

.keywords-section {
  background: var(--color-bg-1);
  padding: 20px 24px;
  border-radius: var(--radius-md);

  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--color-text-primary);
    margin: 0 0 15px 0;
  }

  .keywords-list {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }

  .keyword-item {
    background: var(--color-bg-2);
  }
}

.link-section {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);

  :deep(.el-link) {
    font-size: 16px;
    padding: 12px 30px;
    border-radius: var(--radius-md);
    transition: var(--transition-base);

    &:hover {
      background: var(--color-wood-1);
      color: white;
    }
  }
}
</style>
