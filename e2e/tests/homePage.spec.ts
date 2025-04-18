import { test, expect } from "@playwright/test";
import { clientUrl, dismissCookieBanner } from "../utils.ts";

const VERSION_LINK_REGEX = /https:\/\/github.com\/dandi\/dandi-archive\/commit\/[0-9a-f]{5,40}/;

test.describe("Home page stats", async () => {
  // Skip test until we setup git tags and releases to control and enable version
  /* eslint-disable-next-line jest/no-disabled-tests */
  test.skip("check version link", async ({ page }) => {
    await page.goto(clientUrl);
    await dismissCookieBanner(page);
    const versionLinkElement = await page.locator(".version-link").first();
    const versionLinkHref = await versionLinkElement.getAttribute("href");
    expect(versionLinkHref).toMatch(VERSION_LINK_REGEX);
  });
});
