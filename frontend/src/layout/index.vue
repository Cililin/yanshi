<template>
  <div class="layout-container">
    <!-- 顶部导航栏 -->
    <el-header class="layout-header glass-effect">
      <div class="header-content">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">📚</span>
          <span class="logo-text">研时</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          :ellipsis="false"
          router
          class="header-menu"
        >
          <el-menu-item index="/articles">
            <el-icon><Document /></el-icon>
            <span>时政文章</span>
          </el-menu-item>
          <el-menu-item index="/knowledge">
            <el-icon><Reading /></el-icon>
            <span>知识点</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <el-icon><DataAnalysis /></el-icon>
            <span>统计分析</span>
          </el-menu-item>
        </el-menu>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="layout-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <!-- 底部 -->
    <el-footer class="layout-footer">
      <div class="footer-content">
        <p>© 2026 研时 - 考研时政智能分析系统</p>
      </div>
    </el-footer>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { Document, Reading, DataAnalysis } from '@element-plus/icons-vue'

const route = useRoute()

const activeMenu = computed(() => route.path)
</script>

<style scoped lang="scss">
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, var(--color-bg-1) 0%, var(--color-bg-2) 50%, var(--color-bg-3) 100%);
}

.layout-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  padding: 0;
  height: 64px;
  border-bottom: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.9);

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: var(--transition-base);

    &:hover {
      transform: scale(1.05);
    }

    .logo-icon {
      font-size: 24px;
    }

    .logo-text {
      font-size: 20px;
      font-weight: 600;
      color: var(--color-text-primary);
    }
  }

  .header-menu {
    border: none;
    background: transparent;
    flex: 1;
    justify-content: flex-end;

    .el-menu-item {
      border-bottom: none !important;

      &:hover {
        color: var(--color-wood-1) !important;
      }

      &.is-active {
        color: var(--color-wood-1) !important;
        border-bottom: 2px solid var(--color-wood-1) !important;
      }
    }
  }
}

.layout-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.layout-footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.8);
  color: var(--color-text-tertiary);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
