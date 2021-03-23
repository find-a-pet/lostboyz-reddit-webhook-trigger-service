# Reddit Webhook Trigger Service

## Usage

All responses `(i.e. payloads to the consumer of this service)` will have the form

````json
{
  "data": "Mixed type holding the content of the response",
  "message": "Description of what happened"
}
````

Subsequent response definitions will only detail the expected value of the `data field`

**Definitions**

### Return all new lost pets

The service scheduled to run at predetermined intervals. Polls a subreddit(s) for new submissions meeting a criteria. Data from Reddit is `POST`***ed*** to an endpoint on the lostboyz-reddit-webhook-service. And the latter service responds with the sample payload below

`POST /pets`

**Response**
- `200 OK` on success

Note that "Submission" refers to a Reddit post

````json
[
  {
    "id": "jud5sm",
    "locked": false,
    "is_self": false,
    "post_hint": "image",
    "submission_name": "t3_jud5sm",
    "link_flair_text": "Lost & Found",
    "submission_author_name": "Omerbaturay",
    "url": "https://i.redd.it/qyzkvpl60bz51.jpg",
    "title": "Found wondering dog in Langford area",
		"preview": {
        "enabled ": true,
        "images ":
        [
            {
                "id ": "KjU7Wmv3IcF7UT5uN8PSwHLFMNoy0EniH_XGeNPdCSA",
                "resolutions ":
                [
                    {
                        "height ": 192,
                        "url ": "https://preview.redd.it/qyzkvpl60bz51.jpg?width=108&crop=smart&auto=webp&s=601d30174c409d7426c09fb8f0f22502c6dea80b",
                        "width ": 108
                    },
                    {
                        "height ": 384,
                        "url ": "https://preview.redd.it/qyzkvpl60bz51.jpg?width=216&crop=smart&auto=webp&s=415894ab5ae964f12e2ef268bd2032102af3e4f7 ",
                        "width ": 216
                    },
                    {
                        "height ": 568,
                        "url ": "https://preview.redd.it/qyzkvpl60bz51.jpg?width=320&crop=smart&auto=webp&s=f071f1091d0fd1f87261e256ea9bc6eb3c5d78d5",
                        "width ": 320
                    },
                    {
                        "height ": 1137,
                        "url ": "https://preview.redd.it/qyzkvpl60bz51.jpg?width=640&crop=smart&auto=webp&s=640fa6cc9115f9a7efb017475b4abeb75c8bcbc4",
                        "width ": 640
                    }
                ],
                "source ":
                {
                    "height ": 1600,
                    "url ": "https://preview.redd.it/qyzkvpl60bz51.jpg?auto=webp&s=7af77d0118b0424c063c5d330e3c48d1efc6cb38",
                    "width ": 900
                },
                "variants ": {}
            }
        ]
    } 
  }
]
````