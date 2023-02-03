from waitress import serve
from paste.translogger import TransLogger

from app.routes import app

# Run the web server on the specified network hosts/ports
def start_server(web_host, web_port, db_host, db_port):
    # Hostname and port for database
    app.config["db_host"] = db_host
    app.config["db_port"] = db_port

    # Should ingestion requests be authenticated by API key
    app.config["authenticate_ingestion"] = True

    print(f"Starting web server on {web_host}:{web_port}")
    serve(TransLogger(app, setup_console_handler=False), host=web_host, port=web_port)

if __name__ == "__main__":
    start_server(web_host="0.0.0.0", web_port=80, db_host="localhost", db_port=3306)