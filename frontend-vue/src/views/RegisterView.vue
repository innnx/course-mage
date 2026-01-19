<template>
  <div class="min-h-screen flex">
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <div class="flex items-center mb-8">
          <svg class="w-8 h-8 text-blue-600 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <h1 class="text-2xl font-bold text-gray-900">课程管理系统</h1>
        </div>

        <h2 class="text-3xl font-bold text-gray-900 mb-2">创建账户</h2>
        <p class="text-gray-600 mb-8">请填写以下信息注册</p>

        <div v-if="error" class="mb-4 p-4 bg-red-50 border border-red-200 text-red-600 rounded-lg">
          {{ error }}
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">昵称</label>
            <input
              v-model="formData.nickname"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              placeholder="请输入昵称"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">用户名</label>
            <input
              v-model="formData.username"
              type="text"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition"
              placeholder="4-20位字母、数字或下划线"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">密码</label>
            <div class="relative">
              <input
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition pr-12"
                placeholder="8-20位，包含大小写字母和数字"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
              >
                <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '注册中...' : '注册' }}
          </button>
        </form>

        <p class="mt-6 text-center text-gray-600">
          已有账户？
          <router-link to="/login" class="text-blue-600 hover:text-blue-700 font-medium">
            立即登录
          </router-link>
        </p>
      </div>
    </div>

    <div class="hidden lg:flex flex-1 bg-blue-600 items-center justify-center">
      <div class="text-center text-white p-12">
        <h2 class="text-4xl font-bold mb-4">加入我们</h2>
        <p class="text-blue-100 text-lg">开始您的学习或教学之旅</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { authAPI } from '../api/services';

const router = useRouter();

const formData = reactive({
  username: '',
  password: '',
  nickname: '',
});
const showPassword = ref(false);
const error = ref('');
const loading = ref(false);

const handleSubmit = async () => {
  error.value = '';
  loading.value = true;

  try {
    await authAPI.register(formData);
    // 注册成功后跳转到登录页
    router.push('/login');
  } catch (err) {
    error.value = err.message || '注册失败，请检查网络';
    console.error(err);
  } finally {
    loading.value = false;
  }
};
</script>
