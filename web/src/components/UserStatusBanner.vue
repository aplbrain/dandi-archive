<template>
  <v-banner
    v-if="bannerInfo"
    :bg-color="bannerInfo.color"
    lines="one"
    class="pb-5"
  >
    <template #prepend>
      <v-icon size="36">
        {{ bannerInfo.icon }}
      </v-icon>
    </template>
    <v-banner-text>
      {{ bannerInfo.text }}
    </v-banner-text>
  </v-banner>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { user } from '@/rest';

interface StatusBanner {
  text: string;
  icon: string;
  color: string;
}

const bannerInfo = computed<StatusBanner | null>(() => {
  switch (user.value?.status) {
    case 'PENDING':
      return {
        text: 'Your EMBER-DANDI account is currently pending approval. Please allow up to 2 business days for approval and contact the DANDI admins at help@emberarchive.org if you have any questions.',
        icon: 'mdi-timer-sand-empty',
        color: 'warning',
      };
    case 'REJECTED':
      return {
        text: 'Your EMBER-DANDI account was denied approval. Please contact the DANDI admin team at help@emberarchive.org if you would like to appeal this decision.',
        icon: 'mdi-close-octagon',
        color: 'error',
      };
    default:
      return null;
  }
});
</script>
