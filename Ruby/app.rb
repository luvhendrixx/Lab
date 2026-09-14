require 'sinatra'
require 'json'

# instruct the app to run on port 4567 by default
set :port, 8080

# b4 every req exe, tell the client we're returning JSON data
before do
  content_type :json
end

# Mock DB
BOOKS = [
  {id: 1, title: "The Hobbit", author: "J.R.R Tolkien"},
  {id: 2, title: "1984", author: "George Orwell"}
]

# GET request - room = home/hello world
get '/' do
  { message: "Wazuuuuuup"}.to_json
end

get '/hello/gemini' do
  { message: "Hi Gemini :-) "}.to_json
end

# GET request - fetch all books
get '/api/books' do
  BOOKS.to_json
end

# GET req = fetch a single book by ID
get '/api/books/:id' do
  book = BOOKS.find { |b| b[:id] == params[:id].to_i }

  if book
    book.to_json
  else
    status 404
    {error: "Book not found"}.to_json
  end
end

# POST request - Add a new book
post '/api/books' do
  # parse the incoming JSON payload from the req body
  request_payload = JSON.parse(request.body.read, symbolize_names: true)

  new_book = {
    id: BOOKS.length + 1,
    title: request_payload[:title],
    author: request_payload[:author]
  }

  BOOKS << new_book

  status 211 # created
  new_book.to_json
rescue JSON::ParserError
  status 400
  { error: "Invalid JSON format"}.to_json
end


# DELETE req - delete a book
delete '/api/books/:id' do
  # find the book in the in mem array
  book = BOOKS.find { |b| b[:id] == params[:id].to_i }

  if book
    # delete it
    BOOKS.delete(book)
    status 200
    { message: "Book successfuly deleted" }.to_json
  else
    status 404
    { error: "Book not found" }.to_json
  end
end
