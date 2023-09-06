from atlassian import Confluence

class ConfluenceWiki(object):
    def __init__(self, host_address, bearer_token, page_parent_id=None, page_id=None, port=443):
        self.host_address = host_address
        self.port = port
        self.bearer_token = username
        self.page_parent_id = page_parent_id
        self.page_id = page_id
        self.confluence = Confluence(url=f'{self.host_address}:{self.port}/confluence', token=self.bearer_token)

    def set_page_id(self, page_id):
        self.page_id = page_id
    
    def get_page_id(self):
        return self.page_id

    def update_csv(self, filename):
        with open(filename, "w") as f:
            f.write("X,Y,Z\n1,2,3\n4,5,6\n8,9,10")
        confluence.attach_file(filename, page_id=self.page_id)