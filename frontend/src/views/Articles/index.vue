<template>
  <div class="articles-page">
    <!-- 搜索筛选区 -->
    <el-card class="filter-card nordic-card">
      <el-form :model="queryForm" inline>
        <el-form-item label="标题">
          <el-input
            v-model="queryForm.title"
            placeholder="输入标题关键词"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item label="来源">
          <el-select
            v-model="queryForm.source"
            placeholder="选择来源"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="source in sourceList"
              :key="source"
              :label="source"
              :value="source"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="queryForm.category"
            placeholder="选择分类"
            clearable
            style="width: 150px"
          >
            <el-option
              v-for="category in categoryList"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :icon="Search">
            搜索
          </el-button>
          <el-button @click="handleReset" :icon="Refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 最新文章 -->
    <el-card v-if="!queryForm.title && !queryForm.source && !queryForm.category && !dateRange"
      class="recent-card nordic-card">
      <template #header>
        <div class="card-header">
          <span>📰 最新文章</span>
          <el-link type="primary" @click="$router.push('/articles')">
            查看更多 →
          </el-link>
        </div>
      </template>
      <div class="recent-articles">
        <div
          v-for="article in recentArticles"
          :key="article.id"
          class="recent-item"
          @click="viewArticle(article.id)"
        >
          <div class="recent-tag">{{ article.source }}</div>
          <div class="recent-title">{{ article.title }}</div>
          <div class="recent-meta">
            <span>{{ article.publishDate }}</span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 文章列表 -->
    <el-card class="list-card nordic-card">
      <el-empty v-if="!articles.length" description="暂无数据" />
      <div v-else class="article-list">
        <div
          v-for="article in articles"
          :key="article.id"
          class="article-item nordic-card"
          @click="viewArticle(article.id)"
        >
          <div class="article-header">
            <el-tag size="small" type="info">{{ article.source }}</el-tag>
            <el-tag size="small">{{ article.category }}</el-tag>
            <span class="article-date">{{ article.publishDate }}</span>
          </div>
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-summary">{{ article.summary }}</p>
          <div class="article-footer">
            <div class="article-keywords">
              <el-tag
                v-for="keyword in getKeywords(article.keywords)"
                :key="keyword"
                size="small"
                class="keyword-tag"
              >
                {{ keyword }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="articles.length" class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Refresh } from '@element-plus/icons-vue'
import { getArticleList, getRecentArticles, countBySource, countByCategory } from '@/api/article'

const router = useRouter()

// 查询表单
const queryForm = reactive({
  title: '',
  source: '',
  category: ''
})

const dateRange = ref([])

// 来源和分类列表
const sourceList = ref([])
const categoryList = ref([])

// 文章数据
const articles = ref([])
const recentArticles = ref([])

// 分页
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

// 获取来源列表
const fetchSourceList = async () => {
  try {
    const res = await countBySource()
    console.log('来源列表原始数据:', res)
    if (res && Array.isArray(res)) {
      sourceList.value = res.map(item => item.source).filter(Boolean)
      console.log('来源列表处理后:', sourceList.value)
    } else {
      sourceList.value = []
    }
  } catch (error) {
    console.error('获取来源列表失败:', error)
    sourceList.value = []
  }
}

// 获取分类列表
const fetchCategoryList = async () => {
  try {
    const res = await countByCategory()
    console.log('分类列表原始数据:', res)
    if (res && Array.isArray(res)) {
      categoryList.value = res.map(item => item.category).filter(Boolean)
      console.log('分类列表处理后:', categoryList.value)
    } else {
      categoryList.value = []
    }
  } catch (error) {
    console.error('获取分类列表失败:', error)
    categoryList.value = []
  }
}

// 获取文章列表
const fetchArticles = async () => {
  try {
    // 清理空字符串的查询参数
    const params = {
      page: pagination.current,
      pageSize: pagination.size
    }
    // 只添加非空的筛选条件
    if (queryForm.title && queryForm.title.trim()) {
      params.title = queryForm.title.trim()
    }
    if (queryForm.source) {
      params.source = queryForm.source
    }
    if (queryForm.category) {
      params.category = queryForm.category
    }
    if (dateRange.value && dateRange.value.length === 2) {
      params.startDate = dateRange.value[0]
      params.endDate = dateRange.value[1]
    }

    console.log('请求参数:', params)
    const res = await getArticleList(params)
    console.log('返回数据:', res)

    if (res) {
      articles.value = res.records || []
      pagination.total = res.total || 0
      console.log('文章列表:', articles.value.length, '总数:', pagination.total)
    } else {
      articles.value = []
      pagination.total = 0
    }
  } catch (error) {
    console.error('获取文章列表失败:', error)
    articles.value = []
    pagination.total = 0
  }
}

// 获取最新文章
const fetchRecentArticles = async () => {
  try {
    const res = await getRecentArticles(5)
    recentArticles.value = (res && Array.isArray(res)) ? res : []
  } catch (error) {
    console.error('获取最新文章失败:', error)
    recentArticles.value = []
  }
}

// 查看文章详情
const viewArticle = (id) => {
  router.push(`/article/${id}`)
}

// 搜索
const handleSearch = () => {
  console.log('点击搜索，当前查询条件:', queryForm)
  pagination.current = 1
  fetchArticles()
}

// 重置
const handleReset = () => {
  console.log('点击重置')
  queryForm.title = ''
  queryForm.source = ''
  queryForm.category = ''
  dateRange.value = []
  pagination.current = 1
  fetchArticles()
}

// 分页变化
const handleSizeChange = (size) => {
  console.log('修改每页数量:', size)
  pagination.size = size
  fetchArticles()
}

const handleCurrentChange = (page) => {
  console.log('跳转到页:', page)
  pagination.current = page
  fetchArticles()
}

// 获取关键词
const getKeywords = (keywords) => {
  return keywords ? keywords.split(',') : []
}

onMounted(() => {
  fetchSourceList()
  fetchCategoryList()
  fetchArticles()
  fetchRecentArticles()
})
</script>

<style scoped lang="scss">
.articles-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.filter-card {
  :deep(.el-form-item) {
    margin-bottom: 0;
  }
}

.recent-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .recent-articles {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
  }

  .recent-item {
    background: var(--color-bg-2);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    padding: 16px;
    cursor: pointer;
    transition: var(--transition-base);

    &:hover {
      border-color: var(--color-wood-1);
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .recent-tag {
      font-size: 12px;
      color: var(--color-wood-1);
      margin-bottom: 8px;
    }

    .recent-title {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 8px;
      line-height: 1.5;
    }

    .recent-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 12px;
      color: var(--color-text-tertiary);
    }
  }
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.article-item {
  cursor: pointer;

  .article-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .article-date {
    margin-left: auto;
    font-size: 12px;
    color: var(--color-text-tertiary);
  }

  .article-title {
    font-size: 18px;
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: 12px;
    line-height: 1.5;
  }

  .article-summary {
    color: var(--color-text-secondary);
    margin-bottom: 16px;
    line-height: 1.6;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

.article-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.article-keywords {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.keyword-tag {
  background: var(--color-bg-2);
}
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>
