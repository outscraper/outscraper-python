Outscraper Python Library
=========================

The library provides convenient access to the `Outscraper
API <https://app.outscraper.com/api-docs>`__ from applications written
in the Python language. Allows using `Outscraper’s
services <https://outscraper.com/services/>`__ from your code.

`API Docs <https://app.outscraper.com/api-docs>`__

Installation
------------

Python 3+

.. code:: bash

   pip install outscraper

`Link to the python package
page <https://pypi.org/project/outscraper/>`__

Initialization
--------------

.. code:: python

   from outscraper import ApiClient

   client = ApiClient(api_key='SECRET_API_KEY')

`Link to the profile page to create the API
key <https://app.outscraper.com/profile>`__

Scrape Google Search
--------------------

.. code:: python

   # Googel Search
   results = client.google_search('bitcoin')

   # Googel Search News
   results = client.google_search_news('election', language='en')

Scrape Google Maps (Places)
---------------------------

.. code:: python

   # Search for businesses in specific locations:
   results = client.google_maps_search_v2('restaurants brooklyn usa', limit=20, language='en')

   # Get data of the specific place by id
   results = client.google_maps_search_v2('ChIJrc9T9fpYwokRdvjYRHT8nI4', language='en')

   # Search with many queries (batching)
   results = client.google_maps_search_v2([
       'restaurants brooklyn usa',
       'bars brooklyn usa',
   ], language='en')

Scrape Google Maps Reviews
--------------------------

.. code:: python

   # Get reviews of the specific place by id
   results = client.google_maps_reviews_v3('ChIJrc9T9fpYwokRdvjYRHT8nI4', reviews_limit=20, language='en')

   # Get reviews for places found by search query
   results = client.google_maps_reviews_v3('Memphis Seoul brooklyn usa', reviews_limit=20, limit=500, language='en')

   # Get only new reviews during last 24 hours
   from datetime import datetime, timedelta
   yesterday_timestamp = int((datetime.now() - timedelta(1)).timestamp())

   results = client.google_maps_reviews_v3(
       'ChIJrc9T9fpYwokRdvjYRHT8nI4', sort='newest', cutoff=yesterday_timestamp, reviews_limit=100, language='en')

Scrape Google Maps Photos
-------------------------

.. code:: python

   results = client.google_maps_photos(
       'Trump Tower, NY, USA', photosLimit=20, language='en')

Scrape Google Maps Directions
-----------------------------

.. code:: python

   results = client.google_maps_directions(['29.696596, 76.994928    30.7159662444353, 76.8053887016268', '29.696596, 76.994928    30.723065, 76.770169'])

Scrape Google Play Reviews
--------------------------

.. code:: python

   results = client.google_play_reviews(
       'com.facebook.katana', reviews_limit=20, language='en')

Emails And Contacts Scraper
---------------------------

.. code:: python

   results = client.emails_and_contacts(['outscraper.com'])

`More
examples <https://github.com/outscraper/outscraper-python/tree/master/examples>`__

Responses examples
------------------

Google Maps (Places) response example:

