# Server API

The interaction between the app and the server happens after the app is done collecting data and wants to send it to the server. The specifications are a bit vague on purpose, because we can rewrite the backend quite easily to handle whatever format the data is uploaded in.

Here's an outline of what the endpoint looks like:

1. It's called `<domain>/upload-data` (domain to be specified by the user for testing purposes), and the method should be an HTTP POST request.
2. Data should be encoded with `multipart/form-data`. Some options for Swift:

   - [This link](https://orjpap.github.io/swift/http/ios/urlsession/2021/04/26/Multipart-Form-Requests.html) is a blog post explaning how to do it and it seems like a pretty good option.
   - There's also [this library](https://github.com/Alamofire/Alamofire) called Alamofire that, in addition to handling `multipart/form-data` encoding, has a pretty good explainer.

3. The `multipart/form-data` should have:

   - Any number of data fields, named however you like (but descriptively). These should all be videos (in mp4, mov, webm, or some other format)
   - The same number of text fields, each corresponding to a data field and with the same name. The text here should be JSON-encoded contain a 2D matrix of gyroscope/accelerometer data captured during the video. Labels for the rooms can also be included in the JSON here, if we want to give the user that option.
   - An additional text field encoded with JSON containing information about movement between rooms.

4. The server will respond with a string (or a URL, we might change it) containing a unique label for the user's data.
