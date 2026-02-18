<template>
  <div class="knowledge-page">
    <el-card class="filter-card">
      <el-form inline>
        <el-form-item label="搜索">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索知识点名称或描述"
            clearable
            @keyup.enter="fetchKnowledge"
          />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="filters.type" clearable placeholder="全部" @change="fetchKnowledge">
            <el-option label="概念" value="concept" />
            <el-option label="人物" value="person" />
            <el-option label="事件" value="event" />
            <el-option label="政策" value="policy" />
            <el-option label="数据" value="data" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="filters.category" clearable placeholder="全部" @change="fetchKnowledge">
            <el-option label="政治" value="政治" />
            <el-option label="经济" value="经济" />
            <el-option label="社会" value="社会" />
            <el-option label="外交" value="外交" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchKnowledge">查询</el-button>
          <el-button @click="resetFilters">重置</el-button>
          <el-button type="success" @click="goToGraph">
            <el-icon><Share /></el-icon>
            知识图谱
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading">
      <div v-if="knowledgePoints.length > 0" class="knowledge-list">
        <div
          v-for="point in knowledgePoints"
          :key="point.id"
          class="knowledge-item"
          @click="viewDetail(point.id)"
        >
          <div class="point-header">
            <el-tag size="small">{{ getTypeLabel(point.type) }}</el-tag>
            <el-tag type="success" size="small">{{ point.category }}</el-tag>
            <span class="point-importance">
              重要性: {{ point.importanceScore }}
            </span>
          </div>
          <h3 class="point-name">{{ point.name }}</h3>
          <p v-if="point.description" class="point-desc">{{ point.description }}</p>
          <div class="point-meta">
            <span>{{ point.articleCount }} 篇文章</span>
            <el-button size="small" type="text" @click.stop="viewArticles(point.id)">
              查看相关文章
            </el-button>
          </div>
        </div>
      </div>
      <el-empty v-else description="暂无知识点" />
    </el-card>

    <el-pagination
      v-model:current-page="pagination.current"
      v-model:page-size="pagination.size"
      :total="pagination.total"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @change="fetchKnowledge"
      @size-change="fetchKnowledge"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Share } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()

const searchKeyword = ref('')
const filters = ref({
  type: '',
  category: ''
})
const loading = ref(false)
const knowledgePoints = ref([])
const pagination = ref({
  current: 1,
  size: 20,
  total: 0
})

const typeMap = {
  concept: '概念',
  person: '人物',
  event: '事件',
  policy: '政策',
  data: '数据'
}

const getTypeLabel = (type) => typeMap[type] || type

const fetchKnowledge = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.current,
      pageSize: pagination.value.size,
      ...filters.value
    }

    if (searchKeyword.value) {
      const res = await axios.get('/api/knowledge-points/search', {
        params: { ...params, keyword: searchKeyword.value }
      })
      knowledgePoints.value = res.data.data.records
      pagination.value.total = res.data.data.total
    } else {
      const res = await axios.get('/api/knowledge-points', { params })
      knowledgePoints.value = res.data.data.records
      pagination.value.total = res.data.data.total
    }
  } catch (error) {
    ElMessage.error('获取知识点失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  searchKeyword.value = ''
  filters.value = { type: '', category: '' }
  pagination.value.current = 1
  fetchKnowledge()
}

const goToGraph = () => {
  router.push('/knowledge/graph')
}

const viewDetail = (id) => {
  // TODO: 跳转到详情页
  console.log('View detail:', id)
}

const viewArticles = async (pointId) => {
  try {
    const res = await axios.get(`/api/knowledge-points/${pointId}/articles`)
    // TODO: 显示文章列表弹窗或跳转
    console.log('Articles:', res.data.data)
  } catch (error) {
    ElMessage.error('获取文章失败: ' + error.message)
  }
}

onMounted(() => {
  fetchKnowledge()
})
</script>

<style scoped>
.knowledge-page {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.knowledge-item {
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.knowledge-item:hover {
  border-color: #409eff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.point-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.point-importance {
  margin-left: auto;
  color: #f56c6c;
  font-weight: bold;
}

.point-name {
  margin: 10px 0;
  color: #303133;
  font-size: 18px;
}

.point-desc {
  color: #606266;
  margin: 10px 0;
  line-height: 1.6;
}

.point-meta {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: 10px;
  color: #909399;
}

.el-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
