(function () {
  function toggleActive(element, condition) {
    if (condition) {
      element.classList.add("active");
    } else {
      element.classList.remove("active");
    }
  }

  function switchTab(groupId, name) {
    const tabItems = document.querySelectorAll(
      `.tab-item[data-tab-group="${groupId}"]`
    );
    const tabButtons = document.querySelectorAll(
      `.tab-button[data-tab-group="${groupId}"]`
    );
    [...tabItems, ...tabButtons].forEach(
      (item) => toggleActive(item, item.dataset.tabItem === name)
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    const tabButtons = document.querySelectorAll(
      '.tab-button[data-tab-group]'
    );

    tabButtons.forEach(function (button) {
      button.addEventListener("click", function () {
        const groupId = button.dataset.tabGroup;
        const name = button.dataset.tabItem;

        if (!groupId || !name) {
          return;
        }

        switchTab(groupId, name);
      });
    });
  });
})();
