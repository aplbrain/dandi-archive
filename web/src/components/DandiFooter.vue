<template>
  <v-footer class="text-body-2">
    <v-container>
      <CookieBanner />
      <v-row>
        <v-col offset="2">
          &copy; 2019 - 2025 The DANDI Team<br>
          &copy; 2024 - 2025 JHU/APL.<br>
          <a
            target="_blank"
            rel="noopener"
            href="https://docs.dandiarchive.org/about/terms/"
            class="text-primary"
          >Terms</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon> / <a
            target="_blank"
            rel="noopener"
            href="https://docs.dandiarchive.org/about/policies/"
            class="text-primary"
          >Policies</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon> / <a
            target="_blank"
            rel="noopener"
            href="https://github.com/dandi/dandi-archive/blob/master/CODE_OF_CONDUCT.md"
            class="text-primary"
          >Code of Conduct</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          <span v-if="version != 'unknown'">
            version
            <a
              class="version-link"
              :href="githubLink"
              target="_blank"
              rel="noopener"
            >{{ version }}</a>
          </span>
        </v-col>
        <v-col>
          Funding / In-Kind Support:<br>
          - <a
            target="_blank"
            rel="noopener"
            href="https://braininitiative.nih.gov/"
            class="text-primary"
          >BRAIN Initiative</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon> <a
            target="_blank"
            rel="noopener"
            href="https://braininitiative.nih.gov/research/systems-neuroscience/brain-behavior-quantification-and-synchronization-program"
            class="text-primary"
          >BBQS Program</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          - <a
            target="_blank"
            rel="noopener"
            href="https://aws.amazon.com/opendata/"
            class="text-primary"
          >AWS Open Data</a>
          <!-- TODO: Update to registry link when released for EMBER: https://registry.opendata.aws/XXX/ -->
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          - <a
            target="_blank"
            rel="noopener"
            href="https://netlify.com"
            class="text-primary"
          >This site is powered by Netlify</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          - <a
            target="_blank"
            rel="noopener"
            href="https://sentry.io/"
            class="text-primary"
          >Sentry</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          - <a
            target="_blank"
            rel="noopener"
            :href="dandiUrl"
            class="text-primary"
          >DANDI</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
        </v-col>
        <v-col>
          Support:<br>
          - <a
            target="_blank"
            rel="noopener"
            href="mailto:help@emberarchive.org"
            class="text-primary"
          >Send an email</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
          <br>
          - <a
            target="_blank"
            rel="noopener"
            href="https://github.com/dandi/helpdesk/issues/new/choose"
            class="text-primary"
          >File an issue</a>
          <v-icon size="x-small">
            mdi-open-in-new
          </v-icon>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
import CookieBanner from './CookieBanner.vue';
import { dandiUrl } from '@/utils/constants';

const version = import.meta.env.VITE_APP_VERSION;
const githubLink = import.meta.env.VITE_APP_GIT_REVISION ? `https://github.com/aplbrain/dandi-archive/commit/${import.meta.env.VITE_APP_GIT_REVISION}` : 'https://github.com/aplbrain/dandi-archive';
</script>

<style scoped>
@media (min-width: 1904px) {
  .container {
    max-width: 1185px;
  }
}

.version-link {
  color: inherit;
}

.version-link:hover {
  text-decoration: underline;
}
</style>
