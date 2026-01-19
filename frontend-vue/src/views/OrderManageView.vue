<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-wrap justify-between items-center gap-4">
      <div>
        <h2 class="text-xl font-bold text-gray-900">订单管理</h2>
        <p class="text-gray-600">查看和管理所有订单</p>
      </div>
      <div class="flex items-center gap-3">
        <select
          v-model="statusFilter"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none bg-white"
        >
          <option value="">全部状态</option>
          <option value="0">待支付</option>
          <option value="1">已支付</option>
          <option value="2">已取消</option>
        </select>
        <button
          @click="fetchOrders(page)"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          刷新
        </button>
        <div class="text-sm text-gray-500">
          第 {{ page }} / {{ Math.ceil(total / size) || 1 }} 页
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div v-if="orders.length > 0" class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-gray-500">全部订单</div>
            <div class="text-2xl font-bold text-gray-900">{{ orders.length }}</div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-gray-500">待支付</div>
            <div class="text-2xl font-bold text-yellow-600">{{ pendingCount }}</div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-gray-500">已支付</div>
            <div class="text-2xl font-bold text-green-600">{{ paidCount }}</div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
          <div>
            <div class="text-sm text-gray-500">已取消</div>
            <div class="text-2xl font-bold text-gray-600">{{ canceledCount }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading -->
    <LoadingSpinner v-if="loading" />

    <!-- Empty -->
    <EmptyState v-else-if="orders.length === 0" message="暂无订单" />

    <!-- Orders Table -->
    <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">订单号</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">用户</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">课程</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">金额</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
            <th class="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase">创建时间</th>
            <th class="px-6 py-4 text-right text-xs font-medium text-gray-500 uppercase">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100">
          <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-4">
              <span class="font-mono text-sm text-gray-900">{{ order.orderNo }}</span>
            </td>
            <td class="px-6 py-4">
              <div class="flex items-center gap-2">
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white text-xs font-medium">
                  {{ (order.username || 'U')[0] }}
                </div>
                <div>
                  <div class="text-sm font-medium text-gray-900">{{ order.username }}</div>
                  <div class="text-sm text-gray-500">ID: {{ order.userId || '-' }}</div>
                </div>
              </div>
            </td>
            <td class="px-6 py-4">
              <div class="text-sm font-medium text-gray-900 max-w-xs truncate">{{ order.courseTitle }}</div>
            </td>
            <td class="px-6 py-4">
              <span class="text-sm font-bold text-gray-900">¥{{ order.price?.toFixed(2) || '0.00' }}</span>
            </td>
            <td class="px-6 py-4">
              <span
                :class="getStatusClass(order.status)"
                class="px-3 py-1 text-xs font-medium rounded-full"
              >
                {{ getStatusText(order.status) }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span class="text-sm text-gray-500">{{ formatTime(order.createTime) }}</span>
            </td>
            <td class="px-6 py-4 text-right">
              <div class="flex items-center justify-end gap-2">
                <button
                  v-if="order.status === 0"
                  @click="handlePay(order)"
                  class="px-3 py-1.5 bg-green-600 text-white text-xs rounded-lg hover:bg-green-700 transition"
                  title="手动支付"
                >
                  支付
                </button>
                <button
                  v-if="order.status === 0"
                  @click="handleCancel(order)"
                  class="px-3 py-1.5 text-gray-600 bg-gray-100 text-xs rounded-lg hover:bg-gray-200 transition"
                  title="取消订单"
                >
                  取消
                </button>
                <span
                  v-if="order.status !== 0"
                  class="text-xs text-gray-400"
                >
                  {{ order.status === 1 ? '已完成' : '已取消' }}
                </span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div v-if="total > 0" class="flex justify-center items-center gap-4">
      <button
        @click="fetchOrders(page - 1)"
        :disabled="page === 1"
        class="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        上一页
      </button>
      <span class="text-gray-600">
        第 {{ page }} / {{ Math.ceil(total / size) }} 页，共 {{ total }} 条
      </span>
      <button
        @click="fetchOrders(page + 1)"
        :disabled="page >= Math.ceil(total / size)"
        class="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        下一页
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { orderAPI } from '../api/services';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import EmptyState from '../components/EmptyState.vue';

defineProps({
  embedded: {
    type: Boolean,
    default: false,
  },
});

const orders = ref([]);
const loading = ref(true);
const page = ref(1);
const size = ref(10);
const total = ref(0);
const statusFilter = ref('');

const pendingCount = computed(() => orders.value.filter(o => o.status === 0).length);
const paidCount = computed(() => orders.value.filter(o => o.status === 1).length);
const canceledCount = computed(() => orders.value.filter(o => o.status === 2).length);

const filteredOrders = computed(() => orders.value);

const formatTime = (time) => {
  if (!time) return '-';
  return new Date(time).toLocaleString('zh-CN');
};

const getStatusClass = (status) => {
  const statusNum = typeof status === 'string' ? parseInt(status) : status;
  switch (statusNum) {
    case 1: return 'bg-green-100 text-green-700';
    case 0: return 'bg-yellow-100 text-yellow-700';
    case 2: return 'bg-gray-100 text-gray-600';
    default: return 'bg-gray-100 text-gray-600';
  }
};

const getStatusText = (status) => {
  const statusNum = typeof status === 'string' ? parseInt(status) : status;
  switch (statusNum) {
    case 1: return '已支付';
    case 0: return '待支付';
    case 2: return '已取消';
    default: return '未知';
  }
};

const fetchOrders = async (pageNum = 1) => {
  loading.value = true;
  try {
    const params = {
      pageNum: parseInt(pageNum),
      pageSize: parseInt(size.value),
    };
    if (statusFilter.value !== '' && statusFilter.value !== null) {
      params.status = parseInt(statusFilter.value);
    }
    const data = await orderAPI.getList(params);
    orders.value = data.records || [];
    total.value = data.total || 0;
    page.value = parseInt(pageNum);
  } catch (err) {
    console.error('获取订单列表失败', err);
  } finally {
    loading.value = false;
  }
};

const handlePay = async (order) => {
  if (!confirm(`确定要将订单 ${order.orderNo} 标记为已支付吗？`)) return;
  try {
    await orderAPI.pay(order.orderNo);
    order.status = 1;
  } catch (err) {
    alert(err.message || '操作失败');
  }
};

const handleCancel = async (order) => {
  if (!confirm('确定要取消此订单吗？')) return;
  try {
    await orderAPI.cancel(order.orderNo);
    order.status = 2;
  } catch (err) {
    alert(err.message || '取消失败');
  }
};

watch(statusFilter, () => {
  fetchOrders(1);
});

onMounted(() => {
  fetchOrders();
});
</script>
