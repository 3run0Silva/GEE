"use strict"
axios.get('http://127.0.0.1:5000/events')
  .then(function (response) {
    const data = response.data;
    const row = document.querySelector('.container .row');

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
      footer.appendChild(tag);

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