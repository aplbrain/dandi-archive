<template>
  <DandisetsPage
    title="Starred EMBERsets"
    starred
  >
    <template #empty>
      <v-alert
        type="info"
        text
      >
        You haven't starred any EMBERsets yet.
      </v-alert>
    </template>
  </DandisetsPage>
</template>

<script setup lang="ts">
import DandisetsPage from '@/components/DandisetsPage.vue';
</script>
