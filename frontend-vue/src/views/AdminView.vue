<template>
  <div class="min-h-screen bg-stone-50">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-md fixed top-0 left-0 right-0 z-50 border-b border-gray-100">
      <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center gap-4">
            <router-link to="/" class="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition">
              <div class="w-9 h-9 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
              </div>
              <span class="text-xl font-bold text-gray-900">CourseHub</span>
            </router-link>
            <div class="hidden sm:block w-px h-6 bg-gray-200"></div>
            <span class="hidden sm:inline px-3 py-1 bg-blue-100 text-blue-700 text-sm font-medium rounded-full">管理后台</span>
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

    <div class="flex pt-16">
      <!-- Sidebar -->
      <aside class="w-64 bg-white shadow-sm min-h-screen fixed left-0 top-16 border-r border-gray-100">
        <nav class="p-4">
          <ul class="space-y-1">
            <li>
              <button @click="activeMenu = 'courses'" :class="activeMenu === 'courses' ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'text-gray-600 hover:bg-gray-50 border border-transparent'" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                </svg>
                课程管理
              </button>
            </li>
            <li v-if="authStore.isAdmin">
              <button @click="activeMenu = 'categories'" :class="activeMenu === 'categories' ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'text-gray-600 hover:bg-gray-50 border border-transparent'" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                </svg>
                分类管理
              </button>
            </li>
            <li>
              <button @click="activeMenu = 'orders'" :class="activeMenu === 'orders' ? 'bg-blue-50 text-blue-600 border border-blue-200' : 'text-gray-600 hover:bg-gray-50 border border-transparent'" class="w-full flex items-center gap-3 px-4 py-3 rounded-lg transition font-medium">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
                </svg>
                订单管理
              </button>
            </li>
          </ul>
        </nav>
      </aside>

      <!-- Main Content -->
      <main class="ml-64 flex-1 p-8 max-w-7xl mx-auto w-full">
        <!-- Course Management -->
        <div v-if="activeMenu === 'courses'">
          <!-- Stats Cards -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
            <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-500">课程总数</div>
                  <div class="text-2xl font-bold text-gray-900">{{ courses.length }}</div>
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
                  <div class="text-sm text-gray-500">已上架</div>
                  <div class="text-2xl font-bold text-green-600">{{ courses.filter(c => c.status === 1).length }}</div>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-500">分类数</div>
                  <div class="text-2xl font-bold text-indigo-600">{{ categories.length }}</div>
                </div>
              </div>
            </div>
            <div class="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <div class="text-sm text-gray-500">教师数</div>
                  <div class="text-2xl font-bold text-orange-600">{{ uniqueTeachers }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Toolbar -->
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
            <div class="relative flex-1 max-w-md">
              <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input v-model="searchKeyword" type="text" placeholder="搜索课程..." class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" />
            </div>
            <button @click="openCourseModal()" class="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
              </svg>
              新增课程
            </button>
          </div>

          <!-- Course Table -->
          <div class="bg-white rounded-xl shadow-md overflow-hidden">
            <table class="w-full">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">课程标题</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">分类</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">教师</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">价格</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">状态</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">操作</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                <tr v-if="loading">
                  <td colspan="6" class="px-6 py-12 text-center">
                    <div class="flex items-center justify-center">
                      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    </div>
                  </td>
                </tr>
                <tr v-else-if="filteredCourses.length === 0">
                  <td colspan="6" class="px-6 py-12 text-center text-gray-500">暂无课程</td>
                </tr>
                <template v-else>
                  <tr v-for="course in filteredCourses" :key="course.id" class="hover:bg-gray-50">
                    <td class="px-6 py-4">
                      <div class="font-medium text-gray-900">{{ course.title }}</div>
                      <div class="text-sm text-gray-500 truncate max-w-xs mt-1">{{ course.description }}</div>
                    </td>
                    <td class="px-6 py-4">
                      <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">{{ course.categoryName || '未分类' }}</span>
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex items-center gap-2">
                        <div class="w-8 h-8 bg-gradient-to-br from-orange-400 to-pink-500 rounded-full flex items-center justify-center text-white text-xs">{{ (course.teacherName || 'T')[0] }}</div>
                        <span class="text-gray-900">{{ course.teacherName }}</span>
                      </div>
                    </td>
                    <td class="px-6 py-4"><span class="text-green-600 font-semibold">¥{{ course.price }}</span></td>
                    <td class="px-6 py-4">
                      <span :class="course.status === 1 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'" class="px-2 py-1 text-xs rounded-full">{{ course.status === 1 ? '已上架' : '已下架' }}</span>
                    </td>
                    <td class="px-6 py-4 text-right">
                      <div class="flex items-center justify-end gap-2">
                        <button @click="openCourseModal(course)" class="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition" title="编辑">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                          </svg>
                        </button>
                        <button @click="handleToggleStatus(course)" class="p-2 text-yellow-600 hover:bg-yellow-50 rounded-lg transition" :title="course.status === 1 ? '下架' : '上架'">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                          </svg>
                        </button>
                        <button @click="handleDelete(course.id)" class="p-2 text-red-600 hover:bg-red-50 rounded-lg transition" title="删除">
                          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Category Management -->
        <div v-else-if="activeMenu === 'categories'">
          <CategoryManageView :embedded="true" @navigate="activeMenu = 'courses'" />
        </div>

        <!-- Order Management -->
        <div v-else-if="activeMenu === 'orders'">
          <OrderManageView :embedded="true" />
        </div>
      </main>
    </div>

    <!-- Course Modal -->
    <Teleport to="body">
      <div v-if="showCourseModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-xl shadow-xl w-full max-w-lg">
          <div class="flex justify-between items-center px-6 py-4 border-b">
            <h3 class="text-lg font-semibold">{{ editingCourse ? '编辑课程' : '新增课程' }}</h3>
            <button @click="closeCourseModal" class="p-2 text-gray-400 hover:text-gray-600 transition">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <form @submit.prevent="handleCourseSubmit" class="p-6 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">课程标题 *</label>
              <input v-model="courseForm.title" type="text" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="请输入课程标题" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">课程描述</label>
              <textarea v-model="courseForm.description" rows="3" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="请输入课程描述"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">价格 *</label>
                <input v-model="courseForm.price" type="number" step="0.01" min="0" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none" placeholder="0.00" required />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">分类</label>
                <select v-model="courseForm.categoryId" class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none">
                  <option value="">请选择分类</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>
            </div>
            <div class="flex justify-end gap-3 pt-4">
              <button type="button" @click="closeCourseModal" class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition">取消</button>
              <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">保存</button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { courseAPI, categoryAPI } from '../api/services';
import { useAuthStore } from '../stores/auth';
import CategoryManageView from './CategoryManageView.vue';
import OrderManageView from './OrderManageView.vue';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const activeMenu = ref('courses');
const courses = ref([]);
const categories = ref([]);
const loading = ref(true);
const searchKeyword = ref('');
const showCourseModal = ref(false);
const editingCourse = ref(null);
const courseForm = reactive({ title: '', description: '', price: '', categoryId: '' });

const uniqueTeachers = computed(() => new Set(courses.value.map(c => c.teacherName).filter(Boolean)).size);
const filteredCourses = computed(() => courses.value.filter(c => c.title?.toLowerCase().includes(searchKeyword.value.toLowerCase()) || c.description?.toLowerCase().includes(searchKeyword.value.toLowerCase())));

const fetchData = async () => {
  try {
    const [coursesRes, categoriesRes] = await Promise.all([courseAPI.getList({ pageNum: 1, pageSize: 100 }), categoryAPI.getList()]);
    courses.value = coursesRes.records || [];
    categories.value = categoriesRes || [];
  } catch (err) { console.error('获取数据失败', err); }
  finally { loading.value = false; }
};

const handleLogout = () => { authStore.logout(); router.push('/'); };

const openCourseModal = (course = null) => {
  if (course) { editingCourse.value = course; courseForm.title = course.title; courseForm.description = course.description || ''; courseForm.price = course.price || ''; courseForm.categoryId = course.categoryId || ''; }
  else { editingCourse.value = null; courseForm.title = ''; courseForm.description = ''; courseForm.price = ''; courseForm.categoryId = ''; }
  showCourseModal.value = true;
};

const closeCourseModal = () => { showCourseModal.value = false; editingCourse.value = null; };

const handleCourseSubmit = async () => {
  try {
    const data = { title: courseForm.title, description: courseForm.description, price: parseFloat(courseForm.price) || 0, categoryId: courseForm.categoryId ? parseInt(courseForm.categoryId) : null };
    if (editingCourse.value) await courseAPI.update(editingCourse.value.id, data);
    else await courseAPI.create(data);
    closeCourseModal(); fetchData();
  } catch (err) { console.error('保存失败', err); alert(err.message || '保存失败'); }
};

const handleToggleStatus = async (course) => {
  try { await courseAPI.updateStatus(course.id, course.status === 1 ? 0 : 1); fetchData(); }
  catch (err) { console.error('状态更新失败', err); alert(err.message || '状态更新失败'); }
};

const handleDelete = async (id) => {
  if (!confirm('确定要删除此课程吗？')) return;
  try { await courseAPI.delete(id); fetchData(); }
  catch (err) { console.error('删除失败', err); alert(err.message || '删除失败'); }
};

onMounted(() => {
  // Check URL query parameter for initial tab
  const tab = route.query.tab;
  if (tab === 'categories') {
    activeMenu.value = 'categories';
  } else if (tab === 'orders') {
    activeMenu.value = 'orders';
  }
  fetchData();
});

// Watch for route changes to update tab
watch(() => route.query.tab, (newTab) => {
  if (newTab === 'categories') {
    activeMenu.value = 'categories';
  } else if (newTab === 'orders') {
    activeMenu.value = 'orders';
  }
});
</script>
