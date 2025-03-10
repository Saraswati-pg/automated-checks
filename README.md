### Running locally

Run the following commands to bootstrap your environment if you are unable to run the application using Docker

```bash
cd automatedChecks
pip install -r requirements/dev.txt
npm install
npm run-script build
npm start  # run the webpack dev server and flask server using concurrently
```

Go to `http://127.0.0.1:5000`. You will see a upload screen.
