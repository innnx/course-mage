<template>
  <div :class="embedded ? '' : 'min-h-screen bg-stone-50'">
    <!-- Header (only show when not embedded) -->
    <header v-if="!embedded" class="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/admin" class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
              </div>
              <span class="hidden sm:inline">返回管理</span>
            </router-link>
            <div class="hidden sm:block w-px h-6 bg-gray-200"></div>
            <span class="text-xl font-bold text-gray-900">分类管理</span>
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
            <router-link
              to="/my-orders"
              class="px-3 py-2 text-gray-600 hover:text-gray-900 transition hidden sm:flex items-center gap-1"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              我的订单
            </router-link>
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

    <main :class="embedded ? '' : 'pt-24 max-w-4xl mx-auto px-4 py-8'">
      <!-- Page Header -->
      <div v-if="!embedded" class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-2">分类管理</h2>
        <p class="text-gray-600">管理课程分类</p>
      </div>

      <!-- Toolbar -->
      <div :class="embedded ? '' : 'bg-white rounded-xl shadow-sm p-4 mb-6'">
        <div class="flex justify-between items-center">
          <h3 :class="embedded ? 'text-lg font-semibold text-gray-900' : 'text-lg font-semibold text-gray-900'">
            {{ embedded ? '分类列表' : '分类列表' }}
          </h3>
          <button
            @click="openModal()"
            class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            新增分类
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Empty -->
      <div v-else-if="categories.length === 0" class="bg-white rounded-xl shadow-sm p-12 text-center">
        <div class="w-20 h-20 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
          <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
          </svg>
        </div>
        <p class="text-gray-500 text-lg mb-4">暂无分类</p>
        <button
          @click="openModal()"
          class="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition font-medium"
        >
          添加第一个分类
        </button>
      </div>

      <!-- Categories -->
      <div v-else class="bg-white rounded-xl shadow-sm overflow-hidden">
        <table class="w-full">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">分类名称</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">排序</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="category in categories" :key="category.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 text-gray-500">{{ category.id }}</td>
              <td class="px-6 py-4">
                <div class="font-medium text-gray-900">{{ category.name }}</div>
              </td>
              <td class="px-6 py-4 text-gray-500">{{ category.sort || 0 }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button
                    @click="openModal(category)"
                    class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition"
                    title="编辑"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="handleDelete(category.id)"
                    class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition"
                    title="删除"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-md">
          <div class="flex justify-between items-center px-6 py-4 border-b">
            <h3 class="text-lg font-semibold">{{ editingCategory ? '编辑分类' : '新增分类' }}</h3>
            <button
              @click="closeModal"
              class="p-2 text-gray-400 hover:text-gray-600 transition"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">分类名称 *</label>
              <input
                v-model="formData.name"
                type="text"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="请输入分类名称"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">排序</label>
              <input
                v-model="formData.sort"
                type="number"
                min="0"
                class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
                placeholder="数字越大越靠前"
              />
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
              >
                取消
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
              >
                保存
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { categoryAPI } from '../api/services';
import { useAuthStore } from '../stores/auth';

defineProps({
  embedded: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['navigate']);

const router = useRouter();
const authStore = useAuthStore();

const categories = ref([]);
const loading = ref(true);
const showModal = ref(false);
const editingCategory = ref(null);
const formData = reactive({
  name: '',
  sort: 0,
});

const fetchCategories = async () => {
  try {
    const data = await categoryAPI.getList();
    categories.value = data || [];
  } catch (err) {
    console.error('获取分类失败', err);
  } finally {
    loading.value = false;
  }
};

const handleLogout = () => {
  authStore.logout();
  router.push('/');
};

const openModal = (category = null) => {
  if (category) {
    editingCategory.value = category;
    formData.name = category.name;
    formData.sort = category.sort || 0;
  } else {
    editingCategory.value = null;
    formData.name = '';
    formData.sort = 0;
  }
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  editingCategory.value = null;
};

const handleSubmit = async () => {
  try {
    const data = {
      name: formData.name,
      sort: parseInt(formData.sort) || 0,
    };

    if (editingCategory.value) {
      data.id = editingCategory.value.id;
      await categoryAPI.update(data);
    } else {
      await categoryAPI.create(data);
    }
    closeModal();
    fetchCategories();
  } catch (err) {
    console.error('保存失败', err);
    alert(err.message || '保存失败');
  }
};

const handleDelete = async (id) => {
  if (!confirm('确定要删除此分类吗？')) return;
  try {
    await categoryAPI.delete(id);
    fetchCategories();
  } catch (err) {
    console.error('删除失败', err);
    alert(err.message || '删除失败');
  }
};

onMounted(() => {
  fetchCategories();
});
</script>
