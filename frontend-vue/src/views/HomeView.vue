<template>
  <div class="min-h-screen bg-stone-50">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <span class="text-xl font-semibold text-gray-900">CourseHub</span>
          </div>
          <div class="flex items-center gap-4">
            <router-link
              to="/courses"
              class="px-4 py-2 text-gray-600 hover:text-gray-900 transition"
            >
              课程列表
            </router-link>
            <template v-if="authStore.user">
              <router-link
                to="/my-orders"
                class="px-4 py-2 text-gray-600 hover:text-gray-900 transition"
              >
                我的订单
              </router-link>
              <!-- Management Dropdown (only show if has management items) -->
              <div v-if="authStore.managementMenuItems.length > 0" class="relative group">
                <button class="px-4 py-2 text-gray-600 hover:text-gray-900 transition flex items-center gap-1">
                  管理
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                  </svg>
                </button>
                <div class="absolute right-0 top-full mt-1 w-40 bg-white rounded-lg shadow-lg border border-gray-100 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50">
                  <router-link
                    v-for="item in authStore.managementMenuItems"
                    :key="item.path"
                    :to="item.path"
                    class="block px-4 py-2 text-gray-600 hover:bg-gray-50 hover:text-gray-900 first:rounded-t-lg last:rounded-b-lg"
                  >
                    {{ item.name }}
                  </router-link>
                </div>
              </div>
              <div class="flex items-center gap-2 pl-4 border-l border-gray-200">
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                  {{ authStore.user.username?.charAt(0).toUpperCase() || 'U' }}
                </div>
                <span class="text-gray-700 font-medium">{{ authStore.user.username }}</span>
                <button
                  @click="handleLogout"
                  class="text-gray-500 hover:text-red-600 transition text-sm"
                >
                  退出
                </button>
              </div>
            </template>
            <template v-else>
              <router-link
                to="/login"
                class="px-4 py-2 text-gray-600 hover:text-gray-900 transition"
              >
                登录
              </router-link>
            </template>
          </div>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="text-center max-w-3xl mx-auto">
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 mb-6 leading-tight">
            发现
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-600">优质课程</span>
            <br />
            开启学习之旅
          </h1>
          <p class="text-lg sm:text-xl text-gray-600 mb-8">
            汇聚业界名师，提供精品课程，助力你的成长与蜕变
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              @click="scrollToCourses"
              class="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium shadow-lg shadow-blue-500/25"
            >
              浏览课程
            </button>
            <button class="px-8 py-3 bg-white text-gray-700 border border-gray-200 rounded-lg hover:bg-gray-50 transition font-medium">
              了解更多
            </button>
          </div>
        </div>

        <!-- Stats -->
        <div class="mt-16 grid grid-cols-3 gap-8 max-w-2xl mx-auto">
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">{{ courses.length }}+</div>
            <div class="text-sm text-gray-500 mt-1">精选课程</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">50+</div>
            <div class="text-sm text-gray-500 mt-1">优秀教师</div>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-gray-900">1000+</div>
            <div class="text-sm text-gray-500 mt-1">学员已加入</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Course Section -->
    <section id="courses" class="py-16 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-10">
          <div>
            <h2 class="text-2xl sm:text-3xl font-bold text-gray-900">全部课程</h2>
            <p class="text-gray-500 mt-2">从入门到进阶，系统学习</p>
          </div>
        </div>

        <div v-if="loading" class="flex items-center justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>

        <div v-else-if="error" class="text-center py-20">
          <div class="text-red-500">{{ error }}</div>
        </div>

        <div v-else-if="courses.length === 0" class="text-center py-20">
          <div class="w-24 h-24 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <p class="text-gray-500">暂无课程</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div
            v-for="course in courses"
            :key="course.id"
            class="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100"
          >
            <!-- Card Header -->
            <div class="h-40 bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center relative overflow-hidden">
              <img
                v-if="course.coverImage"
                :src="course.coverImage"
                :alt="course.title"
                class="absolute inset-0 w-full h-full object-cover"
              />
              <div class="absolute inset-0 bg-gradient-to-br from-blue-500/60 to-indigo-600/60"></div>
              <svg v-if="!course.coverImage" class="w-16 h-16 text-white/50 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              <div class="absolute top-3 right-3">
                <span class="px-2 py-1 bg-white/90 backdrop-blur text-xs font-medium text-gray-600 rounded-full">
                  {{ course.categoryName || '未分类' }}
                </span>
              </div>
            </div>

            <!-- Card Body -->
            <div class="p-5">
              <router-link :to="`/course/${course.id}`" class="block">
                <h3 class="font-semibold text-gray-900 mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
                  {{ course.title }}
                </h3>
              </router-link>
              <p class="text-sm text-gray-500 mb-4 line-clamp-2">
                {{ course.description || '暂无描述' }}
              </p>

              <div class="flex items-center justify-between pt-4 border-t border-gray-50">
                <div class="flex items-center gap-2">
                  <div class="w-6 h-6 bg-gradient-to-br from-orange-400 to-pink-500 rounded-full flex items-center justify-center text-white text-xs font-medium">
                    {{ (course.teacherName || 'T')[0] }}
                  </div>
                  <span class="text-sm text-gray-600">{{ course.teacherName || '未知教师' }}</span>
                </div>
                <div class="flex items-center gap-1">
                  <svg class="w-4 h-4 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" />
                  </svg>
                  <span class="font-semibold text-gray-900">¥{{ course.price || 0 }}</span>
                </div>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="px-5 pb-5 flex gap-2">
              <router-link
                :to="`/course/${course.id}`"
                class="flex-1 py-2.5 text-center text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition font-medium text-sm"
              >
                查看详情
              </router-link>
              <button
                @click="handleCreateOrder(course)"
                :disabled="purchasingId === course.id"
                class="flex-1 py-2.5 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-medium text-sm disabled:opacity-50"
              >
                {{ purchasingId === course.id ? '下单中...' : '立即购买' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
            </div>
            <span class="font-semibold text-gray-900">CourseHub</span>
          </div>
          <p class="text-sm text-gray-500">
            &copy; 2024 CourseHub. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { courseAPI, orderAPI } from '../api/services';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const courses = ref([]);
const loading = ref(true);
const error = ref(null);
const purchasingId = ref(null);

const fetchCourses = async () => {
  try {
    const data = await courseAPI.getList({ pageNum: 1, pageSize: 20 });
    courses.value = data.records || [];
  } catch (err) {
    error.value = '获取课程列表失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const scrollToCourses = () => {
  document.getElementById('courses')?.scrollIntoView({ behavior: 'smooth' });
};

const handleLogout = () => {
  authStore.logout();
};

const handleCreateOrder = async (course) => {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  purchasingId.value = course.id;
  try {
    const orderNo = await orderAPI.create({ courseId: course.id });
    alert(`订单创建成功！订单号：${orderNo}\n\n请在订单列表中完成支付。`);
    router.push('/my-orders');
  } catch (err) {
    alert(err.message || '下单失败，请重试');
  } finally {
    purchasingId.value = null;
  }
};

onMounted(() => {
  fetchCourses();
});
</script>
