# Google Maps scraper in Python
Python SDK that allows scraping Google Maps, Google Reviews, Google Play Reviews via [OutScraper API](https://outscraper.com):

- Google Maps (Places) scraper
- Google Maps Reviews scraper
- Google Play Reviews scraper

## Installation

Python 3+
```bash
pip install google-services-api
```

[Link to the python package page](https://pypi.org/project/google-services-api/)

## Scrape Google Maps (Places)

```python
from outscraper import ApiClient

api_cliet = ApiClient(api_key='SECRET_API_KEY')
result = api_cliet.google_maps_search(
    'restaurants brooklyn usa', limit=20, language='en')
```

response:
```json
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
    {
      "name": "Oxalis",
      "full_address": "791 Washington Ave, Brooklyn, NY 11238",
      "borough": "Crown Heights",
      "street": "791 Washington Ave",
      "city": "Brooklyn",
      "postal_code": "11238",
      "country_code": "US",
      "country": "United States of America",
      "us_state": "New York",
      "state": "New York",
      "plus_code": null,
      "latitude": 40.672908299999996,
      "longitude": -73.9626279,
      "time_zone": "America/New_York",
      "popular_times": null,
      "site": "http://www.oxalisnyc.com/",
      "phone": "+1 347-627-8298",
      "type": "New American restaurant",
      "category": "New American restaurant",
      "subtypes": "New American restaurant",
      "posts": null,
      "rating": 4.8,
      "reviews": 260,
      "reviews_data": null,
      "photos_count": 580,
      "google_id": "0x89c25b2d40a27e33:0x166305f2914a4970",
      "place_id": "ChIJM36iQC1bwokRcElKkfIFYxY",
      "reviews_link": "https://search.google.com/local/reviews?placeid=ChIJM36iQC1bwokRcElKkfIFYxY&q=restaurants+brooklyn+usa&authuser=0&hl=en&gl=US",
      "reviews_id": "1613139630906558832",
      "photo": "https://lh5.googleusercontent.com/p/AF1QipPWBq9TAIGmK7_sLt_Ciwno9EJ8tTDZwrh9_9Nx=w800-h500-k-no",
      "street_view": "https://lh5.googleusercontent.com/p/AF1QipPWBq9TAIGmK7_sLt_Ciwno9EJ8tTDZwrh9_9Nx=w1600-h1000-k-no",
      "working_hours_old_format": "Monday: Closed | Tuesday: Closed | Wednesday: 5:30\\u201310PM | Thursday: 5:30\\u201310PM | Friday: 5:30\\u201310PM | Saturday: 5:30\\u201310PM | Sunday: 11AM\\u20132PM,5:30\\u201310PM",
      "working_hours": {
        "Monday": "Closed",
        "Tuesday": "Closed",
        "Wednesday": "5:30\\u201310PM",
        "Thursday": "5:30\\u201310PM",
        "Friday": "5:30\\u201310PM",
        "Saturday": "5:30\\u201310PM",
        "Sunday": "11AM\\u20132PM,5:30\\u201310PM"
      },
      "business_status": "OPERATIONAL",
      "about": {
        "Service options": {
          "Curbside pickup": true,
          "No-contact delivery": true,
          "Delivery": true,
          "Takeout": true,
          "Dine-in": true
        },
        "Health & safety": {
          "Mask required": true,
          "Staff required to disinfect surfaces between visits": true
        },
        "Popular for": {
          "Dinner": true,
          "Solo dining": true
        },
        "Offerings": {
          "Coffee": true
        },
        "Dining options": {
          "Dessert": true
        },
        "Atmosphere": {
          "Cozy": true,
          "Romantic": true
        },
        "Planning": {
          "Dinner reservations recommended": true,
          "Accepts reservations": true
        },
        "Payments": {
          "NFC mobile payments": true
        }
      },
      "range": "$$$",
      "reviews_per_score": {
        "1": 3,
        "2": 2,
        "3": 9,
        "4": 26,
        "5": 220
      },
      "reserving_table_link": "http://www.oxalisnyc.com/#reservations",
      "booking_appointment_link": "http://www.oxalisnyc.com/#reservations",
      "owner_id": "107813995682676897500",
      "verified": true,
      "owner_title": "Oxalis",
      "owner_link": "https://www.google.com/maps/contrib/107813995682676897500",
      "location_link": "https://www.google.com/maps/place/Oxalis/@40.672908299999996,-73.9626279,14z/data=!4m8!1m2!2m1!1sOxalis!3m4!1s0x89c25b2d40a27e33:0x166305f2914a4970!8m2!3d40.672908299999996!4d-73.9626279"
    },
    {
      "name": "Cremini\'s",
      "full_address": "521 Court St, Brooklyn, NY 11231",
      "borough": "Carroll Gardens",
      "street": "521 Court St",
      "city": "Brooklyn",
      "postal_code": "11231",
      "country_code": "US",
      "country": "United States of America",
      "us_state": "New York",
      "state": "New York",
      "plus_code": null,
      "latitude": 40.6749596,
      "longitude": -73.9992896,
      "time_zone": "America/New_York",
      "popular_times": null,
      "site": "http://www.creminis.com/",
      "phone": "+1 929-305-2967",
      "type": "Italian restaurant",
      "category": "restaurants",
      "subtypes": "Italian restaurant",
      "posts": null,
      "rating": 4.9,
      "reviews": 149,
      "reviews_data": null,
      "photos_count": 404,
      "google_id": "0x89c25ba11c76be73:0x58dedcecf3822000",
      "place_id": "ChIJc752HKFbwokRACCC8-zc3lg",
      "reviews_link": "https://search.google.com/local/reviews?placeid=ChIJc752HKFbwokRACCC8-zc3lg&q=restaurants+brooklyn+usa&authuser=0&hl=en&gl=US",
      "reviews_id": "6403798630423207936",
      "photo": "https://lh5.googleusercontent.com/p/AF1QipM7t-JT05S79Ozj7HmOnw6OvsnmsPQdTXBhPl4d=w800-h500-k-no",
      "street_view": "https://lh5.googleusercontent.com/p/AF1QipM7t-JT05S79Ozj7HmOnw6OvsnmsPQdTXBhPl4d=w1600-h1000-k-no",
      "working_hours_old_format": "Monday: 4\\u201310PM | Tuesday: 4\\u201310PM | Wednesday: Closed | Thursday: Closed | Friday: Closed | Saturday: Closed | Sunday: Closed",
      "working_hours": {
        "Monday": "4\\u201310PM",
        "Tuesday": "4\\u201310PM",
        "Wednesday": "Closed",
        "Thursday": "Closed",
        "Friday": "Closed",
        "Saturday": "Closed",
        "Sunday": "Closed"
      },
      "business_status": "OPERATIONAL",
      "about": {
        "From the business": {
          "Identifies as women-led": true
        },
        "Service options": {
          "Outdoor seating": true,
          "No-contact delivery": true,
          "Delivery": true,
          "Takeout": true,
          "Dine-in": true
        },
        "Health & safety": {
          "Mask required": true,
          "Temperature check required": true,
          "Staff wear masks": true,
          "Staff get temperature checks": true,
          "Staff required to disinfect surfaces between visits": true
        },
        "Highlights": {
          "LGBTQ friendly": true,
          "Live music": true,
          "Transgender safespace": true
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
          "Alcohol": true,
          "Beer": true,
          "Cocktails": true,
          "Coffee": true,
          "Comfort food": true,
          "Happy hour drinks": true,
          "Happy hour food": true,
          "Late-night food": true,
          "Organic dishes": true,
          "Quick bite": true,
          "Salad bar": true,
          "Small plates": true,
          "Vegetarian options": true,
          "Wine": true
        },
        "Dining options": {
          "Breakfast": true,
          "Lunch": true,
          "Dinner": true,
          "Catering": true,
          "Dessert": true,
          "Seating": true
        },
        "Amenities": {
          "Bar onsite": true,
          "Good for kids": true,
          "Restroom": true,
          "Wi-Fi": true
        },
        "Atmosphere": {
          "Casual": true,
          "Cozy": true
        },
        "Crowd": {
          "Groups": true,
          "Tourists": true
        },
        "Planning": {
          "Accepts reservations": true
        },
        "Payments": {
          "Debit cards": true,
          "NFC mobile payments": true,
          "Credit cards": true
        }
      },
      "range": null,
      "reviews_per_score": {
        "1": 0,
        "2": 0,
        "3": 3,
        "4": 5,
        "5": 141
      },
      "reserving_table_link": "https://tableagent.com/new-york-city/creminis/",
      "booking_appointment_link": "https://tableagent.com/new-york-city/creminis/",
      "owner_id": "116143296438311936930",
      "verified": true,
      "owner_title": "Cremini\'s",
      "owner_link": "https://www.google.com/maps/contrib/116143296438311936930",
      "location_link": "https://www.google.com/maps/place/Cremini%27s/@40.6749596,-73.9992896,14z/data=!4m8!1m2!2m1!1sCremini%27s!3m4!1s0x89c25ba11c76be73:0x58dedcecf3822000!8m2!3d40.6749596!4d-73.9992896"
    }
  ]
]
```

## Scrape Google Places Reviews

```python
from outscraper import ApiClient

api_cliet = ApiClient(api_key='SECRET_API_KEY')
result = api_cliet.google_maps_reviews(
    'Memphis Seoul brooklyn usa', reviewsLimit=20, language='en')
```

response:
```json
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
```

## Scrape Google Play Reviews

```python
from outscraper import ApiClient

api_cliet = ApiClient(api_key='SECRET_API_KEY')
result = api_cliet.google_play_reviews(
    'com.facebook.katana', reviewsLimit=20, language='en')
```

response:
```json
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
```