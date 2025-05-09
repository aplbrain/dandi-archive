const dandiUrl = 'https://dandiarchive.org';
const emberHomeUrl = 'https://emberarchive.org';
const emberAboutUrl = 'https://emberarchive.org/about';
const emberGitHubUrl = 'https://github.com/aplbrain/dandi-archive';
const dandiDocumentationUrl = 'https://emberarchive.org/documentation';
// const dandiAboutUrl = 'https://about.dandiarchive.org/';
const dandiHelpUrl = 'https://github.com/dandi/helpdesk/issues/new/choose';
const dandihubUrl = 'https://hub.dandiarchive.org/';
const sandboxDocsUrl = `${dandiDocumentationUrl}/getting-started/creating-account/`;

const draftVersion = 'draft';

const VALIDATION_ICONS = {
  // version metadata
  // https://github.com/dandi/schema/blob/master/releases/0.4.4/dandiset.json#L231
  name: 'mdi-note',
  description: 'mdi-text',
  contributor: 'mdi-account-multiple',
  license: 'mdi-gavel',
  assetsSummary: 'mdi-file-multiple',

  // asset metadata
  // https://github.com/dandi/schema/blob/master/releases/0.4.4/asset.json#L312
  contentSize: 'mdi-table-of-contents',
  encodingFormat: 'mdi-code-json',
  digest: 'mdi-barcode',
  path: 'mdi-folder-multiple',
  identifier: 'mdi-identifier',

  // icon to use when one isn't found
  DEFAULT: 'mdi-alert',
};

const sortingOptions = [
  {
    name: 'Modified',
    djangoField: 'modified',
  },
  {
    name: 'Identifier',
    djangoField: 'id',
  },
  {
    name: 'Name',
    djangoField: 'name',
  },
  {
    name: 'Size',
    djangoField: 'size',
  },
  {
    name: 'Stars',
    djangoField: 'stars',
  },
];

const DANDISETS_PER_PAGE = 8;

export {
  dandiUrl,
  emberHomeUrl,
  emberAboutUrl,
  emberGitHubUrl,
  dandiDocumentationUrl,
  dandihubUrl,
  sandboxDocsUrl,
  draftVersion,
  dandiHelpUrl,
  VALIDATION_ICONS,
  sortingOptions,
  DANDISETS_PER_PAGE,
};
