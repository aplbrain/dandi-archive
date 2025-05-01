import { test, expect } from "@playwright/test";
import { clientUrl } from "../utils.ts";

const devDandisetId = "000003";

test.describe("File browser page", async () => {
  test("there is a file browser", async ({ page }) => {
    await page.goto(`${clientUrl}/#/dandiset/${devDandisetId}`);
    await page.getByRole("link", { name: "Files" }).click()

    // Ensure the page has loaded with a folder
    await expect(page.getByText("foo")).toHaveCount(1);
  });
});
