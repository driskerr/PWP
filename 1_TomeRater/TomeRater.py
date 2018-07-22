class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{}'s email has been updated".format(self.name))

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        total = 0.
        count = 0
        for book in self.books:
            if self.books[book] is not None:
                total += self.books[book]
                count += 1
        try:
            average = total / count
            return average
        except ZeroDivisionError:
            return "{} has NOT rated any books".format(self.name)

    def __repr__(self):
        return "User: {}, email: {}, books read: {}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        if (self.name == other_user.name) and (self.email == other_user.email):
            return True
        else:
            return False

class Book(object):
    def __init__(self, title, isbn, price=None):
        self.title = title
        self.isbn = isbn
        self.price = price
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_number):
        self.isbn = new_number
        print("{}'s ISBN has been updated".format(self.title))

    def add_rating(self, rating):
        if type(rating) == int or type(rating) == float:
            if (rating >= 0) and (rating <= 4):
                self.ratings.append(rating)
            else:
                print("Invalid Rating")
        elif type(rating) == list:
            if (min(rating) >= 0) and (max(rating) <= 4):
                self.ratings += rating
            else:
                print("Invalid Rating. No ratings added.")
        elif rating is None:
            pass
        else:
            print("Invalid Rating. No ratings added.")


    def get_average_rating(self):
        total = 0.
        count = 0
        for rating in self.ratings:
            if rating is not None:
                total += rating
                count += 1
        try:
            average = total / count
            return round(average, 2)
        except ZeroDivisionError:
            return "There are no user ratings for {}!".format(self.title)

    def __repr__(self):
        return "Title: {}, ISBN: {}".format(self.title, self.isbn)

    def __eq__(self, other_book):
        if (self.title == other_book.title) and (self.isbn == other_book.isbn):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

class Fiction(Book):
    def __init__(self, title, author, isbn, price=None):
        super().__init__(title, isbn, price)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{} by {}".format(self.title, self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn, price=None):
        super().__init__(title, isbn, price)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{}, a {} manual on {}".format(self.title, self.level, self.subject)

class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn, price=None):
        if Book(title, isbn) not in self.books:
            return Book(title, isbn, price=price)
        else:
            print("{} is already in the system".format(title))

    def create_novel(self, title, author, isbn, price=None):
        return Fiction(title, author, isbn, price=price)

    def create_non_fiction(self, title, subject, level, isbn, price=None):
        return Non_Fiction(title, subject, level, isbn, price=price)

    def add_book_to_user(self, book, email, rating=None):
        if self.users[email] is None:
            print("No User with email {}".format(email))
        else:
            if book not in self.users[email].books:
                self.users[email].read_book(book, rating)
                book.add_rating(rating)
                if book not in self.books:
                    self.books[book] = 1
                else:
                    self.books[book] += 1
            else:
                self.users[email].read_book(book, rating)
                book.add_rating(rating)

    def add_user(self, name, email, user_books=None):
        if email not in self.users:
            self.users[email] = User(name, email)
            if user_books is not None:
                for book in list(set(user_books)):
                    self.add_book_to_user(book, email)
        else:
            print("User {} is already in the system".format(email))

    def print_catalog(self):
        for book in self.books:
            print(book)

    def print_users(self):
        for user in self.users:
            print(self.users[user])

    def most_read_book(self):
        for book in self.books:
            if self.books[book] == max(self.books.values()):
                print("\"{}\" is the most read book. It has been read {} times.".format(book.title, self.books[book]))

    def highest_rated_book(self):
        all_ratings = [book.get_average_rating() for book in self.books]
        top_book = None
        for book in self.books:
            if book.get_average_rating() == max(all_ratings):
                top_book = book
        print("\"{}\" is the highest rated book. It has an average rating of {}.".format(top_book.title, top_book.get_average_rating()))

    def most_positive_user(self):
        all_user_ratings = [self.users[user].get_average_rating() for user in self.users if type(self.users[user].get_average_rating()) != str]
        top_user = None
        for user in self.users:
            if self.users[user].get_average_rating() == max(all_user_ratings):
                top_user = self.users[user]
        print("{} is the most positive user. Their average rating is {}".format(top_user.name, top_user.get_average_rating()))

    def get_n_most_read_books(self, n):
        most_read_list = []
        for book in self.books:
            if self.books[book] >= sorted(list(self.books.values()))[-n:][0]:
                most_read_list.append(book)
        print(most_read_list)

    def get_n_most_prolific_readers(self, n):
        number_books_read = sorted([len(self.users[user].books) for user in self.users])
        prolific_list = []
        for user in self.users:
            if len(self.users[user].books) >= number_books_read[-n:][0]:
                prolific_list.append(user)
        print(prolific_list)

    def get_n_most_expensive_books(self, n):
        prices = sorted([book.price for book in list(self.books.keys()) if book.price is not None])
        gmost_expensive_list = []
        for book in list(self.books.keys()):
            if (book.price is not None) and (book.price >= prices[-n:][0]):
                most_expensive_list.append(book)
        print(most_expensive_list)

    def get_worth_of_user(self, user_email):
        total = 0
        for book in self.users[user_email].books:
            if book.price is not None:
                total += book.price
        print("{}'s library is worth ${:.2f}".format(self.users[user_email].name,total))


    def __repr__(self):
        return "In this TomeRater system there are {} users and {} books.".format(len(self.users), len(self.books))

    def __eq__(self, other):
        if (self.users == other.users) and (self.books == other.books):
            return True
        else:
            return False

