<template>
  <div class="min-h-screen bg-stone-50">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/" class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </div>
              <span class="hidden sm:inline">返回首页</span>
            </router-link>
            <div class="hidden sm:block w-px h-6 bg-gray-200"></div>
            <h1 class="text-xl font-bold text-gray-900">我的订单</h1>
          </div>
          <div class="flex items-center gap-3">
            <router-link
              to="/courses"
              class="px-3 py-2 text-gray-600 hover:text-gray-900 transition hidden sm:flex items-center gap-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
              </svg>
              浏览课程
            </router-link>
            <!-- Management Dropdown (only show if has management items) -->
            <div v-if="authStore.managementMenuItems.length > 0" class="relative group hidden sm:block">
              <button class="px-3 py-2 text-gray-600 hover:text-gray-900 transition flex items-center gap-1 text-sm">
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
            <div class="hidden sm:block w-px h-6 bg-gray-200"></div>
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-sm font-medium">
                {{ authStore.user?.username?.charAt(0).toUpperCase() || 'U' }}
              </div>
              <span class="text-gray-700 font-medium hidden sm:inline">{{ authStore.user?.username }}</span>
            </div>
            <button
              @click="handleLogout"
              class="p-2 text-gray-500 hover:text-red-600 transition rounded-lg hover:bg-gray-100"
              title="退出登录"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="pt-20 max-w-5xl mx-auto px-4 py-8">
      <!-- Tabs -->
      <div class="flex gap-2 mb-6 bg-white rounded-lg p-1 shadow-sm">
        <button
          @click="activeTab = 'all'"
          :class="activeTab === 'all' ? 'bg-blue-600 text-white shadow' : 'text-gray-600 hover:bg-gray-50'"
          class="flex-1 px-4 py-2.5 rounded-md font-medium transition"
        >
          全部订单
          <span class="ml-1 text-xs opacity-75">({{ orders.length }})</span>
        </button>
        <button
          @click="activeTab = 'pending'"
          :class="activeTab === 'pending' ? 'bg-blue-600 text-white shadow' : 'text-gray-600 hover:bg-gray-50'"
          class="flex-1 px-4 py-2.5 rounded-md font-medium transition"
        >
          待支付
          <span class="ml-1 text-xs opacity-75">({{ pendingCount }})</span>
        </button>
        <button
          @click="activeTab = 'paid'"
          :class="activeTab === 'paid' ? 'bg-blue-600 text-white shadow' : 'text-gray-600 hover:bg-gray-50'"
          class="flex-1 px-4 py-2.5 rounded-md font-medium transition"
        >
          已支付
          <span class="ml-1 text-xs opacity-75">({{ paidCount }})</span>
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredOrders.length === 0" class="bg-white rounded-xl shadow-sm p-12 text-center">
        <div class="w-20 h-20 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <p class="text-gray-500 mb-4 text-lg">暂无订单</p>
        <router-link to="/courses" class="inline-block px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium">
          去浏览课程
        </router-link>
      </div>

      <!-- Orders -->
      <div v-else class="space-y-4">
        <div
          v-for="order in filteredOrders"
          :key="order.id"
          class="bg-white rounded-xl shadow-sm overflow-hidden hover:shadow-md transition-shadow"
        >
          <!-- Order Header -->
          <div class="px-6 py-4 bg-gray-50 flex flex-wrap justify-between items-center gap-4 border-b border-gray-100">
            <div class="flex items-center gap-6 text-sm">
              <div>
                <span class="text-gray-500">订单号</span>
                <span class="ml-2 font-mono text-gray-900">{{ order.orderNo }}</span>
              </div>
              <div>
                <span class="text-gray-500">创建时间</span>
                <span class="ml-2 text-gray-900">{{ formatTime(order.createTime) }}</span>
              </div>
            </div>
            <span
              :class="getStatusClass(order.status)"
              class="px-3 py-1 text-sm font-medium rounded-full"
            >
              {{ getStatusText(order.status) }}
            </span>
          </div>

          <!-- Order Content -->
          <div class="p-6">
            <div class="flex items-start gap-4">
              <!-- Course Image Placeholder -->
              <div class="w-24 h-24 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-10 h-10 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>

              <!-- Course Info -->
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-gray-900 text-lg mb-1">{{ order.courseTitle || '未知课程' }}</h3>
                <p class="text-gray-500 text-sm line-clamp-2 mb-3">{{ order.courseDescription || '暂无描述' }}</p>
                <div class="flex items-center gap-4 text-sm text-gray-500">
                  <span>{{ order.teacherName ? `教师: ${order.teacherName}` : '' }}</span>
                </div>
              </div>

              <!-- Price -->
              <div class="text-right flex-shrink-0">
                <div class="text-sm text-gray-500 mb-1">订单金额</div>
                <div class="text-2xl font-bold text-gray-900">¥{{ formatPrice(order.price) }}</div>
              </div>
            </div>

            <!-- Actions -->
            <div class="mt-6 pt-4 border-t border-gray-100 flex justify-end gap-3">
              <router-link
                v-if="getStatusCode(order.status) === 1"
                :to="`/course/${order.courseId}`"
                class="px-4 py-2 text-blue-600 hover:bg-blue-50 rounded-lg transition font-medium"
              >
                查看课程
              </router-link>
              <button
                v-if="getStatusCode(order.status) === 0"
                @click="handlePay(order)"
                :disabled="payingOrderId === order.id"
                class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-medium disabled:opacity-50 flex items-center gap-2"
              >
                <svg v-if="payingOrderId === order.id" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
                {{ payingOrderId === order.id ? '支付中...' : '立即支付' }}
              </button>
              <button
                v-if="getStatusCode(order.status) === 0"
                @click="handleCancel(order)"
                :disabled="cancelingOrderId === order.id"
                class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition font-medium disabled:opacity-50"
              >
                {{ cancelingOrderId === order.id ? '取消中...' : '取消订单' }}
              </button>
              <span
                v-if="getStatusCode(order.status) === 2"
                class="px-4 py-2 text-gray-400"
              >
                已取消
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Stats -->
      <div v-if="orders.length > 0" class="mt-8 bg-white rounded-xl shadow-sm p-6">
        <div class="grid grid-cols-3 gap-6 text-center">
          <div>
            <div class="text-2xl font-bold text-gray-900">{{ orders.length }}</div>
            <div class="text-sm text-gray-500 mt-1">订单总数</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-green-600">{{ paidCount }}</div>
            <div class="text-sm text-gray-500 mt-1">已支付</div>
          </div>
          <div>
            <div class="text-2xl font-bold text-yellow-600">{{ pendingCount }}</div>
            <div class="text-sm text-gray-500 mt-1">待支付</div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { orderAPI } from '../api/services';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const orders = ref([]);
