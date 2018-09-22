import os
import json
import htmlmin

from sigpy.utils import vprint

SAVE_TO = "sigpy/faculties/%s/cache/"  # cache folder in each faculty


# this class defines all the variables and methods that the faculty class should implement
class cache:

    def __init__(self, faculty, save_cache):
        self.path = SAVE_TO % faculty
        self.filepath = self.path + "_cache.json"
        self.save_cache = save_cache
        self._cache = self._load_requests()

    # reads the previously saved cache from disk
    def _load_requests(self):
        if os.path.exists(self.path) and self.save_cache:
            with open(self.filepath) as infile:
                return json.load(infile)
        return {}

    # performs a GET request, if necessary, and returns the HMTL response
    def get(self, session, url):
        if self.save_cache and url in self._cache:  # value is stored in cache
            return self._cache[url]
        else:  # a new request is needed
            req = session.get(url)  # perform the request
            if req.status_code != 200:  # if request fails, display the error code (404, ...)
                vprint("[-] [%s] status code on:\n    %s" % (req.status_code, url))
                return ""
            self.save(url, req.text)
            return req.text

    # adds to the inner representation of the memory and also saves to disk
    def save(self, url, html):
        if not self.save_cache:
            return
        # create the cache folder if it does not exist
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self._cache[url] = minified = htmlmin.minify(html, remove_empty_space=True)
        with open(self.filepath, 'w') as outfile:
            json.dump(self._cache, outfile)

    # completely deletes the cache
    def delete(self):
        os.unlink(self.path)
