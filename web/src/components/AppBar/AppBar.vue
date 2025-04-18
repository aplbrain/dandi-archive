<template>
  <v-app-bar class="px-4">
    <v-menu
      v-if="isMobile"
      :close-delay="300"
      location="bottom"
    >
      <template #activator="{ props }">
        <v-app-bar-nav-icon v-bind="props" />
      </template>
      <v-list>
        <template v-for="navItem in navItems">
          <v-list-item
            v-if="!navItem.if || navItem.if()"
            :key="navItem.text"
            :to="navItem.external ? undefined : {name: navItem.to}"
            :href="navItem.external ? navItem.to : undefined"
            :target="navItem.external ? '_blank' : undefined"
            :rel="navItem.external ? 'noopener' : undefined"
            exact
          >
            <template v-if="!navItem.external">
              <v-list-item-title class="text-md">
                {{ navItem.text }}
              </v-list-item-title>
            </template>
            <template v-if="navItem.external">
              <div class="d-flex justify-space-between align-center">
                <v-list-item-title class="text-md">
                  {{ navItem.text }}
                </v-list-item-title>
                <v-icon
                  class="ml-1"
                  size="x-small"
                >
                  mdi-open-in-new
                </v-icon>
              </div>
            </template>
          </v-list-item>
        </template>
      </v-list>
    </v-menu>
    <router-link
      to="/"
      class="d-flex align-center text-decoration-none"
    >
      <v-img
        alt="EMBER logo"
        cover
        height="40px"
        width="30px"
        :src="logo"
        class="mr-3"
      />
      <span class="flex-grow-1 font-weight-bold mr-3 text-primary">EMBER-DANDI</span>
    </router-link>
    <v-toolbar-items v-if="!isMobile">
      <template v-for="navItem in navItems">
        <v-btn
          v-if="!navItem.external && (!navItem.if || navItem.if())"
          :key="navItem.text"
          :to="{name: navItem.to}"
          exact
          variant="text"
        >
          {{ navItem.text }}
        </v-btn>
        <v-btn
          v-if="navItem.external && (!navItem.if || navItem.if())"
          :key="navItem.text"
          :href="navItem.to"
          target="_blank"
          rel="noopener"
          variant="text"
        >
          {{ navItem.text }}
          <v-icon
            class="ml-1"
            size="small"
          >
            mdi-open-in-new
          </v-icon>
        </v-btn>
      </template>
    </v-toolbar-items>

    <v-spacer />

    <div v-if="!insideIFrame">
      <template v-if="loggedIn">
        <v-btn
          :disabled="!user?.approved"
          :to="{ name: 'createDandiset' }"
          class="mx-3"
          color="primary"
          variant="elevated"
          rounded="pill"
        >
          New Dandiset
        </v-btn>
        <UserMenu />
      </template>
      <template v-else>
        <v-tooltip
          location="bottom"
          :disabled="cookiesEnabled"
        >
          <template #activator="{ props }">
            <div v-bind="props">
              <v-btn
                id="login"
                class="mx-1"
                color="primary"
                variant="elevated"
                rounded="pill"
                :disabled="!cookiesEnabled"
                @click="login"
              >
                Log In with GitHub
              </v-btn>
            </div>
          </template>
          <span>Enable cookies to log in.</span>
        </v-tooltip>
      </template>
    </div>
  </v-app-bar>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useDisplay } from 'vuetify';

import {
  cookiesEnabled as cookiesEnabledFunc,
  loggedIn as loggedInFunc,
  insideIFrame as insideIFrameFunc,
  dandiRest,
  user,
} from '@/rest';
import {
  emberAboutUrl, dandiDocumentationUrl,
} from '@/utils/constants';
import UserMenu from '@/components/AppBar/UserMenu.vue';
import logo from '@/assets/ember-logo.png';

interface NavigationItem {
  text: string,
  to: string,
  if?(): boolean,
  external: boolean,
}

const display = useDisplay();
const isMobile = computed(() => display.mobile.value);

const cookiesEnabled = computed(cookiesEnabledFunc);
const loggedIn = computed(loggedInFunc);
const insideIFrame = computed(insideIFrameFunc);

const navItems: NavigationItem[] = [
  {
    text: 'Public Dandisets',
    to: 'publicDandisets',
    external: false,
  },
  {
    text: 'My Dandisets',
    to: 'myDandisets',
    external: false,
    if: loggedInFunc,
  },
  {
    text: 'Starred Dandisets',
    to: 'starredDandisets',
    external: false,
    if: loggedInFunc,
  },
  {
    text: 'About',
    to: emberAboutUrl,
    external: true,
  },
  {
    text: 'Documentation',
    to: dandiDocumentationUrl,
    external: true,
  },
  // {
  //   text: 'Help',
  //   to: dandiHelpUrl,
  //   external: true,
  // },
  // {
  //   text: 'DandiHub',
  //   to: dandihubUrl,
  //   external: true,
  // },
];

function login() {
  dandiRest.login();
}
</script>
