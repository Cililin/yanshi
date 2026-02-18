<template>
  <div class="statistics-page">
    <!-- 统计概览 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card nordic-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #fef2f2;">
              <el-icon :size="32" color="#dc2626"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">文章总数</div>
              <div class="stat-value">{{ statistics?.totalCount || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card nordic-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #fffbeb;">
              <el-icon :size="32" color="#d97706"><Files /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">今日新增</div>
              <div class="stat-value">{{ statistics?.todayCount || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card nordic-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #f0fdf4;">
              <el-icon :size="32" color="#16a34a"><FolderOpened /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">新华网</div>
              <div class="stat-value">{{ statistics?.xinhuaCount || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card nordic-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #eff6ff;">
              <el-icon :size="32" color="#2563eb"><Calendar /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">人民网</div>
              <div class="stat-value">{{ statistics?.peopleCount || 0 }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20">
      <!-- 按来源统计 -->
      <el-col :xs="24" :md="12">
        <el-card class="chart-card nordic-card">
          <template #header>
            <div class="card-header">
              <span>📊 按来源统计</span>
            </div>
          </template>
          <div class="chart-content">
            <div v-if="sourceStats.length" class="stat-bars">
              <div
                v-for="item in sourceStats"
                :key="item.source"
                class="stat-bar-item"
              >
                <div class="bar-label">{{ item.source }}</div>
                <div class="bar-wrapper">
                  <div
                    class="bar-fill"
                    :style="{
                      width: `${(item.count / maxSourceCount) * 100}%`,
                      background: getBarColor(item.count, maxSourceCount)
                    }"
                  ></div>
                </div>
                <div class="bar-value">{{ item.count }}</div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>

      <!-- 按分类统计 -->
      <el-col :xs="24" :md="12">
        <el-card class="chart-card nordic-card">
          <template #header>
            <div class="card-header">
              <span>📊 按分类统计</span>
            </div>
          </template>
          <div class="chart-content">
            <div v-if="categoryStats.length" class="stat-bars">
              <div
                v-for="item in categoryStats"
                :key="item.category"
                class="stat-bar-item"
              >
                <div class="bar-label">{{ item.category }}</div>
                <div class="bar-wrapper">
                  <div
                    class="bar-fill"
                    :style="{
                      width: `${(item.count / maxCategoryCount) * 100}%`,
                      background: getBarColor(item.count, maxCategoryCount)
                    }"
                  ></div>
                </div>
                <div class="bar-value">{{ item.count }}</div>
              </div>
            </div>
            <el-empty v-else description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 按日期统计 -->
    <el-card class="date-chart-card nordic-card">
      <template #header>
        <div class="card-header">
          <span>📅 按日期统计</span>
          <div class="date-filter">
            <el-date-picker
              v-model="dateRange"
              type="monthrange"
              range-separator="至"
              start-placeholder="开始月份"
              end-placeholder="结束月份"
              value-format="YYYY-MM"
              @change="fetchDateStats"
            />
          </div>
        </div>
      </template>
      <div class="chart-content">
        <div v-if="dateStats.length" class="date-timeline">
          <div
            v-for="item in dateStats"
            :key="item.date"
            class="timeline-item"
          >
            <div class="timeline-date">{{ item.date }}</div>
            <div class="timeline-bar-wrapper">
              <div
                class="timeline-bar"
                :style="{
                  width: `${(item.count / maxDateCount) * 100}%`
                }"
              ></div>
              <div class="timeline-count">{{ item.count }}</div>
            </div>
          </div>
        </div>
        <el-empty v-else description="暂无数据" />
      </div>
    </el-card>

    <!-- 刷新按钮 -->
    <div class="refresh-section">
      <el-button
        type="primary"
        :icon="Refresh"
        size="large"
        @click="refreshAll"
      >
        刷新数据
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Document, Files, FolderOpened, Calendar, Refresh } from '@element-plus/icons-vue'
import {
  getArticleStatistics,
  countBySource,
  countByCategory,
  countByDate
} from '@/api/article'

const statistics = ref(null)
const sourceStats = ref([])
const categoryStats = ref([])
const dateStats = ref([])
const dateRange = ref([])

const maxSourceCount = computed(() => {
  return Math.max(...sourceStats.value.map(s => s.count), 1)
})

const maxCategoryCount = computed(() => {
  return Math.max(...categoryStats.value.map(s => s.count), 1)
})

const maxDateCount = computed(() => {
  return Math.max(...dateStats.value.map(s => s.count), 1)
})

const getBarColor = (count, max) => {
  const ratio = count / max
  if (ratio >= 0.8) return '#dc2626'
  if (ratio >= 0.6) return '#d97706'
  if (ratio >= 0.4) return '#16a34a'
  return '#2563eb'
}

const fetchStatistics = async () => {
  try {
    const res = await getArticleStatistics()
    statistics.value = res || {}
  } catch (error) {
    console.error('获取统计信息失败:', error)
    statistics.value = {}
  }
}

const fetchSourceStats = async () => {
  try {
    const res = await countBySource()
    sourceStats.value = (res && Array.isArray(res)) ? res : []
  } catch (error) {
    console.error('获取来源统计失败:', error)
    sourceStats.value = []
  }
}

const fetchCategoryStats = async () => {
  try {
    const res = await countByCategory()
    categoryStats.value = (res && Array.isArray(res)) ? res : []
  } catch (error) {
    console.error('获取分类统计失败:', error)
    categoryStats.value = []
  }
}

const fetchDateStats = async () => {
  try {
    const params = {}
    if (dateRange.value && dateRange.value.length === 2) {
      // 将月份格式转换为月初和月末
      params.startDate = dateRange.value[0] + '-01'
      params.endDate = dateRange.value[1] + '-28'
    }
    const res = await countByDate(params)
    dateStats.value = (res && Array.isArray(res)) ? res : []
  } catch (error) {
    console.error('获取日期统计失败:', error)
    dateStats.value = []
  }
}

const refreshAll = async () => {
  await Promise.all([
    fetchStatistics(),
    fetchSourceStats(),
    fetchCategoryStats(),
    fetchDateStats()
  ])
}

onMounted(() => {
  console.log('统计页面已挂载')
  refreshAll()
})
</script>

<style scoped lang="scss">
.statistics-page {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.stats-row {
  .stat-card {
    .stat-item {
      display: flex;
      align-items: center;
      gap: 16px;

      .stat-icon {
        width: 60px;
        height: 60px;
        border-radius: var(--radius-lg);
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .stat-content {
        flex: 1;

        .stat-label {
          font-size: 14px;
          color: var(--color-text-tertiary);
          margin-bottom: 8px;
        }

        .stat-value {
          font-size: 28px;
          font-weight: 700;
          color: var(--color-text-primary);
        }

        .stat-date {
          font-size: 16px;
          font-weight: 600;
          color: var(--color-text-primary);
        }
      }
    }
  }
}

.chart-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .chart-content {
    min-height: 300px;
    padding: 20px 0;
  }
}

.stat-bars {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .stat-bar-item {
    display: flex;
    align-items: center;
    gap: 12px;

    .bar-label {
      width: 80px;
      text-align: right;
      font-size: 14px;
      color: var(--color-text-secondary);
    }

    .bar-wrapper {
      flex: 1;
      height: 32px;
      background: var(--color-bg-2);
      border-radius: 4px;
      overflow: hidden;
      position: relative;

      .bar-fill {
        height: 100%;
        transition: width 0.5s ease;
        border-radius: 4px;
      }
    }

    .bar-value {
      width: 40px;
      text-align: center;
      font-weight: 600;
      color: var(--color-text-primary);
    }
  }
}

.date-chart-card {
  .card-header {
    .date-filter {
      display: flex;
      gap: 12px;
    }
  }
}

.date-timeline {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px 0;

  .timeline-item {
    display: flex;
    align-items: center;
    gap: 12px;

    .timeline-date {
      width: 100px;
      font-size: 14px;
      color: var(--color-text-secondary);
    }

    .timeline-bar-wrapper {
      flex: 1;
      display: flex;
      align-items: center;
      gap: 12px;

      .timeline-bar {
        height: 32px;
        background: linear-gradient(90deg, #2563eb 0%, #16a34a 100%);
        border-radius: 4px;
        transition: width 0.5s ease;
      }

      .timeline-count {
        width: 60px;
        text-align: center;
        font-weight: 600;
        color: var(--color-text-primary);
      }
    }
  }
}

.refresh-section {
  text-align: center;
  padding: 20px;
}
</style>
