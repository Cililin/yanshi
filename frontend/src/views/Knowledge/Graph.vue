<template>
  <div class="knowledge-graph">
    <el-card class="controls-card">
      <el-form inline>
        <el-form-item label="分类">
          <el-select v-model="filters.category" clearable placeholder="全部" @change="loadGraph">
            <el-option label="政治" value="政治" />
            <el-option label="经济" value="经济" />
            <el-option label="社会" value="社会" />
            <el-option label="外交" value="外交" />
          </el-select>
        </el-form-item>
        <el-form-item label="节点数量">
          <el-slider
            v-model="filters.limit"
            :min="50"
            :max="500"
            :step="50"
            :marks="{ 50: '50', 200: '200', 500: '500' }"
            style="width: 200px"
            @change="loadGraph"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadGraph">刷新</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-loading="loading">
      <div ref="graphRef" class="graph-container"></div>
      <el-empty v-if="!loading && nodes.length === 0" description="暂无知识点图谱数据" />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import axios from 'axios'

const graphRef = ref(null)
const loading = ref(false)
const nodes = ref([])
const edges = ref([])
const filters = ref({
  category: '',
  limit: 200
})
let chart = null

const categoryColors = {
  政治: '#409eff',
  经济: '#67c23a',
  社会: '#e6a23c',
  外交: '#f56c6c'
}

const loadGraph = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/knowledge-points', {
      params: {
        page: 1,
        pageSize: filters.value.limit,
        category: filters.value.category || undefined
      }
    })

    const knowledgePoints = res.data.data.records || []
    buildGraphData(knowledgePoints)
    renderGraph()
  } catch (error) {
    ElMessage.error('加载图谱数据失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const buildGraphData = (points) => {
  // 节点数据
  nodes.value = points.map(point => ({
    id: point.id,
    name: point.name,
    category: point.category,
    value: calculateNodeSize(point.importanceScore, point.articleCount),
    itemStyle: {
      color: categoryColors[point.category] || '#909399'
    }
  }))

  // 边数据（基于相同分类的知识点关联）
  edges.value = []
  const byCategory = {}
  points.forEach(point => {
    if (!byCategory[point.category]) {
      byCategory[point.category] = []
    }
    byCategory[point.category].push(point.id)
  })

  // 为同一分类的知识点创建关联
  Object.values(byCategory).forEach(ids => {
    for (let i = 0; i < ids.length - 1; i++) {
      for (let j = i + 1; j < ids.length; j++) {
        edges.value.push({
          source: ids[i],
          target: ids[j],
          lineStyle: {
            width: 0.5,
            color: '#e0e0e0',
            curveness: 0.3
          }
        })
      }
    }
  })
}

const calculateNodeSize = (importanceScore, articleCount) => {
  const score = importanceScore || 50
  const articles = articleCount || 1
  return Math.max(10, Math.min(50, (score / 100) * 30 + Math.min(articles, 20)))
}

const renderGraph = () => {
  if (!graphRef.value || nodes.value.length === 0) return

  if (!chart) {
    chart = echarts.init(graphRef.value)
  }

  const option = {
    tooltip: {
      formatter: (params) => {
        if (params.dataType === 'node') {
          const data = params.data
          return `
            <div style="padding: 10px;">
              <strong>${data.name}</strong><br/>
              <span style="color: ${data.itemStyle.color}">●</span> ${data.category}<br/>
              重要程度: ${Math.round(data.value * 3.33)}/100
            </div>
          `
        }
        return ''
      }
    },
    legend: {
      data: Object.keys(categoryColors),
      bottom: 10,
      itemWidth: 12,
      itemHeight: 12,
      borderRadius: 4
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        data: nodes.value,
        links: edges.value,
        categories: Object.keys(categoryColors).map(name => ({ name })),
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          fontSize: 12
        },
        force: {
          repulsion: 200,
          edgeLength: 100,
          gravity: 0.1
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            width: 3
          }
        }
      }
    ]
  }

  chart.setOption(option, true)
}

const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

onMounted(() => {
  loadGraph()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.knowledge-graph {
  padding: 20px;
}

.controls-card {
  margin-bottom: 20px;
}

.graph-container {
  width: 100%;
  height: 600px;
}
</style>
