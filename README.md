# LangChain Playground
A playground based on Quickstart tutorial from [LangChain](https://python.langchain.com/docs/get_started/quickstart).

## Preparations
#### Create virtual environment and install dependencies
Creating a Python virtual environment is a useful practice for isolating dependencies and project environments. Here's how you can create one using the `venv` module, which comes built-in with Python 3:

1. **Open your terminal or command prompt**: This is where you'll enter commands to create the virtual environment.

2. **Navigate to your project directory (if not already there)**: Use the `cd` command to change directories.

3. **Create the virtual environment**: Run the following command:

```bash
python3 -m venv myenv
```

Replace `myenv` with the name you want to give your virtual environment. This command will create a directory named `myenv` (or whatever name you chose) containing the virtual environment.

4. **Activate the virtual environment**: Activating the virtual environment isolates your Python environment from the system-wide Python installation. 

   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```

   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```

   You'll notice that your command prompt or terminal prompt changes, indicating that you're now working within the virtual environment.

5. **Install dependencies**: Once your virtual environment is activated, you can use `pip` to install packages just like you would in a global Python environment. To install LangChain dependencies in this project:

```bash
pip install -r requirements.txt
```

6. **Deactivate the virtual environment**: When you're done working in the virtual environment, you can deactivate it by simply running:

```bash
deactivate
```

This will return you to your global Python environment.


## Running the projects

#### Install JupyterLab and run LangChain Tutorials
Install JupyterLab, an interactive development environment for working with notebooks, code, and data, using `pip`, the Python package manager. Here's how to do it:

1. **Ensure you have Python installed**: JupyterLab requires Python 3.6 or greater.

2. **Activate your virtual environment**:

   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```

   - On macOS and Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install JupyterLab**: Run the following command in your terminal or command prompt:

```bash
pip install jupyterlab
```

5. **Export OpenAI and Tavily API key** Register OpenAI and Tavily account, export API keys for authorizing calls.

```bash
export OPENAI_API_KEY="sk-XXX...XXX"
export TAVILY_API_KEY="tvly-XXX...XXX"
```

6. **Launch JupyterLab**: After installation, you can start JupyterLab by running the following command in project root.:

```bash
jupyter lab
```

This command will start the JupyterLab server and open a new tab in your default web browser with the JupyterLab interface. Open `langchain_tutorial.ipynb` to test LangChain tutorial.

7. **Deactivate the virtual environment (if you created one)**: After you're done using JupyterLab, you can deactivate the virtual environment by running:

```bash
deactivate
```

This will return you to your global Python environment.

#### Serving LangChain chains as a REST API using LangServe
1. **Start the server**: This will start the LangChain server at localhost, port 8000.

```bash
python3 langserve/serve.py

or

python3 langserve/serve.py --source {default,pdf,image}
```
Output:
```bash
Starting server...
INFO:     Started server process [85575]
INFO:     Waiting for application startup.

 __          ___      .__   __.   _______      _______. _______ .______     ____    ____  _______
|  |        /   \     |  \ |  |  /  _____|    /       ||   ____||   _  \    \   \  /   / |   ____|
|  |       /  ^  \    |   \|  | |  |  __     |   (----`|  |__   |  |_)  |    \   \/   /  |  |__
|  |      /  /_\  \   |  . `  | |  | |_ |     \   \    |   __|  |      /      \      /   |   __|
|  `----./  _____  \  |  |\   | |  |__| | .----)   |   |  |____ |  |\  \----.  \    /    |  |____
|_______/__/     \__\ |__| \__|  \______| |_______/    |_______|| _| `._____|   \__/     |_______|

LANGSERVE: Playground for chain "/agent/" is live at:
LANGSERVE:  │
LANGSERVE:  └──> /agent/playground/
LANGSERVE:
LANGSERVE: See all available routes at /docs/

INFO:     Application startup complete.
INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
```
2. **Run the client**: This will run the client that talk to LangChain server at localhost, port 8000.

```bash
python3 langserve/client.py
```
Output:
```bash
Question: Can LangSmith help test my LLM applications?
Answer: Yes, LangSmith can help you with your LLM applications. LangSmith provides personalized guidance and support throughout the application process, including reviewing your application materials, providing feedback, and offering tips and strategies to enhance your chances of success. Additionally, LangSmith can assist you in researching and selecting the best LLM programs that align with your interests and goals.
================================================
```
