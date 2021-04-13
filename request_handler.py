import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# from entries import get_all_entries


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/entries/1", the resulting list will
        # have "" at index 0, "entries" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        # Try to get the item at index 2
        try:
            # Convert the string "1" to the integer 1
            # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /entries
        except ValueError:
            pass  # Request had trailing slash: /entries/

        return (resource, id)  # This is a tuple

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        # If URL resource = entries
        if resource == "entry":
            if id is not None:
                response = f"{get_single_entry(id)}"

            else:
                response = f"{get_all_entries()}"

        # If URL resource = locations
        # elif resource == "locations":
        #     if id is not None:
        #         response = f"{get_single_location(id)}"

        #     else:
        #         response = f"{get_all_locations()}"


       

        #whatever is passed to this gets encoded and passed to the client
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new entry
        new_entry = None


        # Add a new entry to the list. Don't worry about
        # the orange squiggle, you'll define the create_entry
        # function next.
        if resource == "entry":
            new_entry = create_entry(post_body)

        # Encode the new entry and send in response
            self.wfile.write(f"{new_entry}".encode())


        # if resource == "customers":
        #     new_customer = create_customer(post_body)
        # # Encode the new customer and send in response
        #     self.wfile.write(f"{new_customer}".encode())


        # if resource == "employees":
        #     new_employee = create_employee(post_body)
        
        # # Encode the new employee and send in response
        #     self.wfile.write(f"{new_employee}".encode())


        # if resource == "locations":
        #     new_location = create_location(post_body)
        # # Encode the new location and send in response
        #     self.wfile.write(f"{new_location}".encode())



    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        self.do_POST()

    
    # def do_DELETE(self):
    #     # Set a 204 response code
    #     self._set_headers(204)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     # Delete a single entry from the list
    #     if resource == "entries":
    #         delete_entry(id)
    #     if resource == "customers":
    #         delete_customer(id)
    #     if resource == "employees":
    #         delete_employee(id)
    #     if resource == "locations":
    #         delete_location(id)

    #     # Encode the new entry and send in response
    #     self.wfile.write("".encode())

    # def do_PUT(self):
    #     self._set_headers(204)
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     post_body = json.loads(post_body)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    #     # Delete a single entry from the list
    #     if resource == "entries":
    #         update_entry(id, post_body)
    #     # Encode the new entry and send in response
            
    #     elif resource == "customers":
    #         update_customer(id, post_body)
        
    #     elif resource == "employees":
    #         update_employee(id, post_body)
        
    #     elif resource == "locations":
    #         update_location(id, post_body)
    #     self.wfile.write("".encode())



# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()