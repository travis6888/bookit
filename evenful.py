         # eventful_params = {
         #        'app_key': 'pXS5JztFCZDmbxbG',
         #        'category': str(interest.interests),
         #        'location': zipcode.city,
         #        'within': '10mi',
         #        'date': "{}-{}".format(eventful_start, eventful_end),
         #        'page_size': 2
         #    }
         #    eventful_resp = get(url=eventful_url, params=eventful_params)
         #    print eventful_resp.url
         #    eventful_data = json.loads(eventful_resp.text)
         #    eventful_list.append(eventful_data)
         #    for event in eventful_data['events']['event']:
         #        if event['image'] == None:
         #            picture = None
         #        else:
         #            picture=event['image']['url']
         #        Event.objects.create(
         #            name=event['title'],
         #            category=interest.interests,
         #            venue=event['venue_name'],
         #            description=event['description'],
         #            latitude=event['latitude'],
         #            longitude=event['longitude'],
         #            start_time=event['start_time'],
         #            end_time=event['stop_time'],
         #            picture=picture,
         #            event_url=event['url']
         #        )

        #
        #    eventful_start = start_time[:-10].translate(None, '-')
        # eventful_end = start_time[:-10].translate(None, '-')

        # eventful_url = 'http://api.eventful.com/json/events/search?'