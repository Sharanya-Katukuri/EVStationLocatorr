fetch(API_BASE + "stations/")
.then(res => res.json())
.then(data => {
  data.forEach(s => {
    list.innerHTML += `
      <li>
        ${s.name} - ${s.city}
        <a href="station-detail.html?id=${s.id}">View</a>
      </li>`;
  });
});
