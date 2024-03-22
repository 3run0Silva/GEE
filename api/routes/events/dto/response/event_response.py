def event_to_dto(event):
  return{
    'id': event.id,
    'img': event.get('img'),
    'title': event.get('title'),
    'date': event.get('date'),
    'day': event.get('day'),
    'month': event.get('month'),
    'year': event.get('year'),
    'description': event.get('description'),
    'tag': event.get('tag')
  }