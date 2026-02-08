(function () {
  function toggleActive(element, condition) {
    if (condition) {
      element.classList.add("active");
    } else {
      element.classList.remove("active");
    }
  }

  function switchTabInternal(groupId, name, focusTab) {
    const tabItems = document.querySelectorAll(
      `.tab-item[data-tab-group="${groupId}"]`
    );
    const tabButtons = document.querySelectorAll(
      `.tab-button[data-tab-group="${groupId}"]`
    );
    
    tabButtons.forEach((button) => {
      const isSelected = button.dataset.tabItem === name;
      toggleActive(button, isSelected);
      button.setAttribute('aria-selected', isSelected ? 'true' : 'false');
      button.setAttribute('tabindex', isSelected ? '0' : '-1');
      
      if (isSelected && focusTab) {
        button.focus();
      }
    });
    
    tabItems.forEach((item) => {
      const isActive = item.dataset.tabItem === name;
      toggleActive(item, isActive);
      
      if (isActive) {
        item.removeAttribute('hidden');
      } else {
        item.setAttribute('hidden', '');
      }
    });
  }

  function handleKeyboardNavigation(event, groupId) {
    const tabButtons = Array.from(
      document.querySelectorAll(`.tab-button[data-tab-group="${groupId}"]`)
    );
    const currentIndex = tabButtons.findIndex((btn) => btn === event.target);
    
    let nextIndex = -1;
    
    switch (event.key) {
      case 'ArrowLeft':
      case 'ArrowUp':
        event.preventDefault();
        nextIndex = currentIndex > 0 ? currentIndex - 1 : tabButtons.length - 1;
        break;
      case 'ArrowRight':
      case 'ArrowDown':
        event.preventDefault();
        nextIndex = currentIndex < tabButtons.length - 1 ? currentIndex + 1 : 0;
        break;
      case 'Home':
        event.preventDefault();
        nextIndex = 0;
        break;
      case 'End':
        event.preventDefault();
        nextIndex = tabButtons.length - 1;
        break;
      default:
        return;
    }
    
    if (nextIndex !== -1) {
      const nextButton = tabButtons[nextIndex];
      switchTabInternal(groupId, nextButton.dataset.tabItem, true);
    }
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

        switchTabInternal(groupId, name, false);
      });
      
      button.addEventListener("keydown", function (event) {
        const groupId = button.dataset.tabGroup;
        
        if (!groupId) {
          return;
        }
        
        handleKeyboardNavigation(event, groupId);
      });
    });
  });
  
  /**
   * Global function to switch tabs programmatically.
   * Exposed for compatibility with inline onclick handlers in the template.
   * @param {string} groupId - The ID of the tab group
   * @param {string} name - The name of the tab to switch to
   */
  window.switchTab = function(groupId, name) {
    switchTabInternal(groupId, name, false);
  };
})();
