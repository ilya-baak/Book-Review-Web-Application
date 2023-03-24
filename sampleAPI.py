# For complete guide refer to API documentation  here https://developers.google.com/books/docs/v1/using
import requests


# Function to get the AVG review and number of reviews for the given book
def getAPIRatings(isbn):
    url = "https://www.googleapis.com/books/v1/volumes?"
    params = {"q": f"isbn:{isbn}", "fields": "items(volumeInfo(averageRating,ratingsCount))"}
    res = requests.get(url, params=params)

    book_data = res.json()["items"][0]["volumeInfo"]
    average_rating = book_data["averageRating"]
    ratings_count = book_data["ratingsCount"]
    return (average_rating, ratings_count)


#Example request
#x = getAPIRatings("0374528373")
#print('AVG RATING:', x[0], 'RATING COUNT', x[1])