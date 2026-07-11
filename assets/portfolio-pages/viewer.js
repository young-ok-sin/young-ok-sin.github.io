const pages = [...document.querySelectorAll('.portfolio-page')];
const list = document.querySelector('#page-list');
const current = document.querySelector('#current-page');

pages.forEach((page, index) => {
  const number = index + 1;
  const item = document.createElement('li');
  const imageSource = page.querySelector('img').src;
  item.innerHTML = `<a href="#page-${number}" data-link-page="${number}" aria-label="${number}페이지로 이동"><img src="${imageSource}" alt="" width="1440" height="810" loading="lazy"><span>${number} 페이지</span></a>`;
  list.append(item);
});

const links = [...document.querySelectorAll('[data-link-page]')];
function setCurrent(number) {
  current.textContent = number;
  links.forEach((link) => link.classList.toggle('active', link.dataset.linkPage === number));
}

const observer = new IntersectionObserver((entries) => {
  const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
  if (visible) setCurrent(visible.target.dataset.page);
}, { rootMargin: '-20% 0px -60%', threshold: [0, .25, .5] });

pages.forEach((page) => observer.observe(page));
setCurrent('1');
