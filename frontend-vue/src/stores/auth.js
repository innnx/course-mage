import { defineStore } from 'pinia';
import { ref, computed } from 'vue';

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null);
  const loading = ref(true);

  const init = () => {
    const token = localStorage.getItem('token');
    const userInfo = localStorage.getItem('userInfo');
    if (token && userInfo) {
      user.value = JSON.parse(userInfo);
    }
    loading.value = false;
  };

  const login = (token, userInfo) => {
    localStorage.setItem('token', token);
    localStorage.setItem('userInfo', JSON.stringify(userInfo));
    user.value = userInfo;
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('userInfo');
    user.value = null;
  };

  // Role checks
  const isAdmin = computed(() => user.value?.role === 'ADMIN');
  const isTeacher = computed(() => user.value?.role === 'TEACHER');
  const isStudent = computed(() => user.value?.role === 'STUDENT');

  // Management menu items based on role
  const managementMenuItems = computed(() => {
    const items = [];
    // 订单管理 - 所有角色可见
    items.push({ name: '订单管理', path: '/admin?tab=orders', icon: 'orders' });

    if (isAdmin.value) {
      // 管理员：可以管理分类
      items.unshift({ name: '分类管理', path: '/admin?tab=categories', icon: 'category' });
    }

    if (isAdmin.value || isTeacher.value) {
      // 教师和管理员：可以管理课程
      items.unshift({ name: '课程管理', path: '/admin', icon: 'course' });
    }

    return items;
  });

  init();

  return { user, loading, login, logout, isAdmin, isTeacher, isStudent, managementMenuItems };
});
