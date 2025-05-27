// 解除右鍵限制的程式
console.log("解除右鍵限制腳本已載入");

// 解除右鍵菜單限制
document.addEventListener(
  "contextmenu",
  function (e) {
    e.stopPropagation();
    e.stopImmediatePropagation();
    return true;
  },
  true
);

// 禁用可能會阻止右鍵的事件監聽器
document.addEventListener("mousedown", function(e) {
  if(e.button === 2) {
    e.stopPropagation();
    return true;
  }
}, true);

// 解除選取限制
document.addEventListener("selectstart", function(e) {
  e.stopPropagation();
  return true;
}, true);

// 解除複製限制
document.addEventListener("copy", function(e) {
  e.stopPropagation();
  return true;
}, true);

// 移除頁面上的事件限制 (特別是針對圖片元素)
setTimeout(function() {
  const images = document.querySelectorAll('img');
  images.forEach(img => {
    img.oncontextmenu = null;
    img.ondragstart = null;
    img.onselectstart = null;
    img.style.setProperty('-webkit-user-select', 'auto', 'important');
    img.style.setProperty('user-select', 'auto', 'important');
    img.style.setProperty('-webkit-user-drag', 'auto', 'important');
  });
}, 1000);
