# PyOhio '14
###### or to Josh, "Ohpyo"...

What info can I relay?



There was a lot I learned from...

~10 hours of lectures.



# Talks I Attended

* Make API Calls Wicked Fast with Redis

* Introduction to Pandas

* A gentle introduction to asyncio

* Functional programming in Python with PyToolz


* Pushy Postgres and Python

* Postgres with Python inside and out: PL/Python

* HOWTO: Teach Python to Read

* The Clean Architecture in Python

* Configman - the grand unified theorem of configuration



# Most Relevant to VK


### pandas 

### (statistical analysis framework)


### postgres 

### (a relational db alternative to mysql)


### the clean architecture



## What should I talk about?

* PostgreSQL
* Clean Architecture


### pandas
    
Will be covered by Billy


### I also learned about some tools

* [IPython notebook](http://ipython.org/notebook.html)
* This presentation framework: [reveal.js](https://github.com/hakimel/reveal.js)



## Why care about PostgreSQL?

We use MySQL, why would we convert or consider converting?



# Some features


* Large database management features
    * tablespaces, table partitioning


* Powerful query planner & executor
    * complex queries, nested subselects, outer joins
    * large many-table joins with multiple join types


* Data mining
    * full text indexing & regex support
    * embed external language DM modules



## Transactional DDL


Excellent support for schema changes (migrations)


Hopefully less corruptions, if the programmer is careful!



## Exotic types


Can store and use:

* arrays
* GIS (spatial data)
* ISN & ISBN (amazon collection?)
* XML
* and more...



## You can include 

## procedural languages inside


We can write a python script to transform something like an ugly datetime string!



## Performance and Capabilities

In a nutshell:


* MySQL: Better w/ simple queries & 2-core machines
    * motivated by Application Developers

* PostgreSQL: Better w/ complex queries & multi-core machines
    * motivated by Database Administrators



# Why Else?


Postgres's powerful nested subquery performance.


Recommended by many a speaker at PyOhio.


[Avoid nested subqueries in mysql at all costs](http://www.selikoff.net/2008/12/10/memo-avoid-nested-queries-in-mysql-at-all-costs/)


In turn, MySQL's lack of optimization in nested query performance requires...


The breaking up of queries into *multiple parts* and...


The use of complex joins

(much faster but potentially harder to read)


Read [this little post](http://dba.stackexchange.com/questions/41232/performance-difference-between-mysql-and-postgresql-for-the-same-schema-queries) in your free time and learn about some key differences in common queries.


Or just use

    EXPLAIN query



## TL;DR - Tradeoffs

Primary key lookups are fast, Fast, *FAST* in MySQL

Complex joins/work-loads are faster in Postgres than MySQL



## Benchmarks

* [Index creation benchmarks](http://www.randombugs.com/linux/mysql-postgresql-benchmarks.html)
* [Concurrency benchmarks](http://tweakers.net/reviews/657/6/database-test-dual-intel-xeon-5160-overview.html)
* [More recent performance benchmarks (using drupal)](http://posulliv.github.io/2012/06/29/mysql-postgres-bench/)


## Citations

* [Excellent slideshow on MySQL & Postgres](http://www.slideshare.net/PGExperts/development-of-83-in-india)



# Pushy Postgres


Here's a use case for Postgres


Polling to find out the popularity of whoopi_pics:

    def check_if_whoopi_was_mentioned():
        query = '''SELECT * 
                   FROM tweet
                   WHERE tweet.content = "@whoopi_pics"
                   AND tweet.posted_at < 15 min ago'''

        sleep(9000) # 15 minutes
        check_if_whoopi_was_mentioned()


Let's avoid that.


Postgres has a notification stream


If I specify:

    NOTIFY whoopi_pics_was_mentioned


And craft a trigger on the save of a post about whoopi:

    CREATE TRIGGER whoopi_tweet
    AFTER UPDATE ON tweet
    FOR EACH ROW NOTIFY whoopi_pics_was_mentioned "whoopi_pics! woo!"


Now there's a magical stream with "whoopi_pics! woo!" on it.


If no one's listening, this means nothing...


But if we have a db connection and specify:

    LISTEN whoopi_pics_was_mentioned


We'll receive that string!



None of this means PostgreSQL is better than MySQL, simply that each system has chosen certain contexts to optimize and we should consider which technology better suits our needs.



## [The Clean Architecture](http://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html)


Proposed by ["Uncle Bob" Martin](https://en.wikipedia.org/wiki/Robert_Cecil_Martin)

He wrote a lot of craftsmanship books & Java (ack!) code.


I *really* like his writing and ideas.


So did this guy named [Brandon Rhodes](https://twitter.com/brandon_rhodes), an extremely passionate and influential speaker @ PyOhio.


He's also an astronomer and main contributor of the [skyfield api](https://github.com/brandon-rhodes/python-skyfield).

Which I think is quite cool.


This was my favorite talk of the conference.

I'm going to take a little bit too much from it, but I want to make sure Mr. Rhodes gets the credit.


You should watch it once it's [online](http://pyvideo.org)!


The talk was excellent but I'll only give a synopsis of it, while also using it as a springboard for more company-specific items.



# Clean?


Rhodes' example was exactly something we deal with at our company.

    def define_word(word):
        url = 'http://google.com?q={}'.format(word)
        source = requests.get(url)
        return parse_definition(source)


How is this not clean?

Python makes it easy to read & understand...


What if you have to introduce more logic to it?

Or want to define many words?


This is like writing a crawler.


More url building?

i.e. a spider we write must create a lot of urls like...
    
    for i in range(len(words)):
        query_string = "&wordCount=100&countIndex={}".format(i)


You say, nbd.


I'll just loop through my function (alter it) and I'll supply the url each time.

    def define_words(words, base_url):
        for i in range(len(words)):
            word = words[i]
            url = url_join(base_url, '&wordCount=100&countIndex={}'.format(i))
            define_word(word, url)

    def define_word(word, url):
        source = requests.get(url)
        return parse_definition(source)


Doesn't that seem clean?

When subroutines were proposed ~60 years ago, the main idea was to hide complexity.


We've hidden complexity by allowing a call to be as simple as
    
    define_words()

which calls

    define_word()

over & over



# Dirty


The procedure I just described was dirty.


What if we lose internet connectivity?


What if we want to use a new HTTP library?


What if google changes its query string format?


Can we easily change out those dependencies/tools while not touching our logic?


Not without reading the code thoroughly


Or looking for comments


Or comprehending the logic before/after


That sounds gross.

It's a reason fixing spiders can be a massive pain.


All of those things are not our code, not our fault for failing.


Those are the gory details.


We are hiding these dependencies & I/O in functions...

nested inside other functions?


Why don't we bring the I/O to the top level where it's easy to find?


If we know someone is unreliable, untrustable, and ultimately an enormous pain,

what should we do with them?


Make them a manager, of course.



# Making I/O Managers


![Clean Architecture](/imgs/CleanArchitecture.jpg)


What does this mean for the individual spider?


We can apply this architecture to any module, any small project.


Imagine the small example from before, broken up:

    def define_word():
        pass

    def build_url():
        pass

    def fetch_from_google():
        pass

    def parse_definition():
        pass


It seems we're currently doing this:

    def define_word():
        # build url
        code code code

        # fetch from google
        more code

        # parse definition
        moar code


Looks really similar, and in fact, we often don't have comments.

So it looks like:

    def define_word():
        code code code
        more code
        what's going on here??
        I have to read all of this???


Or worse:
    
    def foo():
        for item in items:
            for task in item.tasks():
                for column in task.dohickey():
                    if column.something():
                        query = '''select *
                                   from table
                                   join table2
                                   join table3
                                   join table4
                                   where time_created < utc.now()
                                   '''
                        db.execute(query, [column.1, column.2])
                        print 'more stuff'
                        print 'to do...'
                    else:
                        print 'wut'


Why does it matter?


Besides clarity, conciseness, replaceable/reusable parts...



# Testability


## Test?


Yes, test.


It seems we don't do enough unit tests.

Unit testing shouldn't be scary and it shouldn't be hard.


Testing means no more:

>"Oh, I need to redeploy,
I forgot I changed

>/

>the name of that function

>/

>the type of that variable

>/

>I messed up."


You'll still mess up but...

99% of the time it'll be locally.


If we require tests, good tests.


## Test Driven Development


Some programmers want to write tests first and 

*then* write code to pass them.


That's called TDD, and would be even better.



# Simple Spider


You may have heard this term thrown around.


It has some basis in this architecture. How?


Spider/Parser has this as input:

    "<html>.*</html>"


The programmer will define something like this through a tool like Spider-Testr

    {
      'regexes': ['span class="address">([^<]+)<',
                  'span class="other-address">([^<]+)'],
      'pyquery': ['span.address',
                  'span.other-address']
    }


And finally define the business logic separately (in subroutines)

    # theoretical address example
    def get_correct_address(address_elements):
        matches = filter(lambda e: is_valid_address(e), address_elements)
        address = None
        if matches:
            address = matches[0]
        return address


Now, each of the fields the programmer needs to persist can be parsed 
for using simple data structures as arguments.


No more: 

    from somethingapp.models import Model
    address = get_correct_address(Model.field_info)


![Swag](/imgs/swag.gif)


Do you really want to play with your 

database or python classes 

to test individual parts of your spider?


Hint: No.


Decouple things. Make your life easier. 


Make any function that relies on a tool outside of your control obvious.


Separate those functions. Don't hide them.

    # file.py

    ########### all your IO ###########

    def grab_HTML():
        pass

    def fetch_ad_content():
        pass

    ########### all your business logic ###########

    def parse_address():
        pass

    def parse_price():
        pass


Make it readable.


Make it *clean.*


Because humans forget what they do.


And you'll forget what you did.



## Why haven't I heard of this?


## Surprise functional programming talk!


### This design paradigm is a core tenant of FP


Ever hear of Lisp, Scheme, Clojure, F#?


They aren't the most popular languages, but the forward trend in Python is implementing core tenants of functional languages.


Functions like:
    
    len()
    sorted()
    filter()

And generators:

    [ item.cool_stuff for item in items ]


They seem to be magic.

They abstract away what happens underneath.


That's what any programmer's functions should do.

Remember this?

    def grab_HTML(url):
        pass

    def export_data(data):
        pass

    def parse_company_name(html):
        pass

    def parse_address(html):
        pass


Let's make that work (theoretically)

    # helper method
    def parse_everything(html):
        parsed_fields = {}
        name = parse_company_name(html)
        address = parse_address(html)
        parsed_fields.update({
            'name': name,
            'address': address
        })
        return parsed_fields


# Spider go!

    def do_the_spider(url):
        export = export_data(parse_everything(grab_HTML(url)))
        return export



## Ew, you have to read right-to-left


People are fixin' that

    from toolz import pipe
    export = pipe(grab_HTML(url), parse_everything, export_data)


## Those tools will be native in Python 3


Oh, and...

    def export_sorted_list(html):
        return pipe(html, parse_everything, export_data, list, sorted)



Why should we even be talking about this in relation to clean architecture?


We've created functions with clear: 

* input
* output
* names.


This eliminates a lot of commentation since your code becomes self-documenting.


And readability is part of a clean architecture.


This does *NOT* mean you should stop saying *WHY* you're doing something.



Yet, we're missing something. Two things actually.

1. Data > Workflow
2. Immutability



# 1. Data > Flow Chart


>"Show me your flowchart and conceal your tables, and I shall continue to be mystified. Show me your tables, and I won't usually need your flowchart; it'll be obvious." 

>\- Fred Brooks, *The Mythical Man-Month*


>"Show me your code and conceal your data structures, and I shall continue to be mystified. Show me your data structures, and I won't usually need your code; it'll be obvious." 

>\- Eric Raymond, *The Cathedral and the Bazaar*


Or most famously:

>"Bad programmers worry about the code. Good programmers worry about data structures and their relationships" - Linus Torvalds


## No one cares about how you code something

###### (well, some nerds do)


## Everyone cares what data you have to show



# 2. Immutability


## Without immutability,

## we'll have side effects


## Those can make bugs hard to find


What's a side effect?

    def make_bacon(pan, raw_bacon):
        turn_on_burner()
        place(raw_bacon, pan)
        turn_off_burner()
        cooked_bacon = raw_bacon
        return cooked_bacon

    def place(raw_bacon, pan):
        raw_bacon.is_cooked = True # side effect


Why is this a problem?


Well, if you don't alias bacon as cooked bacon...

    cooked_bacon = raw_bacon


Reading the code, it is not intuitive that 

    raw_bacon 

is now cooked.


If you mess with

    cooked_bacon

you're also messing with the 

    raw_bacon


And if you forget the alias you specified, and are passing it to many different mutating functions...


You may cook it twice 

    cooked_bacon # could be raw??

or think it's ready to eat!


Bugs, bugs, bugs, *bugs*


How could this be avoided?

    def make_bacon(pan, raw_bacon):
        turn_on_burner()
        cooked_bacon = place(raw_bacon, pan) # returns new object
        turn_off_burner()
        return cooked_bacon

    def place(raw_bacon, pan):
        cooked_bacon = Bacon(is_cooked=True)
        return cooked_bacon


Hopefully, you see how returning a new data structure can help clean up your code...


and, it will make you able to use pipe() and other utilities.


Learn from the python language community.


They previously used
    
    sort()

and now they use

    sorted()


Code like this:

    items = "box crate cargo-ship".split()
    items.sort()
    for item in items:
        do_something()

Now looks like:

    items = "box crate cargo-ship".split()
    for item in sorted(items):
        do_something()


A cool feature of programming in this style is its portability to [parallel computing.](http://www.cse.chalmers.se/edu/course/DAT280_Parallel_Functional_Programming/lectures.html)


Like anything else, though. It is not magic. 

Parallelism is still hard and any I/O needs to be clearly defined and dealt with.


But, by separating the I/O and side effect ridden code from the purely business logic: 


writing performant, readable, and clean code is a possibility.



# The End