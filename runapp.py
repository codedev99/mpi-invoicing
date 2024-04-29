from app import create_app, add_data
import socket

hostname = socket.gethostname()
ipadd = socket.gethostbyname(hostname)
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        add_data()
    
    app.run(host=ipadd)