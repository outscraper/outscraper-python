Google services API in Python
=============================

Python sdk that allows extracting data from Google services via
`OutScraper API <http://outscraper.com>`__.

Installation
------------

Python 3+

.. code:: bash

    pip install google-services-api

`Link to the python package
page <https://pypi.org/project/google-services-api/>`__

Quick start
-----------

.. code:: python

    from outscraper import ApiClient
    api_cliet = ApiClient(api_key='SECRET_API_KEY')
    maps_result = api_cliet.google_maps_search('restaurants brooklyn usa')
    search_result = api_cliet.google_search('bitcoin')

Get business reviews
--------------------

.. code:: python

    from outscraper import ApiClient
    api_cliet = ApiClient(api_key='SECRET_API_KEY')
    business_with_reviews = api_cliet.google_maps_business_reviews(
        'Memphis Seoul brooklyn usa', limit=100, language='en')

response:

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