"""
User Class Tests
"""
"""
#create user
kerry = User('Kerry', 'kerrydriscoll06033@gmail.com')
#print(kerry)

#change email
kerry.change_email('kerrydriscoll2016@u.northwestern.edu')
print(kerry.get_email())
#print(kerry)

#equivalence
driscoll = User('Kerry', 'kerrydriscoll06033@gmail.com')
#print(driscoll == kerry)
"""
"""
Book Class Tests
"""
"""
#create book
Catch = Book('Catch 22', 9780099529118)
print(Catch)

#test methods
print(Catch.get_title())
print(Catch.get_isbn())

#change ISBN
#Catch.set_isbn(194865)
#print(Catch)

#add a rating
##valid
Catch.add_rating(3.5)
Catch.add_rating(4)
Catch.add_rating([4.0, 3.8])
print(Catch.ratings)
##invalid
Catch.add_rating(6)
Catch.add_rating([4.0, 7.9])
print(Catch.ratings)

#equivalence
Heller = Book('Catch 22', 9780099529118)
print(Catch == Heller)
"""
"""
Fiction Subclass Tests
"""
"""
#create fiction
Catch = Fiction('Catch 22', 'Joseph Heller', 9780099529118)
print(Catch)

#test methods
print(Catch.get_title())
print(Catch.get_isbn())
print(Catch.get_author())
"""
"""
Non-Fiction Subclass Tests
"""
"""
#create non-fiction
Lupino = Non_Fiction('Ida Lupino, Director', 'Film', 'college', 9780813574905)
print(Lupino)

#test methods
print(Lupino.get_title())
print(Lupino.get_isbn())
print(Lupino.get_subject())
print(Lupino.get_level())
"""
"""
Tests Interaction of Books and Users
"""
"""
kerry.read_book(Catch, 3)
kerry.read_book(Lupino, 4.2)
kerry.read_book('Great Gatsby')
print(kerry.books)
print(kerry.get_average_rating())

#Catch.add_rating([4.0, 3.8, 3.5, 2.8, 3.8])
print(Catch.ratings)
print(Catch.get_average_rating())
"""
"""
Tests of TomeRater
"""
"""
TR = TomeRater()
Catch = TR.create_novel('Catch 22', 'Joseph Heller', 9780099529118)
Heller = TR.create_book('Catch 22', 9780099529118, 7.22)
Catch.add_rating([4, 3.8, 3.9])
#print(Catch == Heller)
#print(list(set([Catch, Heller])))
Lupino = TR.create_non_fiction('Ida Lupino, Director', 'Film', 'college', 9780813574905, 20.99)
Lupino.add_rating([2.2, 3, 3.5])
InColdBlood = TR.create_non_fiction('In Cold Blood', 'True Crime', 'intermediate', 9780784805060, 12.08)

TR.add_user('Kerry', 'kerrydriscoll06033@gmail.com', user_books=[Catch, Lupino])
TR.add_user('Bridget', 'bdrizz178@sbcglobal.net', user_books=[Lupino])
TR.add_book_to_user(Heller, 'bdrizz178@sbcglobal.net', rating=3.5)
TR.add_user('Bridget Driscoll', 'bdrizz178@sbcglobal.net')
TR.add_book_to_user(Catch, 'bdrizz178@sbcglobal.net', rating=3.8)
TR.add_book_to_user(InColdBlood, 'bdrizz178@sbcglobal.net', rating=4)
print(TR.users['bdrizz178@sbcglobal.net'].books)
print(Lupino.ratings)
TR.print_catalog()
TR.print_users()
TR.most_read_book()
TR.highest_rated_book()
TR.most_positive_user()
TR.get_n_most_read_books(2)
TR.get_n_most_prolific_readers(1)
TR.get_n_most_expensive_books(1)
TR.get_worth_of_user('bdrizz178@sbcglobal.net')
TR.get_worth_of_user('kerrydriscoll06033@gmail.com')
"""