.. code:: json

   [
     [
       {
         "name": "Colonie",
         "full_address": "127 Atlantic Ave, Brooklyn, NY 11201",
         "borough": "Brooklyn Heights",
         "street": "127 Atlantic Ave",
         "city": "Brooklyn",
         "postal_code": "11201",
         "country_code": "US",
         "country": "United States of America",
         "us_state": "New York",
         "state": "New York",
         "plus_code": null,
         "latitude": 40.6908464,
         "longitude": -73.9958422,
         "time_zone": "America/New_York",
         "popular_times": null,
         "site": "http://www.colonienyc.com/",
         "phone": "+1 718-855-7500",
         "type": "American restaurant",
         "category": "restaurants",
         "subtypes": "American restaurant, Cocktail bar, Italian restaurant, Organic restaurant, Restaurant, Wine bar",
         "posts": null,
         "rating": 4.6,
         "reviews": 666,
         "reviews_data": null,
         "photos_count": 486,
         "google_id": "0x89c25a4590b8c863:0xc4a4271f166de1e2",
         "place_id": "ChIJY8i4kEVawokR4uFtFh8npMQ",
         "reviews_link": "https://search.google.com/local/reviews?placeid=ChIJY8i4kEVawokR4uFtFh8npMQ&q=restaurants+brooklyn+usa&authuser=0&hl=en&gl=US",
         "reviews_id": "-4277250731621359134",
         "photo": "https://lh5.googleusercontent.com/p/AF1QipN_Ani32z-7b9XD182oeXKgQ-DIhLcgL09gyMZf=w800-h500-k-no",
         "street_view": "https://lh5.googleusercontent.com/p/AF1QipN_Ani32z-7b9XD182oeXKgQ-DIhLcgL09gyMZf=w1600-h1000-k-no",
         "working_hours_old_format": "Monday: 5\\u20139:30PM | Tuesday: Closed | Wednesday: Closed | Thursday: 5\\u20139:30PM | Friday: 5\\u20139:30PM | Saturday: 11AM\\u20133PM,5\\u20139:30PM | Sunday: 11AM\\u20133PM,5\\u20139:30PM",
         "working_hours": {
           "Monday": "5\\u20139:30PM",
           "Tuesday": "Closed",
           "Wednesday": "Closed",
           "Thursday": "5\\u20139:30PM",
           "Friday": "5\\u20139:30PM",
           "Saturday": "11AM\\u20133PM,5\\u20139:30PM",
           "Sunday": "11AM\\u20133PM,5\\u20139:30PM"
         },
         "business_status": "OPERATIONAL",
         "about": {
           "Service options": {
             "Dine-in": true,
             "Delivery": false,
             "Takeout": false
           },
           "Health & safety": {
             "Mask required": true,
             "Staff required to disinfect surfaces between visits": true
           },
           "Highlights": {
             "Fast service": true,
             "Great cocktails": true,
             "Great coffee": true
           },
           "Popular for": {
             "Lunch": true,
             "Dinner": true,
             "Solo dining": true
           },
           "Accessibility": {
             "Wheelchair accessible entrance": true,
             "Wheelchair accessible restroom": true,
             "Wheelchair accessible seating": true
           },
           "Offerings": {
             "Coffee": true,
             "Comfort food": true,
             "Healthy options": true,
             "Organic dishes": true,
             "Small plates": true,
             "Vegetarian options": true,
             "Wine": true
           },
           "Dining options": {
             "Dessert": true
           },
           "Amenities": {
             "High chairs": true
           },
           "Atmosphere": {
             "Casual": true,
             "Cozy": true,
             "Romantic": true,
             "Upscale": true
           },
           "Crowd": {
             "Groups": true
           },
           "Planning": {
             "Dinner reservations recommended": true,
             "Accepts reservations": true,
             "Usually a wait": true
           },
           "Payments": {
             "Credit cards": true
           }
         },
         "range": "$$$",
         "reviews_per_score": {
           "1": 9,
           "2": 10,
           "3": 47,
           "4": 129,
           "5": 471
         },
         "reserving_table_link": "https://resy.com/cities/ny/colonie",
         "booking_appointment_link": "https://resy.com/cities/ny/colonie",
         "owner_id": "114275131377272904229",
         "verified": true,
         "owner_title": "Colonie",
         "owner_link": "https://www.google.com/maps/contrib/114275131377272904229",
         "location_link": "https://www.google.com/maps/place/Colonie/@40.6908464,-73.9958422,14z/data=!4m8!1m2!2m1!1sColonie!3m4!1s0x89c25a4590b8c863:0xc4a4271f166de1e2!8m2!3d40.6908464!4d-73.9958422"
       },
       ...
     ]
   ]

Google Maps Reviews response example:

