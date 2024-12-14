Start Using project and below are the Json formats to use in POST methods

http://127.0.0.1:8000/User/createUser

{
    "name": "John Doe",
    "email": "johndoe@example.com",
    "password": "securepassword"
}


http://127.0.0.1:8000/createBook

{
    "book_id": "12345",
    "title": "Book Title",
    "author": "Book Author",
    "description": "Book Description"
}


http://127.0.0.1:8000/User/<int:id>/borrowRequest

{
    "book": 1,
    "start_date": "2024-12-15",
    "end_date": "2024-12-20"
}


http://127.0.0.1:8000/<int:request_id>/borrowRequest/

{
  "action": "approve"
}