const loading = ref(true);
const activeTab = ref('all');
const payingOrderId = ref(null);
const cancelingOrderId = ref(null);

const pendingCount = computed(() => orders.value.filter(o => getStatusCode(o.status) === 0).length);
const paidCount = computed(() => orders.value.filter(o => getStatusCode(o.status) === 1).length);

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') return orders.value;
  if (activeTab.value === 'paid') return orders.value.filter(o => getStatusCode(o.status) === 1);
  if (activeTab.value === 'pending') return orders.value.filter(o => getStatusCode(o.status) === 0);
  return orders.value;
});

const formatTime = (time) => {
  if (!time) return '-';
  return new Date(time).toLocaleString('zh-CN');
};

// 处理价格显示（可能是BigDecimal对象或数字）
const formatPrice = (price) => {
  if (!price) return '0.00';
  if (typeof price === 'number') return price.toFixed(2);
  if (typeof price === 'object' && price.toString) return price.toString();
  return String(price);
};

// 获取状态码（处理枚举类型）
const getStatusCode = (status) => {
  if (status === null || status === undefined) return -1;
  // 如果是枚举对象，有code属性
  if (typeof status === 'object' && status.code !== undefined) {
    return status.code;
  }
  // 如果是枚举的name字符串
  if (typeof status === 'string') {
    if (status === 'PAID' || status === '已支付') return 1;
    if (status === 'PENDING' || status === '待支付') return 0;
    if (status === 'CANCELLED' || status === '已取消') return 2;
  }
  // 如果是数字
  return Number(status);
};

const getStatusClass = (status) => {
  const code = getStatusCode(status);
  switch (code) {
    case 1: return 'bg-green-100 text-green-700 border border-green-200';
    case 0: return 'bg-yellow-100 text-yellow-700 border border-yellow-200';
    case 2: return 'bg-gray-100 text-gray-600 border border-gray-200';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const getStatusText = (status) => {
  const code = getStatusCode(status);
  switch (code) {
    case 1: return '已支付';
    case 0: return '待支付';
    case 2: return '已取消';
    default: return '未知';
  }
};

const fetchOrders = async () => {
  try {
    const data = await orderAPI.getMyOrders({ pageNum: 1, pageSize: 100 });
    orders.value = data.records || [];
  } catch (err) {
    console.error('获取订单失败', err);
    alert(err.message || '获取订单失败');
  } finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

const handlePay = async (order) => {
  if (!confirm(`确定要支付订单 ${order.orderNo} 吗？\n支付金额：¥${formatPrice(order.price)}`)) return;

  payingOrderId.value = order.id;
  try {
    await orderAPI.pay(order.orderNo);
    order.status = 1;
    alert('支付成功！');
  } catch (err) {
    alert(err.message || '支付失败');
  } finally {
    payingOrderId.value = null;
  }
};

const handleCancel = async (order) => {
  if (!confirm('确定要取消此订单吗？取消后不可恢复。')) return;

  cancelingOrderId.value = order.id;
  try {
    await orderAPI.cancel(order.orderNo);
    order.status = 2;
  } catch (err) {
    alert(err.message || '取消失败');
  } finally {
    cancelingOrderId.value = null;
  }
};

onMounted(() => {
  fetchOrders();
});
</script>
