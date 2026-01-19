<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <router-link to="/" class="flex items-center gap-2 text-gray-600 hover:text-gray-900">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          返回首页
        </router-link>
        <router-link
          v-if="authStore.user"
          to="/admin"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          管理后台
        </router-link>
        <router-link
          v-else
          to="/login"
          class="px-4 py-2 text-gray-600 hover:text-gray-900 transition"
        >
          登录
        </router-link>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 py-8">
      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="text-center py-20">
        <div class="text-red-500 mb-4">{{ error }}</div>
        <router-link to="/" class="text-blue-600 hover:text-blue-700">
          返回首页
        </router-link>
      </div>

      <!-- Course Detail -->
      <div v-else-if="course" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2">
          <!-- Course Image -->
          <div class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl h-80 flex items-center justify-center mb-8 relative overflow-hidden">
            <img
              v-if="course.coverImage"
              :src="course.coverImage"
              :alt="course.title"
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/50 to-indigo-600/50"></div>
            <svg v-if="!course.coverImage" class="w-24 h-24 text-white/50 relative z-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>

          <!-- Course Info -->
          <div class="bg-white rounded-xl shadow-sm p-8">
            <div class="flex items-center gap-3 mb-4">
              <span class="px-3 py-1 bg-blue-100 text-blue-700 text-sm rounded-full">
                {{ course.categoryName || '未分类' }}
              </span>
              <span
                :class="course.status === 1 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
                class="px-3 py-1 text-sm rounded-full"
              >
                {{ course.status === 1 ? '已上架' : '已下架' }}
              </span>
            </div>

            <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ course.title }}</h1>

            <div class="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-pink-500 rounded-full flex items-center justify-center text-white font-medium">
                  {{ (course.teacherName || 'T')[0] }}
                </div>
                <div>
                  <div class="text-sm text-gray-500">教师</div>
                  <div class="font-medium text-gray-900">{{ course.teacherName }}</div>
                </div>
              </div>
              <div class="w-px h-10 bg-gray-200"></div>
              <div>
                <div class="text-sm text-gray-500">学生数</div>
                <div class="font-medium text-gray-900">{{ course.studentCount || 0 }} 人</div>
              </div>
            </div>

            <div class="prose max-w-none">
              <h3 class="text-xl font-semibold text-gray-900 mb-3">课程描述</h3>
              <p class="text-gray-600 leading-relaxed">
                {{ course.description || '暂无描述' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm p-6 sticky top-24">
            <div class="text-center mb-6">
              <div class="text-4xl font-bold text-gray-900 mb-2">¥{{ course.price }}</div>
              <div class="text-gray-500">课程价格</div>
            </div>

            <div v-if="authStore.user">
              <button
                v-if="hasPurchased"
                disabled
                class="w-full py-3 bg-green-600 text-white rounded-lg font-medium mb-3"
              >
                已购买
              </button>
              <button
                v-else
                @click="handlePurchase"
                :disabled="purchasing"
                class="w-full py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition disabled:opacity-50"
              >
                {{ purchasing ? '购买中...' : '立即购买' }}
              </button>
              <p v-if="purchaseMessage" class="text-center text-sm mt-2" :class="purchaseSuccess ? 'text-green-600' : 'text-red-600'">
                {{ purchaseMessage }}
              </p>
            </div>

            <router-link
              v-else
              to="/login"
              class="block w-full py-3 text-center bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition"
            >
              登录后购买
            </router-link>

            <div class="mt-6 pt-6 border-t border-gray-100">
              <h4 class="font-medium text-gray-900 mb-3">课程包含</h4>
              <ul class="space-y-2 text-sm text-gray-600">
                <li class="flex items-center gap-2">
                  <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  完整课程内容
                </li>
                <li class="flex items-center gap-2">
                  <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  终身学习权限
                </li>
                <li class="flex items-center gap-2">
                  <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  教师答疑支持
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { courseAPI, orderAPI } from '../api/services';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const course = ref(null);
const loading = ref(true);
const error = ref(null);
const hasPurchased = ref(false);
const purchasing = ref(false);
const purchaseMessage = ref('');
const purchaseSuccess = ref(false);

const fetchCourse = async () => {
  try {
    const data = await courseAPI.getById(route.params.id);
    course.value = data;
  } catch (err) {
    error.value = '获取课程详情失败';
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const checkPurchase = async () => {
  if (!authStore.user) return;
  try {
    const result = await orderAPI.checkPurchase(route.params.id);
    hasPurchased.value = result;
  } catch (err) {
    console.error('检查购买状态失败', err);
  }
};

const handlePurchase = async () => {
  if (!authStore.user) {
    router.push('/login');
    return;
  }

  purchasing.value = true;
  purchaseMessage.value = '';

  try {
    const orderNo = await orderAPI.create({ courseId: course.value.id });
    purchaseMessage.value = `订单创建成功！订单号：${orderNo}\n\n请在订单列表中完成支付。`;
    router.push('/my-orders');
  } catch (err) {
    purchaseSuccess.value = false;
    purchaseMessage.value = err.message || '下单失败，请重试';
    console.error(err);
  } finally {
    purchasing.value = false;
  }
};

onMounted(() => {
  fetchCourse();
  checkPurchase();
});
</script>
