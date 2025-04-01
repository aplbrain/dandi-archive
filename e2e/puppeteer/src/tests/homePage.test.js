const VERSION_LINK_REGEX = /https:\/\/github.com\/dandi\/dandi-archive\/commit\/[0-9a-f]{5,40}/;

describe('home page stats', () => {
  // Skip test until we setup git tags and releases to control and enable version
  /* eslint-disable-next-line jest/no-disabled-tests */
  it.skip('checks version link', async () => {
    /* eslint-disable-next-line no-undef */
    const versionLink = await page.evaluate(() => document.querySelector('.version-link').getAttribute('href'));
    expect(versionLink).toMatch(VERSION_LINK_REGEX);
  });
});
