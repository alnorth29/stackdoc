from pymongo import Connection
import sys
from xml.sax import make_parser, handler

class SOProcessor(handler.ContentHandler):

    def __init__(self):
        connection = Connection()
        self._db = connection.stack_doc
        self._posts = self._db.posts
        self._count = 0

    def startElement(self, name, attrs):
        if name == "row":
            if attrs["PostTypeId"] == "1":
                if "<.net>" in attrs["Tags"] and "http://msdn.microsoft.com/" in attrs["Body"]:
                    matches = re.findall(r"http://msdn\.microsoft\.com/en\-us/library/([a-zA-Z0-9\.]+)(_[a-z]+)?\.aspx", attrs["Body"])
                    ids = []
                    for match_tuple in matches:
                        ids.append(match_tuple[0])
                        print match_tuple[0]
                    post = {
                        "page_ids": ids,
                        "id": attrs["Id"],
                        "url": "http://stackoverflow.com/questions/%s" % attrs["Id"],
                        "title": attrs["Title"],
                        "score": attrs["Score"],
                        "answers": attrs["AnswerCount"],
                        "accepted_answer": "AcceptedAnswerId" in attrs
                    }
                    #self._posts.insert(post)
                    self._count += 1
                    print self._count
            
parser = make_parser()
parser.setContentHandler(SOProcessor())
parser.parse(open(sys.argv[1]))