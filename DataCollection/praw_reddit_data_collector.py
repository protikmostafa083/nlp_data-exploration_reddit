import praw
import csv
import threading
from queue import Queue


class RedditScraper:
    client_id = 'T0Yw8hzg-_CpReakMslQZQ'
    client_secret = 'bnigIaBeAaX2c0ENNZwwKdYGdKmrxg'
    user_agent = 'Mostafa Mohiuddin Jalal'

    def __init__(self, search_limit=None, num_threads=10, time_filter='all', sort_method='relevance'):
        self.reddit = praw.Reddit(client_id=self.client_id, client_secret=self.client_secret, user_agent=self.user_agent)
        self.search_limit = search_limit
        self.num_threads = num_threads
        self.time_filter = time_filter
        self.sort_method = sort_method

        self.result_queue = Queue()
        self.processed_ids = set()

    def scrape_data(self):
        while True:
            post = self.result_queue.get()
            if post is None:
                break
            content = post.selftext.replace('\n', ' ')  # Replace newlines with spaces
            result_dict = {
                'subreddit': post.subreddit.display_name,
                'username': post.author.name,
                'url': post.url,
                'upvotes': post.score,
                'content': content,
                'date': post.created_utc
            }
            if post.id not in self.processed_ids:
                self.processed_ids.add(post.id)
                self.result_queue.task_done()
                yield result_dict
            else:
                self.result_queue.task_done()

    def fetch_data(self, search_query):
        for post in self.reddit.subreddit('all').search(search_query, limit=self.search_limit, time_filter=self.time_filter, sort=self.sort_method):
            if post.is_self:  # Exclude posts that only contain a link to an image or video
                self.result_queue.put(post)

        for i in range(self.num_threads):
            self.result_queue.put(None)

    def save_data(self, csv_file):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ['subreddit', 'username', 'url', 'content', 'upvotes', 'date']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result_dict in self.scrape_data():
                writer.writerow(result_dict)
                print(f'{len(self.processed_ids)} posts found so far...')

    def run(self, search_query, csv_file):
        threads = []
        for i in range(self.num_threads):
            t = threading.Thread(target=self.fetch_data, args=(search_query,))
            t.start()
            threads.append(t)

        self.save_data(csv_file)

        for t in threads:
            t.join()