.. code:: json

   {
     "name": "Memphis Seoul",
     "address": "569 Lincoln Pl, Brooklyn, NY 11238, \\u0421\\u043f\\u043e\\u043b\\u0443\\u0447\\u0435\\u043d\\u0456 \\u0428\\u0442\\u0430\\u0442\\u0438",
     "address_street": "569 Lincoln Pl",
     "address_borough": "\\u041a\\u0440\\u0430\\u0443\\u043d-\\u0413\\u0430\\u0439\\u0442\\u0441",
     "address_city": "Brooklyn",
     "time_zone": "America/New_York",
     "type": "\\u0420\\u0435\\u0441\\u0442\\u043e\\u0440\\u0430\\u043d",
     "types": "\\u0420\\u0435\\u0441\\u0442\\u043e\\u0440\\u0430\\u043d",
     "postal_code": "11238",
     "latitude": 40.6717258,
     "longitude": -73.9579098,
     "phone": "+1 347-349-2561",
     "rating": 3.9,
     "reviews": 32,
     "site": "http://www.getmemphisseoul.com/",
     "photos_count": 77,
     "google_id": "0x89c25bb5950fc305:0x330a88bf1482581d",
     "reviews_link": "https://www.google.com/search?q=Memphis+Seoul,+569+Lincoln+Pl,+Brooklyn,+NY+11238,+%D0%A1%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D1%96+%D0%A8%D1%82%D0%B0%D1%82%D0%B8&ludocid=3677902399965648925#lrd=0x89c25bb5950fc305:0x330a88bf1482581d,1",
     "reviews_id": "3677902399965648925",
     "photo": "https://lh5.googleusercontent.com/p/X_6-QqMphC_ctqs3bHSqFg",
     "working_hours": "\\u0432\\u0456\\u0432\\u0442\\u043e\\u0440\\u043e\\u043a: 16:00\\u201322:00 | \\u0441\\u0435\\u0440\\u0435\\u0434\\u0430: 16:00\\u201322:00 | \\u0447\\u0435\\u0442\\u0432\\u0435\\u0440: 16:00\\u201322:00 | \\u043f\\u02bc\\u044f\\u0442\\u043d\\u0438\\u0446\\u044f: 16:00\\u201322:00 | \\u0441\\u0443\\u0431\\u043e\\u0442\\u0430: 16:00\\u201322:00 | \\u043d\\u0435\\u0434\\u0456\\u043b\\u044f: 16:00\\u201322:00 | \\u043f\\u043e\\u043d\\u0435\\u0434\\u0456\\u043b\\u043e\\u043a: 16:00\\u201322:00",
     "reviews_per_score": "1: 6, 2: 0, 3: 4, 4: 3, 5: 19",
     "verified": true,
     "reserving_table_link": null,
     "booking_appointment_link": null,
     "owner_id": "100347822687163365487",
     "owner_link": "https://www.google.com/maps/contrib/100347822687163365487",
     "reviews_data": [
       {
         "google_id": "0x89c25bb5950fc305:0x330a88bf1482581d",
         "autor_link": "https://www.google.com/maps/contrib/112314095435657473333?hl=en-US",
         "autor_name": "Eliott Levy",
         "autor_id": "112314095435657473333",
         "review_text": "Very good local comfort fusion food ! \\nKimchi coleslaw !! Such an amazing idea !",
         "review_link": "https://www.google.com/maps/reviews/data=!4m5!14m4!1m3!1m2!1s112314095435657473333!2s0x0:0x330a88bf1482581d?hl=en-US",
         "review_rating": 5,
         "review_timestamp": 1560692128,
         "review_datetime_utc": "06/16/2019 13:35:28",
         "review_likes": null
       },
       {
         "google_id": "0x89c25bb5950fc305:0x330a88bf1482581d",
         "autor_link": "https://www.google.com/maps/contrib/106144075337788507031?hl=en-US",
         "autor_name": "fenwar1",
         "autor_id": "106144075337788507031",
         "review_text": "Great wings with several kinds of hot sauce. The mac and cheese ramen is excellent.\\nUPDATE:\\nReturned later to try the meatloaf slider, a thick meaty slice  topped with slaw and a fantastic sauce- delicious. \\nConsider me a regular.\\ud83d\\udc4d",
         "review_link": "https://www.google.com/maps/reviews/data=!4m5!14m4!1m3!1m2!1s106144075337788507031!2s0x0:0x330a88bf1482581d?hl=en-US",
         "review_rating": 5,
         "review_timestamp": 1571100055,
         "review_datetime_utc": "10/15/2019 00:40:55",
         "review_likes": null
       },
       ...
     ]
   }

Google Play Reviews response example:

.. code:: json

   [
     [
       {
         "autor_name": "candice petrancosta",
         "autor_id": "113798143822975084287",
         "autor_image": "https://play-lh.googleusercontent.com/a-/AOh14GiBRe-07Fmx8MyyVyrZP6TkSGenrs97e1_MG7Z-sWA",
         "review_text": "I love FB but the app has been pissing me off lately. It keeps having problems. Now my public page for my business is not letting me see my notifications and it is very annoying. Also, it keeps saying that I have a message when I don\'t. That\'s been a probably for a very long time that comes and goes. I hate seeing the icon showing me that I have a message when I do not \\ud83d\\ude21",
         "review_rating": 1,
         "review_likes": 964,
         "version": "328.1.0.28.119",
         "review_timestamp": 1627360161,
         "review_datetime_utc": "07/27/2021 04:29:21",
         "owner_answer": null,
         "owner_answer_timestamp": null,
         "owner_answer_timestamp_datetime_utc": null
       },
       {
         "autor_name": "Deren Nickerson",
         "autor_id": "117741211939002621733",
         "autor_image": "https://play-lh.googleusercontent.com/a/AATXAJwIXPpnodqFFvB9oQEsk8XYFqtkEcfDEmNr704=mo",
         "review_text": "Technical support is non-existent whatsoever. Currently hiding behind the guise of a lack of reviewers being able to sit and stare at a computer screen due to a pandemic that forces people to stay at and work from home. Using auto-bots to destroy people\'s only methods of communicating with the outside world. I bet Facebook literally has blood on their hands from all the people who have killed themselves due to having their accounts needlessly disabled for months. Also you can\'t remove the app..",
         "review_rating": 1,
         "review_likes": 225,
         "version": "328.1.0.28.119",
         "review_timestamp": 1627304448,
         "review_datetime_utc": "07/26/2021 13:00:48",
         "owner_answer": null,
         "owner_answer_timestamp": null,
         "owner_answer_timestamp_datetime_utc": null
       },
       {
         "autor_name": "Tj Symula",
         "autor_id": "103540836420891624440",
         "autor_image": "https://play-lh.googleusercontent.com/a/AATXAJxW4-DAYNCAgj2OQ41lQadAQtBxX4G_Aqn-Urvc=mo",
         "review_text": "I have been logged into facebook for as long as I can remember, but I\'ve been booted somehow. I\'ve sent several emails with no response. All of my logins for multiple sites, I\'ve used the \\"login with facebook\\" option. I have no way to retrieve emails and passwords that I changed years ago, please help me fix this issue, its hindering my ability to use many online features on my phone.",
         "review_rating": 1,
         "review_likes": 181,
         "version": "328.1.0.28.119",
         "review_timestamp": 1627307359,
         "review_datetime_utc": "07/26/2021 13:49:19",
         "owner_answer": null,
         "owner_answer_timestamp": null,
         "owner_answer_timestamp_datetime_utc": null
       },
       ...
     ]
   ]

Emails & Contacts Scraper response example:

.. code:: json

   [
       {
         "query": "outscraper.com",
         "domain": "outscraper.com",
         "emails": [
           {
             "value": "service@outscraper.com",
             "sources": [
               {
                 "ref": "https://outscraper.com/",
                 "extracted_on": "2021-09-27T07:45:30.386000",
                 "updated_on": "2021-11-18T12:59:15.602000"
               },
             ...
             ]
           },
           {
             "value": "support@outscraper.com",
             "sources": [
               {
                 "ref": "https://outscraper.com/privacy-policy/",
                 "extracted_on": "2021-11-18T12:51:39.716000",
                 "updated_on": "2021-11-18T12:51:39.716000"
               }
             ]
           }
         ],
         "phones": [
           {
             "value": "12812368208",
             "sources": [
               {
                 "ref": "https://outscraper.com/",
                 "extracted_on": "2021-11-18T12:59:15.602000",
                 "updated_on": "2021-11-18T12:59:15.602000"
               },
               ...
             ]
           }
         ],
         "socials": {
           "facebook": "https://www.facebook.com/outscraper/",
           "github": "https://github.com/outscraper",
           "linkedin": "https://www.linkedin.com/company/outscraper/",
           "twitter": "https://twitter.com/outscraper",
           "whatsapp": "https://wa.me/12812368208",
           "youtube": "https://www.youtube.com/channel/UCDYOuXSEenLpt5tKNq-0l9Q"
         },
         "site_data": {
           "description": "Scrape Google Maps Places, Business Reviews, Photos, Play Market Reviews, and more. Get any public data from the internet by applying cutting-edge technologies.",
           "generator": "WordPress 5.8.2",
           "title": "Outscraper - get any public data from the internet"
         }
       }
     ]

Contributing
------------

Bug reports and pull requests are welcome on GitHub at
https://github.com/outscraper/outscraper-python.
