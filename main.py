from website import create_app
import os
from dotenv import load_dotenv


app = create_app()
load_dotenv()


if __name__ == '__main__':
    # port = int(os.getenv("PORT"))
    # app.run(port=port, debug=True)
    app.run(debug=True)
