import socket
import threading

class SudhanvaPy:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.routes = {}

    def route(self, path):
        def wrapper(func):
            self.routes[path] = func
            return func
        return wrapper

    def handle_request(self, request):
        try:
            if not request:
                return b"HTTP/1.1 400 Bad Request\n\n<h1>400 Bad Request</h1>"
            
            request_line = request.decode().splitlines()[0]
            method, path, _ = request_line.split()
            print(f"{method} {path}")

            if path in self.routes:
                response = self.routes[path]()
                return f"HTTP/1.1 200 OK\nContent-Type: text/html\n\n{response}".encode()
            else:
                return b"HTTP/1.1 404 Not Found\n\n<h1>404 Page Not Found</h1>"
        except Exception as e:
            print(e)
            return b"HTTP/1.1 500 Internal Server Error\n\n<h1>500 Internal Server Error</h1>"

    def client_handler(self, client_socket, addr):
        print(f"Connected: {addr}")
        request = client_socket.recv(1024)
        response = self.handle_request(request)
        client_socket.sendall(response)
        client_socket.close()

    def run(self):
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"🔥 SudhanvaPy running at http://{self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                thread = threading.Thread(target=self.client_handler, args=(client_socket, addr))
                thread.start()
        except OSError as e:
            print(f"Server error: {e}")
            print("Make sure your environment allows socket binding and listening.")


# Example Usage
if __name__ == "__main__":
    app = SudhanvaPy()

    STYLE = """
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; text-align: center; }
        h1 { color: #333; }
        p { color: #555; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }
        nav { background: #007bff; padding: 10px; }
        nav a { color: white; margin: 10px; text-decoration: none; font-size: 18px; }
        .section { margin: 20px 0; padding: 10px; background: #e9ecef; border-radius: 10px; }
    </style>
    """

    @app.route("/")
    def home():
        return f"""
        {STYLE}
        <nav><a href='/'>Home</a> | <a href='/about'>About</a></nav>
        <div class='container'>
            <h1>Welcome to SudhanvaPy Framework 🔥</h1>
            <p>A lightweight Python web framework made for simplicity and speed.</p>
        </div>
        """

    @app.route("/about")
    def about():
        return f"""
        {STYLE}
        <nav><a href='/'>Home</a> | <a href='/about'>About</a></nav>
        <div class='container'>
            <h1>About SudhanvaPy</h1>
            <p>SudhanvaPy is a minimalistic Python web framework built for learning and rapid prototyping.</p>
            <p>Developed by Sudhanva J Rao, this project is designed to give insights into how web servers work.</p>
            <div class='section'>
                <h2>Hip Hop Music</h2>
                <p>Sudhanva loves hip hop music, especially artists like SeedheMaut, Kendrick Lamar, and Talha Anjum.</p>
            </div>
            <div class='section'>
                <h2>Bikes</h2>
                <p>Bikes are more than just a passion — they represent freedom and adrenaline for Sudhanva.</p>
            </div>
            <div class='section'>
                <h2>Coding</h2>
                <p>Sudhanva enjoys coding and building projects like this custom Python framework.</p>
            </div>
        </div>
        """

    app.run()
