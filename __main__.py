from app import init_app, host, port

if __name__ == "__main__":
    init_app().run(host=host,
                   port=port)
