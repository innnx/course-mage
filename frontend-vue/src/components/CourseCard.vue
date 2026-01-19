<template>
  <div class="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100">
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
      <div class="absolute top-3 right-3 flex gap-2">
        <span class="px-2 py-1 bg-white/90 backdrop-blur text-xs font-medium text-gray-600 rounded-full">
          {{ course.categoryName || '未分类' }}
        </span>
        <span
          v-if="course.status === 0"
          class="px-2 py-1 bg-red-500/90 backdrop-blur text-xs font-medium text-white rounded-full"
        >
          已下架
        </span>
      </div>
    </div>

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

    <div class="px-5 pb-5 flex gap-2">
      <router-link
        :to="`/course/${course.id}`"
        class="flex-1 py-2.5 text-center text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition font-medium text-sm"
      >
        查看详情
      </router-link>
      <button
        @click="$emit('purchase', course)"
        :disabled="purchasingId === course.id || course.status !== 1"
        class="flex-1 py-2.5 bg-gray-900 text-white rounded-lg hover:bg-gray-800 transition font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {{ purchasingId === course.id ? '下单中...' : (course.status !== 1 ? '已下架' : '立即购买') }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  course: {
    type: Object,
    required: true
  },
  purchasingId: {
    type: Number,
    default: null
  }
});

defineEmits(['purchase']);
</script>