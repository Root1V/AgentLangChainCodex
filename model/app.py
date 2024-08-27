import os
from dotenv import load_dotenv
from config import Config
import streamlit as st
import datetime
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_experimental.tools import PythonREPLTool

# Cargar las variables de entorno
load_dotenv()

# Obtener todos los valores de configuración
config = Config.get_all()

historyFile = "history.txt"


def save_history(question, answer):
    with open(historyFile, "a") as h:
        h.write(f"{datetime.datetime.now()}: {question} -> {answer}\n")


def load_history():
    if os.path.exists(historyFile):
        with open(historyFile, "r") as h:
            return h.readlines()
    return []


def clear_history():
    if os.path.exists(historyFile):
        open(historyFile, "w").close()


def download_file():
    with open(historyFile, "r") as f:
        file_contents = f.read()
    return file_contents


def agen_run(agent_executor, user_input):
    answer = agent_executor.invoke(input={"input": user_input})
    st.markdown("### Respuesta del Agente AI")
    st.code(answer["output"], language="python")
    save_history(user_input, answer["output"])


def main():
    st.set_page_config(
        page_title="Agente AI para Codigo de Programación", page_icon="", layout="wide"
    )
    st.title("Agent AI Codex")
    st.markdown(
        """
        <style>
        .title { color: #1B69F0; }
        .button { background-color: #ff4b4b; color: white; border-radius: 5px;}
        .input { border: 1px solid #ff4b4b; border-radius: 5px;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    prompt_system = """
        - Eres un agent de AI experto en programación con amplio conocimiento de buenas practicas y principios de diseño de software
        - Debes de usar siempre el codigo de python para responder.
        - Solo responder a la pregunta escribiendo codigo, incluso si sabes la respuesta.
        - Si no sabes la respuesta, responde "no se la respuesta"
    """

    st.markdown("### Instrucciones:")
    st.markdown(prompt_system)

    base_prompt = hub.pull("langchain-ai/react-agent-template")
    print("\nPrint prompt AI Agent React:", base_prompt)

    prompt = base_prompt.partial(instructions=prompt_system)
    st.write("Prompt base cargado...")

    tools = [PythonREPLTool()]
    llm = ChatOpenAI(model=config["model"], temperature=config["temperature"])

    # creamos el agente
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Run con ejemplos
    st.markdown("### Ejemplos:")
    examples = [
        "Calcula la division de 1234/5678",
        "Genera una lista con los 15 primeros numeros primos",
        "Crea una funcion que calcule el factorial del numero",
        "Calcula el factorial del numero 19",
    ]
    examp = st.selectbox("Selecciona un ejemplo:", examples)

    if st.button("Ejecutar ejemplo"):
        user_input = examp
        agen_run(agent_executor, user_input)

    # Capturar el input del usuario.
    user_input = st.text_input(
        "Introduce tu pregunta para el agente:", key="input_text"
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        exec = st.button("Ejecutar", key="exec_button")
    with col2:
        clean = st.button("Limpiar historial", key="clear_button")
    with col3:
        download = st.download_button(
            "Descargar historial",
            key="down_button",
            data=download_file(),
            file_name="full_history.txt",
        )

    if exec:
        if user_input:
            agen_run(agent_executor, user_input)
        else:
            st.warning("Ingresa una pregunta para el Agente AI")

    if clean:
        clear_history()

    if download:
        st.write("Descarga exitosa...")

    st.markdown("### Hostorial de consultas")
    history = load_history()
    if history:
        for h in history:
            st.text(h)
    else:
        st.write("No hay historial....")


if __name__ == "__main__":
    main()
