"use strict"

function loadEvents(tag = "", date = "") {
  let url = 'http://127.0.0.1:5000/events'

  if (tag && tag !== "") {
    const encodedTag = encodeURIComponent(tag);
    url += `/tag/${encodedTag}`;
  } else if (date && date !== "") {
    const selectedDate = new Date(date);
    const day = selectedDate.getDate();
    const month = selectedDate.getMonth() + 1;
    const year = selectedDate.getFullYear();
    console.log(`Selected date: Year: ${year}, Month: ${month}, Day: ${day}`);
    url += `/date?day=${day}&month=${month}&year=${year}`
  }

  axios.get(url)
    .then(function (response) {
      const data = response.data;
      const row = document.querySelector('.container .row');
      row.innerHTML = '';

      data.forEach(function(item) {

        const col = document.createElement('div');
        col.className = 'col-lg-4 col-md-6 col-sm-12';

        const card = document.createElement('div');
        card.className = 'event_card';

        const imgDiv = document.createElement('div');
        imgDiv.className = 'event_card_img';
        const img = document.createElement('img');
        img.src = item.img;
        img.alt = 'event image';
        imgDiv.appendChild(img);

        const cardContent = document.createElement('div');
        cardContent.className = 'event_card_content';
        const title = document.createElement('h3');
        title.className = 'title';
        title.textContent = item.title;
        const description = document.createElement('p');
        description.className = 'description';
        description.textContent = item.description;
        cardContent.appendChild(title);
        cardContent.appendChild(description);

        const footer = document.createElement('div');
        footer.className = 'event_card_footer';
        const tag = document.createElement('p');
        tag.className = 'tag';
        tag.textContent = item.tag;
        const date = document.createElement('p');
        date.className = 'date';
        date.textContent = item.date;
        footer.appendChild(tag);
        footer.appendChild(date);

        card.appendChild(imgDiv)
        card.appendChild(cardContent)
        card.appendChild(footer)

        col.appendChild(card)
        row.appendChild(col)

      });
    })

    .catch(function (error) {
      console.error('Error fetching data:', error)
    })
}

document.getElementById('filterEvents').addEventListener('click', function() {
  const selectedTag = document.getElementById('tagSelect').value;
  const selectedDate = document.getElementById('dateInput').value;
  loadEvents(selectedTag, selectedDate);
})

loadEvents();