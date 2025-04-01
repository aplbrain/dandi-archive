const VERSION_LINK_REGEX = /https:\/\/github.com\/dandi\/dandi-archive\/commit\/[0-9a-f]{5,40}/;

describe('home page stats', () => {
  // TODO: Re-enable test when <a class="version-link" > is uncommented from DandiFooter.vue
  //    The commented out div displays the version, which is pulled from git tags. In EMBER-DANDI,
  //    are not currently using tags, so the version displays as unknown.

  // it('checks version link', async () => {
  //   /* eslint-disable-next-line no-undef */
  //   const versionLink = await page.evaluate(() => document.querySelector('.version-link').getAttribute('href'));
  //   expect(versionLink).toMatch(VERSION_LINK_REGEX);
  // });
});
