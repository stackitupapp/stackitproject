document.addEventListener('DOMContentLoaded', function () {
	var modeSwitch = document.querySelector('.mode-switch');
	modeSwitch.addEventListener('click', function () { document.documentElement.classList.toggle('dark');
	modeSwitch.classList.toggle('active');
	});
	var listView = document.querySelector('.list-view');
	var gridView = document.querySelector('.grid-view');
	var projectsList = document.querySelector('.project-boxes');
	listView.addEventListener('click', function () {
	gridView.classList.remove('active');
	listView.classList.add('active');
	projectsList.classList.remove('jsGridView');
	projectsList.classList.add('jsListView');
	});
	gridView.addEventListener('click', function () {
	gridView.classList.add('active');
	listView.classList.remove('active');
	projectsList.classList.remove('jsListView');
	projectsList.classList.add('jsGridView');
	});
	document.querySelector('.messages-btn').addEventListener('click', function () {
	document.querySelector('.messages-section').classList.add('show');
	});
	document.querySelector('.messages-close').addEventListener('click', function() {
	document.querySelector('.messages-section').classList.remove('show');
	});
	});

	document.addEventListener("DOMContentLoaded", function () {
    const boxes = document.querySelectorAll(".project-box-wrapper");
    const pageBtns = document.querySelectorAll(".page-btn");
    const perPage = 1; // number of boxes per page
    let currentPage = 1;

    function showPage(page) {
      const start = (page - 1) * perPage;
      const end = start + perPage;

      boxes.forEach((box, index) => {
        box.style.display = (index >= start && index < end) ? "block" : "none";
      });

      pageBtns.forEach(btn => btn.classList.remove("active"));
      pageBtns.forEach(btn => {
        if (btn.dataset.page == page) btn.classList.add("active");
      });

      currentPage = page;
    }

    pageBtns.forEach(button => {
      button.addEventListener("click", () => {
        const value = button.dataset.page;

        if (value === "prev") {
          if (currentPage > 1) showPage(currentPage - 1);
        } else if (value === "next") {
          if (currentPage < Math.ceil(boxes.length / perPage)) {
            showPage(currentPage + 1);
          }
        } else {
          showPage(parseInt(value));
        }
      });
    });

    showPage(currentPage);
  });