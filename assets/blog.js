(() => {
  const search = document.getElementById('journal-search');
  if (!search) return;
  const cards = [...document.querySelectorAll('#journal-grid .journal-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  let category = 'All';
  const update = () => {
    const query = search.value.trim().toLowerCase();
    let count = 0;
    for (const card of cards) {
      const visible = (category === 'All' || card.dataset.category === category) && card.dataset.search.includes(query);
      card.hidden = !visible;
      if (visible) count++;
    }
    document.querySelector('.journal-count').textContent = `${count} ${count === 1 ? 'guide' : 'guides'} to explore`;
    document.getElementById('journal-empty').hidden = count !== 0;
  };
  search.addEventListener('input', update);
  for (const button of filters) button.addEventListener('click', () => {
    category = button.dataset.filter;
    for (const filter of filters) filter.setAttribute('aria-pressed', String(filter === button));
    update();
  });
})();
