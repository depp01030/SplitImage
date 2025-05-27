chrome.runtime.onInstalled.addListener(() => {
  // 右鍵選單：針對naver
  chrome.contextMenus.create({
    id: "send-all-image-urls",
    title: "送出Naver所有圖片網址",
    contexts: ["page"]
  });
  // 右鍵選單：針對圖片
  chrome.contextMenus.create({
    id: "split-image-api",
    title: "送到本地分割 API",
    contexts: ["image"]
  });
  // 右鍵選單：針對頁面
  chrome.contextMenus.create({
    id: "split-page-url-api",
    title: "送出minute整頁圖片",
    contexts: ["page"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "send-all-image-urls") {
    chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => {
        // 🧩 專門抓取最大 .se-main-container 區塊裡的圖片網址
        function extractImageUrlsFromLargestSeMainContainer() {
          const containers = [...document.querySelectorAll(".se-main-container")];
          let target = null;

          if (containers.length > 0) {
            target = containers.reduce((a, b) =>
              b.querySelectorAll("img").length > a.querySelectorAll("img").length ? b : a
            );
          } else {
            target = document;
          }

          const added = new Set();
          const imageUrls = [];

          // 抓 <img>
          target.querySelectorAll("img").forEach((img) => {
            const lazySrc = img.dataset.src || img.dataset.lazySrc;
            if (lazySrc && !img.src.startsWith("http")) img.src = lazySrc;

            const src = img.src;
            if (!src || src.startsWith("data:image/") || added.has(src)) return;

            imageUrls.push(src);
            added.add(src);

            // 檢查所有 data-* 屬性中可能的圖片路徑
            for (const attr in img.dataset) {
              const val = img.dataset[attr];
              if (
                typeof val === "string" &&
                (attr.includes("src") || attr.includes("img") || attr.includes("image")) &&
                val.startsWith("http") &&
                !added.has(val)
              ) {
                imageUrls.push(val);
                added.add(val);
              }
            }
          });

          // 抓背景圖
          target.querySelectorAll("*").forEach((el) => {
            const bg = getComputedStyle(el).backgroundImage;
            if (bg && bg.startsWith("url(")) {
              const url = bg.slice(4, -1).replace(/^"(.*)"$/, "$1");
              if (url && !added.has(url) && url.startsWith("http")) {
                imageUrls.push(url);
                added.add(url);
              }
            }
          });

          // 最終清洗路徑
          const cleanUrls = [...new Set(imageUrls)]
            .filter(url =>
              url &&
              typeof url === "string" &&
              url.startsWith("http") &&
              !url.includes("icon") &&
              !url.includes("button") &&
              !url.includes("logo")
            )
            .map(url => url.replace(/_\d+x\d+\./, '.').replace(/\?.*$/, ''));

          return cleanUrls;
        }

        return extractImageUrlsFromLargestSeMainContainer();
      }
    }).then(results => {
      const imgUrls = results[0].result;
      const pageUrl = tab.url; // ⬅️ 這裡就是頁面 URL
      console.log("抓到的圖片網址:", imgUrls);
      console.log("頁面網址：", pageUrl);

      // 傳送到後端 FastAPI
      fetch("http://localhost:8888/download_naver/image_list", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          image_urls: imgUrls,
          page_url: pageUrl     // ✅ 傳送頁面網址
        })
      })
      .then(res => res.json())
      .then(data => {
        chrome.notifications.create({
          type: "basic",
          iconUrl: chrome.runtime.getURL("icon.png"),
          title: "圖片網址傳送成功",
          message: `共送出 ${imgUrls.length} 張圖片`
        });
      })
      .catch(err => {
        chrome.notifications.create({
          type: "basic",
          iconUrl: chrome.runtime.getURL("icon.png"),
          title: "傳送失敗",
          message: err.message
        });
        console.error("❌ 發送圖片網址失敗：", err);
      });
    });
  }
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
