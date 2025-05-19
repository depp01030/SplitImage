chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "split-image-api",
    title: "送到本地分割 API",
    contexts: ["image"]
  });
});
// 📌 新增右鍵選單：針對頁面（非圖片）
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "split-page-url-api",
    title: "送出整頁圖片給後端分析",
    contexts: ["page"]
  });
});
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "split-page-url-api") {
    const pageUrl = tab.url;

    fetch("http://localhost:8888/split/page_url", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ url: pageUrl })
    })
      .then(res => {
        if (!res.ok) throw new Error("HTTP error: " + res.status);
        return res.json();
      })
      .then(data => {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "頁面分析完成",
          message: `共分割出圖片數量：${data.num_sub_images}`
        });
      })
      .catch(err => {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "頁面分析失敗",
          message: err.message
        });
        console.error("Extension error:", err);
      });
  }
  if (info.menuItemId === "split-image-api") {
    fetch("http://localhost:8888/split/url", {
      method: "POST",
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: new URLSearchParams({url: info.srcUrl})
    })
    .then(res => {
      if (!res.ok) throw new Error("HTTP error: " + res.status);
      return res.json();
    })
    .then(data => {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: "圖片分割完成",
        message: `產生子圖數量：${data.num_sub_images}`
      });
    })
    .catch(err => {
      chrome.notifications.create({
        type: "basic",
        iconUrl: "icon.png",
        title: "分割失敗",
        message: err.message
      });
      // 也可以加到 console 方便自己 debug
      console.error("Extension error:", err);
    });
  }
});
